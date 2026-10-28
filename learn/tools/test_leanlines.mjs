#!/usr/bin/env node
// Tests for assets/leanlines.js (wrapping Lean statements line by line) and the quiz star score
// in assets/progress.js.   node tools/test_leanlines.mjs
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { splitHtmlLines, wrapLeanLines, indentOf } from "../assets/leanlines.js";
import { highlight, linkMap } from "../assets/lean.js";
import { quizScore, recordQuizResults, starString, migrateProgress } from "../assets/progress.js";

const SITE = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
let n = 0;
const t = (name, fn) => { try { fn(); n++; } catch (e) { console.error(`FAIL ${name}:`, e.message); process.exit(1); } };
const strip = (h) => h.replace(/<[^>]+>/g, "").replace(/&#8203;/g, "").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&amp;/g, "&");
const balanced = (h) => { const st = []; for (const m of h.matchAll(/<(\/?)([a-z]+)[^>]*>/g)) { if (m[1]) { if (st.pop() !== m[2]) return false; } else st.push(m[2]); } return st.length === 0; };

t("split keeps plain lines", () => assert.deepEqual(splitHtmlLines("a\nb\n\nc"), ["a", "b", "", "c"]));
t("tags spanning a newline are closed and reopened", () => {
  const out = splitHtmlLines('x <span class="cm">-- one\ntwo</span> y');
  assert.deepEqual(out, ['x <span class="cm">-- one</span>', '<span class="cm">two</span> y']);
  assert.ok(out.every(balanced));
});
t("indentOf", () => { assert.equal(indentOf("    foo"), 4); assert.equal(indentOf("\tx"), 2); assert.equal(indentOf(""), 0); });
t("wrap: one .ln per line, indentation moved into --i, tail on the last line", () => {
  const w = wrapLeanLines('<span class="kw">theorem</span> x :\n    <span class="ty">P</span>', "theorem x :\n    P", "<i>t</i>");
  assert.equal(w, '<span class="ln" style="--i:0"><span class="kw">theorem</span> x :</span><span class="ln" style="--i:4"><span class="ty">P</span><i>t</i></span>');
});

// Every real declaration: wrapping loses no text (besides leading indentation) and stays well-formed.
const decls = JSON.parse(fs.readFileSync(path.join(SITE, "data/decls.json"), "utf8"));
t(`all ${decls.length} statements survive wrapping`, () => {
  for (const d of decls) {
    const html = highlight(d.statement, linkMap([...d.meaningDeps, ...d.proofDeps, d.id]));
    const w = wrapLeanLines(html, d.statement);
    assert.ok(balanced(w), `${d.id}: unbalanced`);
    const lines = [...w.matchAll(/<span class="ln" style="--i:(\d+)">/g)].map((m) => +m[1]);
    const src = d.statement.split("\n");
    assert.equal(lines.length, src.length, `${d.id}: line count`);
    assert.deepEqual(lines, src.map(indentOf), `${d.id}: indents`);
    assert.equal(strip(w.replace(/<\/span><span class="ln"[^>]*>/g, "\n")), src.map((l) => l.trimStart()).join("\n"), `${d.id}: text`);
  }
});

t("stars: score from per-question correctness", () => {
  assert.deepEqual(quizScore({}, 4), { right: 0, total: 4 });
  assert.deepEqual(quizScore({ correct: [true, false, true, false] }, 4), { right: 2, total: 4 });
  assert.equal(starString({ right: 2, total: 4 }), "★★☆☆");
});
t("stars: old quiz-passed data (no per-question record) shows all stars", () => {
  const p = migrateProgress({ v: 1, nodes: { a: { signedOff: 1 }, b: { quizPassed: 2 } } });
  assert.deepEqual(quizScore(p.nodes.a, 5), { right: 5, total: 5 }, "v1 sign-off ⇒ quiz passed ⇒ all stars");
  assert.deepEqual(quizScore(p.nodes.b, 3), { right: 3, total: 3 });
});
t("stars: correct answers stick across rounds; passing needs every star", () => {
  const r = {};
  assert.deepEqual(recordQuizResults(r, [true, false, false], 10), { right: 1, total: 3 });
  assert.equal(r.quizPassed, undefined);
  assert.deepEqual(recordQuizResults(r, [false, true, false], 11), { right: 2, total: 3 }, "earlier right answer stays filled");
  assert.deepEqual(recordQuizResults(r, [false, false, true], 12), { right: 3, total: 3 });
  assert.equal(r.quizPassed, 12);
  recordQuizResults(r, [false, false, false], 13);
  assert.equal(r.quizPassed, 12); assert.deepEqual(quizScore(r, 3), { right: 3, total: 3 });
});
t("stars: a passed old record keeps all stars after a wrong re-check", () => {
  const r = { quizPassed: 5 };
  assert.deepEqual(recordQuizResults(r, [false, true]), { right: 2, total: 2 });
});

console.log(`test_leanlines: ${n} groups passed`);
