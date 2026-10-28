// Tiny DOM helpers shared by the widgets. No dependencies.

export const h = (tag, attrs = {}, ...kids) => {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (v == null) continue;
    if (k === "class") el.className = v;
    else if (k.startsWith("on")) el.addEventListener(k.slice(2), v);
    else if (k === "html") el.innerHTML = v;
    else el.setAttribute(k, v);
  }
  for (const c of kids.flat()) if (c != null) el.append(c.nodeType ? c : document.createTextNode(String(c)));
  return el;
};

export const svg = (tag, attrs = {}, ...kids) => {
  const el = document.createElementNS("http://www.w3.org/2000/svg", tag);
  for (const [k, v] of Object.entries(attrs)) if (v != null) el.setAttribute(k, String(v));
  for (const c of kids.flat()) if (c != null) el.append(c);
  return el;
};

export const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
export const W = (w) => (w === "" ? "ε" : esc(w));
export const wordSpan = (w, cls = "") => `<span class="${cls}">${W(w)}</span>`;
export const field = (label, input) => h("label", {}, label + " ", input);
export const row = (...kids) => h("div", { class: "row" }, ...kids);
export const btn = (label, onclick, attrs = {}) => h("button", { ...attrs, onclick }, label);
export const yes = (b, y = "yes", n = "no") =>
  b ? `<b style="color:var(--green)">${y}</b>` : `<b style="color:var(--pink)">${n}</b>`;

export const parseAlphabet = (s) => [...new Set([...String(s).replace(/[\s,{}]/g, "")])].filter((c) => /[a-z]/.test(c));
export const parseList = (s) => String(s).split(/[\s,]+/).filter(Boolean).map((x) => (x === "ε" || x === "[]" ? "" : x));

export const clampStep = (i, total) => Math.max(0, Math.min(total, i));

// Buttons that step through a sequence: ⏮ ◀ ▶ with a counter. `onset(i)` runs on each press.
// It is deliberately NOT called during construction: callers that re-render themselves from
// `onset` would otherwise recurse forever when the re-render rebuilds the stepper. Render the
// state for `i0` yourself.
export function stepper(total, onset, i0 = 0) {
  let i = clampStep(i0, total);
  const label = h("span", { class: "small muted" }, ` step ${i} / ${total}`);
  const go = (k) => { i = clampStep(k, total); label.textContent = ` step ${i} / ${total}`; onset(i); };
  const bar = h("div", { class: "row steps" },
    btn("⏮", () => go(0), { title: "reset" }),
    btn("◀", () => go(i - 1), { title: "back" }),
    btn("▶", () => go(i + 1), { title: "forward", class: "primary" }),
    label);
  return { bar, go, get index() { return i; } };
}
