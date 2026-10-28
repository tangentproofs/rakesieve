#!/usr/bin/env node
// The "what the theorem says" set is computed from statement mentions only.   node tools/test_statement.mjs
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { statementSet } from "../assets/statement.js";

const SITE = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
let n = 0;
const t = (name, fn) => { try { fn(); n++; } catch (e) { console.error(`FAIL ${name}:`, e.message); process.exit(1); } };
const mk = (o) => new Map(Object.entries(o).map(([id, v]) => [id, { id, meaningDeps: [], proofDeps: [], mathlib: [], ...v }]));

t("synthetic: proof-only edges are ignored, order is dependency-first", () => {
  const g = mk({
    thm: { meaningDeps: ["P"], proofDeps: ["lemma1", "Q"], mathlib: ["Finite"] },
    P: { meaningDeps: ["Q", "R"], mathlib: ["Set"] },
    Q: { meaningDeps: ["R"] },
    R: {},
    lemma1: { meaningDeps: ["S"] }, S: {},
  });
  const s = statementSet(g, ["thm"]);
  assert.deepEqual(s.defs, ["R", "Q", "P"]);
  assert.ok(!s.defs.includes("lemma1") && !s.defs.includes("S"), "proof deps leaked");
  assert.deepEqual(s.mathlib, ["Finite", "Set"]);
});
t("synthetic: cycles and unknown ids terminate", () => {
  const g = mk({ h: { meaningDeps: ["a", "zzz"] }, a: { meaningDeps: ["b"] }, b: { meaningDeps: ["a"] } });
  assert.deepEqual(statementSet(g, ["h"]).defs.sort(), ["a", "b"]);
});

const decls = JSON.parse(fs.readFileSync(path.join(SITE, "data/decls.json"), "utf8"));
const byId = new Map(decls.map((d) => [d.id, d]));
const HEADS = JSON.parse(fs.readFileSync(path.join(SITE, "assets/app.js"), "utf8").match(/const HEADLINES = (\[[^\]]*\]);/)[1]);
t("real data: equals the meaning-edge closure of the headlines", () => {
  const { defs } = statementSet(byId, HEADS);
  const seen = new Set(), st = [...HEADS];
  while (st.length) for (const x of byId.get(st.pop()).meaningDeps) if (!seen.has(x)) { seen.add(x); st.push(x); }
  for (const h of HEADS) seen.delete(h);
  assert.deepEqual([...defs].sort(), [...seen].sort());
  assert.ok(defs.length > 0);
  for (const [i, id] of defs.entries()) for (const x of byId.get(id).meaningDeps)
    if (!HEADS.includes(x)) assert.ok(defs.indexOf(x) < i, `${x} should come before ${id}`);
});
t("real data: proof-only dependencies of the headlines are excluded", () => {
  const { defs } = statementSet(byId, HEADS);
  const proofOnly = HEADS.flatMap((h) => byId.get(h).proofDeps).filter((x) => !defs.includes(x));
  assert.ok(proofOnly.length > 0, "expected the headline proofs to use something outside the statement");
  for (const x of proofOnly) assert.ok(!defs.includes(x));
});

console.log(`test_statement: ${n} groups passed`);
