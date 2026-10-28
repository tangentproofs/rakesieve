#!/usr/bin/env node
// Tests for the shared progress model (assets/progress.js): the three green states, the v1 → v2
// migration, recursive "understood", and colour contrast.   node tools/test_progress.mjs
import assert from "node:assert/strict";
import { migrateProgress, emptyProgress, ownStatus, makeUnderstood, STATUS_ORDER, STATUS_LABEL, COLORS, contrast, PROGRESS_VERSION } from "../assets/progress.js";

let n = 0;
const t = (name, fn) => { try { fn(); n++; } catch (e) { console.error(`FAIL ${name}:`, e.message); process.exit(1); } };

t("three own states", () => {
  assert.equal(ownStatus({ signedOff: 1, quizPassed: 2 }, true), "both");
  assert.equal(ownStatus({ quizPassed: 2 }, true), "quiz");
  assert.equal(ownStatus({ signedOff: 1 }, true), "signed");
  assert.equal(ownStatus({ viewed: 1 }, true), "explained");
  assert.equal(ownStatus(undefined, true), "explained");
  assert.equal(ownStatus({ signedOff: 1, quizPassed: 1 }, false), "stub");
});

t("v1 sign-offs migrate to both", () => {
  const p = migrateProgress({ v: 1, nodes: { a: { signedOff: 5 }, b: { quizPassed: 3 }, c: { signedOff: 7, quizPassed: 4 }, d: { viewed: 1 } } });
  assert.equal(p.v, PROGRESS_VERSION);
  assert.deepEqual(p.nodes.a, { signedOff: 5, quizPassed: 5 });
  assert.equal(ownStatus(p.nodes.a, true), "both");
  assert.equal(ownStatus(p.nodes.b, true), "quiz");
  assert.deepEqual(p.nodes.c, { signedOff: 7, quizPassed: 4 }, "existing quiz time kept");
  assert.deepEqual(p.nodes.d, { viewed: 1 });
});
t("missing version counts as v1", () => {
  assert.equal(ownStatus(migrateProgress({ nodes: { a: { signedOff: 1 } } }).nodes.a, true), "both");
});
t("v2 sign-off without quiz stays light", () => {
  const p = migrateProgress({ v: 2, nodes: { a: { signedOff: 5 } } });
  assert.deepEqual(p.nodes.a, { signedOff: 5 });
  assert.equal(ownStatus(p.nodes.a, true), "signed");
  assert.deepEqual(migrateProgress(p).nodes.a, { signedOff: 5 }, "idempotent");
});
t("garbage → empty", () => {
  for (const x of [null, undefined, 3, "x", [], {}, { nodes: [] }, { nodes: null }]) assert.deepEqual(migrateProgress(x), emptyProgress());
  assert.deepEqual(migrateProgress({ v: 1, nodes: { a: null, b: 4 } }).nodes, { a: null, b: 4 });
});

t("understood is recursive over mentions, requires sign-off, survives cycles", () => {
  const deps = { a: ["b"], b: ["c"], c: [], x: ["y"], y: ["x"] };
  const signed = new Set(["a", "b", "x", "y"]);
  const u = makeUnderstood((id) => signed.has(id), (id) => deps[id]);
  assert.equal(u("c"), false); assert.equal(u("b"), false); assert.equal(u("a"), false);
  signed.add("c"); u.clear();
  assert.equal(u("a"), true);
  assert.equal(u("x"), false, "a pure cycle never bottoms out");
});

t("labels and colours cover every state; greens are distinct", () => {
  for (const s of STATUS_ORDER) { assert.ok(STATUS_LABEL[s], s); assert.match(COLORS[s], /^#[0-9a-f]{6}$/i, s); }
  const g = [COLORS.signed, COLORS.quiz, COLORS.both];
  assert.equal(new Set(g).size, 3);
  // lightest → darkest, with a visible step between neighbours
  assert.ok(contrast(COLORS.signed, COLORS.quiz) >= 1.3, "signed vs quiz too similar");
  assert.ok(contrast(COLORS.quiz, COLORS.both) >= 1.5, "quiz vs both too similar");
});
t("contrast: dark pill text and dark backgrounds", () => {
  for (const s of ["both", "quiz", "signed"]) {
    assert.ok(contrast(COLORS[s], "#111111") >= 4.5, `${s}: #111 text on fill`);
    for (const bg of ["#1e1f1c", "#272822", "#2f302a"]) assert.ok(contrast(COLORS[s], bg) >= 4.5, `${s} on ${bg}`);
  }
  assert.ok(contrast(COLORS.both, COLORS.explained) >= 1.3, "both vs explained-blue");
});

console.log(`test_progress: ${n} groups passed`);
