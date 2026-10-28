#!/usr/bin/env node
// Validate site/nodes/*.md against schema + decls.json, then build site/dist/.
//   node tools/build_site.mjs          # validate + build
//   node tools/build_site.mjs --check  # validate only (CI on PRs)
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import yaml from "js-yaml";
import { marked } from "marked";
import Ajv2020 from "ajv/dist/2020.js";
import { buildSource, sourceFiles, locateSnippet } from "./build_source.mjs";
import { linkSourceRefs } from "./srcrefs.mjs";

const SITE = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const REPO_ROOT = path.dirname(SITE);
const SRC_FILES = sourceFiles(REPO_ROOT);
const fileLines = new Map(); // repo-relative .lean path -> its lines (for checking ranges / locating snippets)
const linesOf = (f) => { if (!fileLines.has(f)) fileLines.set(f, fs.readFileSync(path.join(REPO_ROOT, f), "utf8").split("\n")); return fileLines.get(f); };
const checkOnly = process.argv.includes("--check");
const decls = JSON.parse(fs.readFileSync(path.join(SITE, "data/decls.json"), "utf8"));
const byId = new Map(decls.map((d) => [d.id, d]));
const schema = JSON.parse(fs.readFileSync(path.join(SITE, "schema/node.schema.json"), "utf8"));
const validate = new Ajv2020({ allErrors: true, strict: false }).compile(schema);

const errors = [];
const warnings0 = [];
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const err = (file, msg) => errors.push(`${file}: ${msg}`);
const nodes = {};

for (const f of fs.readdirSync(path.join(SITE, "nodes")).filter((f) => f.endsWith(".md")).sort()) {
  const src = fs.readFileSync(path.join(SITE, "nodes", f), "utf8");
  const m = src.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!m) { err(f, "missing YAML frontmatter delimited by '---' lines"); continue; }
  let fm;
  try { fm = yaml.load(m[1]); } catch (e) { err(f, "YAML: " + e.message); continue; }
  const body = m[2];
  if (!validate(fm)) {
    for (const e of validate.errors) err(f, `schema ${e.instancePath || "/"} ${e.message}`);
    continue;
  }
  if (fm.id + ".md" !== f) err(f, `id '${fm.id}' must match the file name`);
  if (!byId.has(fm.id)) err(f, `id '${fm.id}' is not a declaration in data/decls.json`);
  if (!/^## Plain English\s*$/m.test(body)) err(f, "body needs a '## Plain English' section");
  fm.quiz.forEach((q, i) => {
    const where = `quiz[${i}]`;
    if (q.type === "choice") {
      if (!Array.isArray(q.choices)) err(f, `${where}: choice question needs 'choices'`);
      else if (!Number.isInteger(q.answer) || q.answer < 0 || q.answer >= q.choices.length)
        err(f, `${where}: answer must be a valid 0-based index into choices`);
    } else if (q.type === "number") {
      if (typeof q.answer !== "number") err(f, `${where}: number question needs a numeric answer`);
    } else if (q.type === "text") {
      if (!Array.isArray(q.answer)) err(f, `${where}: text question needs a list of accepted answers`);
    }
  });
  // "Main.lean lines 9-28" and `Height.lean` in node text become links to the rendered source (src/…).
  const srcErr = (m) => err(f, m);
  const L = (h) => linkSourceRefs(h, SRC_FILES, linesOf, srcErr);
  const md = (s) => L(marked.parse(s));
  const mdInline = (s) => L(marked.parseInline(s));
  // Walkthrough widgets: link the title's "(File.lean, lines a-b)" and locate each step's Lean in it.
  const d0 = byId.get(fm.id);
  for (const w of fm.widgets || []) {
    if (w.title) w.titleHtml = L(esc(w.title));
    if (w.type !== "walkthrough" || !d0) continue;
    const m = (w.title || "").match(/((?:[\w-]+\/)*[A-Za-z]\w*\.lean),?\s+lines?\s+(\d+)\s*[-–]\s*(\d+)/);
    // Prefer the node's own file when the name matches it (several projects share names like Final.lean).
    const file = !m ? d0.file : d0.file.endsWith("/" + m[1]) ? d0.file : SRC_FILES.find((x) => x.endsWith("/" + m[1]) || x === m[1]);
    const [from, to] = m ? [+m[2], +m[3]] : [d0.line, d0.endLine];
    for (const [k, st] of (w.config?.steps || []).entries()) {
      if (!st.lean || !file) continue;
      const loc = locateSnippet(linesOf(file), st.lean, from, to);
      if (loc) st.src = { file, ...loc };
      if (!loc || loc.approx) warnings0.push(`${f}: walkthrough step ${k + 1}: its Lean is not verbatim in ${file} lines ${from}-${to}; ${loc ? `linked to its nearest line, ${loc.line}` : "no source link"}`);
    }
  }
  nodes[fm.id] = {
    ...fm,
    summaryHtml: mdInline(fm.summary),
    bodyHtml: md(body),
    caveatsHtml: (fm.caveats || []).map(mdInline),
    quiz: fm.quiz.map((q) => ({
      ...q,
      qHtml: md(q.q),
      choicesHtml: q.choices ? q.choices.map(mdInline) : undefined,
      explainHtml: md(q.explain),
    })),
  };
}

// Every explained node's meaning-dependencies should be explained too, otherwise
// the reader can never mark it "understood". Warn (not fail) so stubs can land first.
const warnings = [...warnings0];
for (const id of Object.keys(nodes)) {
  for (const dep of byId.get(id)?.meaningDeps || [])
    if (!nodes[dep]) warnings.push(`${id}.md: meaning-dependency '${dep}' has no explainer yet`);
}

for (const w of warnings) console.warn("warning:", w);
if (errors.length) {
  for (const e of errors) console.error("error:", e);
  console.error(`\n${errors.length} error(s). See CONTRIBUTING.md for the node format.`);
  process.exit(1);
}
console.log(`ok: ${Object.keys(nodes).length} explainer nodes, ${decls.length} declarations`);
if (checkOnly) process.exit(0);

// ---- build dist/ ----
const DIST = path.join(SITE, "dist");
fs.rmSync(DIST, { recursive: true, force: true });
fs.mkdirSync(path.join(DIST, "data"), { recursive: true });
fs.cpSync(path.join(SITE, "assets"), path.join(DIST, "assets"), { recursive: true });
fs.copyFileSync(path.join(SITE, "index.html"), path.join(DIST, "index.html"));
fs.copyFileSync(path.join(SITE, "data/decls.json"), path.join(DIST, "data/decls.json"));
// Proof view data, generated and checked by tools/build_proof_steps.mjs (committed so the site build needs no Lean).
if (fs.existsSync(path.join(SITE, "data/proofs.json"))) fs.copyFileSync(path.join(SITE, "data/proofs.json"), path.join(DIST, "data/proofs.json"));
fs.writeFileSync(path.join(DIST, "data/nodes.json"), JSON.stringify(nodes));
// Free-standing pages (review, trust, about): site/pages/<key>.md -> data/pages.json, with Lean file refs linked.
const pages = {};
for (const f of fs.existsSync(path.join(SITE, "pages")) ? fs.readdirSync(path.join(SITE, "pages")).filter((f) => f.endsWith(".md")) : []) {
  const html = linkSourceRefs(marked.parse(fs.readFileSync(path.join(SITE, "pages", f), "utf8")), SRC_FILES, linesOf, (m) => { console.error("error:", f, m); process.exitCode = 1; });
  pages[f.slice(0, -3)] = { html };
}
fs.writeFileSync(path.join(DIST, "data/pages.json"), JSON.stringify(pages));
// Machine-readable work list for agents.
const reachable = decls.filter((d) => d.depth !== null);
const todo = reachable
  .filter((d) => !nodes[d.id])
  .map((d) => ({ id: d.id, kind: d.kind, depth: d.depth, file: d.file, line: d.line,
    meaningDeps: d.meaningDeps, explainedDeps: d.meaningDeps.filter((x) => nodes[x]).length }))
  .sort((a, b) => a.depth - b.depth || a.id.localeCompare(b.id));
fs.writeFileSync(path.join(DIST, "data/needs-explainer.json"), JSON.stringify(todo, null, 1));
fs.copyFileSync(path.join(SITE, "schema/node.schema.json"), path.join(DIST, "data/node.schema.json"));
fs.writeFileSync(path.join(DIST, ".nojekyll"), "");
// Browsable source: dist/src/<path>.lean.html (see tools/build_source.mjs).
const xrefPath = path.join(SITE, "data/xref.json");
const xref = fs.existsSync(xrefPath) ? JSON.parse(fs.readFileSync(xrefPath, "utf8")) : null;
if (!xref) console.warn("warning: data/xref.json missing; source pages will have no identifier links (run tools/build_xref.py)");
const src = buildSource({ repo: REPO_ROOT, dist: DIST, decls, nodes, xref });
for (const w of src.warnings) console.warn("warning:", w);
console.log(`source: ${src.stats.files} files, ${src.stats.linked} identifier links (${src.stats.local} to this project, ${src.stats.external} to Mathlib docs)`);
console.log(`built ${DIST}`);
