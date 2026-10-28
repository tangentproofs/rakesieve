// Shared reader-progress model. The same file is copied into every tangentproofs informalization
// site (star-height, fourcolor-lean, turyn, eulers-gem); keep the copies identical.
// Tested by tools/test_progress.mjs.
//
// localStorage schema v2: { v: 2, nodes: { [id]: { viewed?, quizPassed?, signedOff?, answers? } } }
//   signedOff  = the reader ticked "I understand the formal statement" (always available)
//   quizPassed = the reader got every quiz question right (independent of signedOff)
// v1 → v2: under v1 the sign-off box only unlocked after the quiz was passed, so every v1 sign-off
// also passed the quiz. Migration fills in quizPassed for those, so they show as "both".

export const PROGRESS_VERSION = 2;
export const emptyProgress = () => ({ v: PROGRESS_VERSION, nodes: {} });

/** Bring a stored or imported progress object up to v2 (mutates and returns it; never throws). */
export function migrateProgress(p) {
  if (!p || typeof p !== "object" || Array.isArray(p) || !p.nodes || typeof p.nodes !== "object" || Array.isArray(p.nodes)) return emptyProgress();
  const v = Number.isFinite(Number(p.v)) && Number(p.v) > 0 ? Number(p.v) : 1;
  if (v < 2) {
    for (const r of Object.values(p.nodes)) {
      if (r && typeof r === "object" && r.signedOff && !r.quizPassed) r.quizPassed = r.signedOff;
    }
  }
  p.v = PROGRESS_VERSION;
  return p;
}

/** A node's own progress state, ignoring its dependencies.
 *  both  = ticked "I understand" and passed the quiz      (darkest green)
 *  quiz  = passed the quiz, not (yet) ticked              (middle green)
 *  signed = ticked "I understand", quiz not passed        (lightest green)
 *  explained = has an explainer, nothing done yet; stub = no explainer (cannot be signed or quizzed). */
export function ownStatus(r, hasExplainer) {
  if (!hasExplainer) return "stub";
  const s = !!r?.signedOff, q = !!r?.quizPassed;
  return s && q ? "both" : q ? "quiz" : s ? "signed" : "explained";
}

export const STATUS_ORDER = ["both", "quiz", "signed", "explained", "stub"];
export const STATUS_LABEL = {
  both: "understood + quiz passed",
  quiz: "quiz passed",
  signed: "marked understood",
  explained: "has explainer",
  stub: "needs explainer",
};
// Three distinguishable greens, darkest = most done. All take dark (#111) text at ≥ 6.7:1 and stand
// out from the dark panels at ≥ 5:1 (checked in tools/test_progress.mjs).
export const COLORS = { both: "#4caf50", quiz: "#a6e22e", signed: "#d9f99d", explained: "#66d9ef", stub: "#75715e" };
export const PENDING_COLOR = "#ae81ff";

/** understood(id): the reader marked `id` understood AND everything its statement mentions is
 *  understood (recursively). Passing the quiz alone does not count. Memoised; call clear() after
 *  progress changes. `isSigned(id)` says whether `id` carries a sign-off; `meaningDeps(id)` lists
 *  the project declarations its statement mentions. */
export function makeUnderstood(isSigned, meaningDeps) {
  const memo = new Map();
  function understood(id, stack = new Set()) {
    if (memo.has(id)) return memo.get(id);
    if (stack.has(id)) return false;
    stack.add(id);
    const r = !!isSigned(id) && (meaningDeps(id) || []).every((d) => understood(d, stack));
    stack.delete(id);
    memo.set(id, r);
    return r;
  }
  understood.clear = () => memo.clear();
  return understood;
}

/** WCAG relative-luminance contrast ratio between two #rrggbb colours. */
export function contrast(a, b) {
  const lum = (h) => {
    const [r, g, b2] = [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16) / 255)
      .map((v) => (v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4));
    return 0.2126 * r + 0.7152 * g + 0.0722 * b2;
  };
  const x = lum(a), y = lum(b);
  return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05);
}

// ---- per-question quiz score (shown as stars) -------------------------------------------------
// r.correct: array of booleans, one per quiz question; a question stays filled once it has been
// answered correctly. Older records have no `correct`: a passed quiz counts as every star filled.

/** { right, total } for a node record and a quiz of `total` questions. */
export function quizScore(r, total) {
  total = Math.max(0, total | 0);
  if (Array.isArray(r?.correct)) {
    const right = r.correct.slice(0, total).filter(Boolean).length;
    return { right: r.quizPassed ? total : right, total };
  }
  return { right: r?.quizPassed ? total : 0, total };
}

/** Merge one round of answers (`oks[i]` true when question i is right now) into record `r`.
 *  Sets r.quizPassed (once) when every question has been answered correctly. Returns quizScore. */
export function recordQuizResults(r, oks, now = Date.now()) {
  const prev = Array.isArray(r.correct) ? r.correct : r.quizPassed ? oks.map(() => true) : [];
  r.correct = oks.map((ok, i) => !!(ok || prev[i]));
  if (oks.length && r.correct.every(Boolean) && !r.quizPassed) r.quizPassed = now;
  return quizScore(r, oks.length);
}

/** "★★☆☆" for a score. */
export const starString = ({ right, total }) => "★".repeat(right) + "☆".repeat(Math.max(0, total - right));
