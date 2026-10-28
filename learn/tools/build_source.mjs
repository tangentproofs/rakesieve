// Browsable, highlighted Lean source for the site: dist/src/<path>.lean.html, one page per .lean
// file of the repo (Mathlib is left alone; its names link out to the Mathlib docs).
//
// Same idea as JacobianChallenge's / eulers-gem's scripts/build-source-pages.py (file tree, per-file
// outline, plain-English badge at each declaration), ported to this site's Node build so it shares
// the site's Monokai highlighter (assets/lean.js), nav and styles. Differences:
//   * identifier links come from Lean's own .ilean cross-references (data/xref.json, made by
//     tools/build_xref.py), not a regex guess: project names jump to their definition here, anything
//     else to mathlib4_docs;
//   * #L9-L28 highlights a line range (and #L9 one line); click a line number, shift-click to extend;
//   * each declaration with a node gets a badge linking to its node page, and each node page links
//     back here (two-way).
// Called by tools/build_site.mjs; checked by tools/test_source.mjs.
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { highlight } from "../assets/lean.js";
import { splitHtmlLines, indentOf } from "../assets/leanlines.js";
import { sourceUrl, githubSourceUrl, anchor, REPO } from "../assets/source.js";

const NSES = []; // rakesieve has no project-wide namespace: ids are the Lean names
const SOURCE_ROOTS = ["."]; // the repo root: the .lean files sit at the top level (learn/ and site/ hold no Lean)
const MATHLIB_FIND = (n) => `https://leanprover-community.github.io/mathlib4_docs/find/?pattern=${encodeURIComponent(n)}#doc`;
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const attr = (s) => esc(s).replace(/"/g, "&quot;");
const short = (n) => { for (const [ns, p] of NSES) if (n.startsWith(ns)) return p + n.slice(ns.length); return n; };

/** Repo-relative paths of the .lean files to render, sorted. */
export function sourceFiles(repo) {
  const out = [];
  const walk = (rel) => {
    const abs = path.join(repo, rel);
    if (!fs.existsSync(abs)) return;
    if (fs.statSync(abs).isDirectory()) {
      for (const f of fs.readdirSync(abs).sort()) if (!f.startsWith(".") && !["learn", "site", "node_modules"].includes(f)) walk(rel === "." ? f : path.posix.join(rel, f));
    } else if (rel.endsWith(".lean")) out.push(rel);
  };
  SOURCE_ROOTS.forEach(walk);
  return out.sort();
}

/** Find the lines of `snippet` inside lines [from, to] (1-based, inclusive) of `fileLines`.
 *  Whitespace is normalized (YAML folds multi-line strings into one line), focus dots `·` are
 *  ignored, and up to two source lines the snippet leaves out (e.g. `let : Fintype M := hfin`) may be
 *  skipped. Returns {line, endLine} or null. Used to link walkthrough steps to their exact lines. */
export function locateSnippet(fileLines, snippet, from = 1, to = fileLines.length) {
  const norm = (x) => x.replace(/^\s*(?:·\s*)+/, "").replace(/\s+/g, " ").trim();
  const S = norm(snippet.replace(/\n\s*(?:·\s*)?/g, " "));
  if (!S) return null;
  const L = (k) => norm(fileLines[k - 1] ?? "");
  for (let i = from; i <= Math.min(to, fileLines.length); i++) {
    const li = L(i);
    if (!li) continue;
    if (li.includes(S)) return { line: i, endLine: i };
    if (!S.startsWith(li)) continue;
    let p = li.length, j = i, skipped = 0;
    while (p < S.length && j < Math.min(to, fileLines.length)) {
      j++;
      const lj = L(j);
      if (!lj) continue;
      const rest = S.slice(p).trimStart();
      if (rest.startsWith(lj)) { p = S.length - rest.length + lj.length; skipped = 0; continue; }
      if (lj.startsWith(rest)) { p = S.length; break; }
      if (++skipped > 2) break;
    }
    if (p >= S.length) return { line: i, endLine: j };
  }
  // Not verbatim (the outline paraphrases or the Lean changed): point at the line sharing the longest
  // prefix with the snippet, at least 12 characters, and say it is approximate.
  let best = null, bestLen = 11;
  for (let i = from; i <= Math.min(to, fileLines.length); i++) {
    const li = L(i).replace(/^@/, "");
    let k = 0;
    while (k < li.length && k < S.length && li[k] === S[k]) k++;
    if (k > bestLen) { best = i; bestLen = k; }
  }
  return best ? { line: best, endLine: best, approx: true } : null;
}

export function buildSource({ repo, dist, decls, nodes, xref }) {
  const files = sourceFiles(repo);
  const OUT = path.join(dist, "src");
  fs.mkdirSync(OUT, { recursive: true });
  const warnings = [];
  const X = xref?.files || {};
  const names = xref?.names || [], mods = xref?.mods || [];

  // Where each project declaration lives: FQ name -> {file, line, endLine} (1-based).
  const where = new Map();
  for (const [file, fx] of Object.entries(X)) for (const [ni, l0, l1] of fx.decls) where.set(names[ni], { file, line: l0 + 1, endLine: l1 + 1 });
  const byName = new Map(decls.map((d) => [d.name, d]));
  const declsByFile = new Map();
  for (const d of decls) { if (!declsByFile.has(d.file)) declsByFile.set(d.file, []); declsByFile.get(d.file).push(d); }

  const tree = treeOf(files);
  const stats = { files: files.length, refs: 0, linked: 0, local: 0, external: 0, stale: [] };
  const index = {}; // file -> { lines, decls: [...] } (also written as src/index.json for tools/tests)

  for (const file of files) {
    const text = fs.readFileSync(path.join(repo, file), "utf8");
    const lines = text.split("\n");
    if (lines.length && lines[lines.length - 1] === "") lines.pop();
    const depth = file.split("/").length; // dist/src/<file> -> root is depth+? : src/ + dirs
    const R = "../".repeat(depth); // from dist/src/a/b/F.lean.html: up (dirs + 1 for src/) to dist/
    let fx = X[file];
    if (fx && fx.sha256 !== crypto.createHash("sha256").update(fs.readFileSync(path.join(repo, file))).digest("hex")) {
      warnings.push(`${file}: data/xref.json is stale for this file (rerun python3 site/tools/build_xref.py after lake build); identifier links skipped`);
      stats.stale.push(file);
      fx = null;
    }
    // UTF-16 offset of each line start (JS string indices are UTF-16, like the .ilean columns).
    const starts = [0];
    for (let i = 0; i < text.length; i++) if (text[i] === "\n") starts.push(i + 1);
    const refAtOffset = new Map(); // offset -> [{e, href, title, cls}]
    for (const [l0, c0, c1, ni, mi] of fx?.refs || []) {
      stats.refs++;
      const n = names[ni], m = mods[mi];
      const s = starts[l0] + c0, e = starts[l0] + c1;
      let href, title, cls;
      const w = where.get(n);
      if (w) {
        href = sourceUrl(w.file, w.line, w.endLine, R);
        if (w.file === file) href = anchor(w.line, w.endLine);
        title = `${short(n)} (${w.file.split("/").pop()} line ${w.line})`; cls = "ref"; stats.local++;
      } else if (/^(Mathlib|Init|Std|Batteries|Lean|Aesop|Qq|Plausible|ImportGraph|LeanSearchClient)\b/.test(m)) {
        href = MATHLIB_FIND(n); title = `${n} — Mathlib docs (${m})`; cls = "ext"; stats.external++;
      } else continue;
      if (!refAtOffset.has(s)) refAtOffset.set(s, []);
      refAtOffset.get(s).push({ e, href, title, cls });
    }
    const refAt = (i, tok, plain) => {
      let out = "", pos = i, any = false;
      for (let k = i; k < i + tok.length; k++) {
        const rs = refAtOffset.get(k);
        if (!rs) continue;
        const r = rs[0];
        const e = Math.min(r.e, i + tok.length);
        if (e <= k) continue;
        if (k > pos) out += plain(tok.slice(pos - i, k - i));
        const ext = r.cls === "ext" ? ` target="_blank" rel="noopener"` : "";
        out += `<a class="${r.cls}" href="${attr(r.href)}" title="${attr(r.title)}"${ext}>${plain(tok.slice(k - i, e - i))}</a>`;
        pos = e; k = e - 1; any = true; stats.linked++;
      }
      if (!any) return null;
      if (pos < i + tok.length) out += plain(tok.slice(pos - i));
      return out;
    };
    const html = splitHtmlLines(highlight(lines.join("\n"), new Map(), undefined, refAt));

    // Declarations in this file: outline (from xref, else from decls.json) and node badges.
    const here = (declsByFile.get(file) || []).slice().sort((a, b) => a.line - b.line);
    const badges = new Map();
    for (const d of here) {
      const n = nodes[d.id];
      const b = `<a class="nb${n ? " explained" : ""}" href="${R}index.html#/node/${encodeURIComponent(d.id)}" data-node="${attr(d.id)}" title="${attr(n ? `Plain English and quiz for ${d.id}` : `Node page for ${d.id} (no explainer yet)`)}">${n ? "¶ plain English" : "¶ node"}</a>`;
      badges.set(d.line, (badges.get(d.line) || "") + b);
    }
    const outline = fx
      ? fx.decls.map(([ni, l0, l1]) => ({ name: names[ni], line: l0 + 1, endLine: l1 + 1 }))
          .filter((o) => byName.has(o.name) || (lines[o.line - 1] || "").includes(o.name.split(".").pop()))
      : here.map((d) => ({ name: d.name, line: d.line, endLine: d.endLine }));
    const outlineRows = outline.map((o) => {
      const d = byName.get(o.name);
      const kind = d?.kind || (lines[o.line - 1].match(/\b(theorem|lemma|def|abbrev|instance|structure|class|inductive)\b/) || [, ""])[1];
      return `<li><a href="${anchor(o.line, o.endLine)}" title="${attr(short(o.name))}"><span class="k">${esc(kind)}</span>${esc(short(o.name).split(".").pop())}</a>${d ? `<a class="nb-mini${nodes[d.id] ? " explained" : ""}" href="${R}index.html#/node/${encodeURIComponent(d.id)}" title="node page">¶</a>` : ""}</li>`;
    }).join("");
    index[file] = { lines: lines.length, decls: here.map((d) => [d.id, d.line, d.endLine]) };

    const body = html.map((h, k) => {
      const n = k + 1;
      const ind = indentOf(lines[k] ?? "");
      const code = h.replace(/^((?:<[^>]+>)*) +/, "$1") || "&#8203;";
      return `<div class="sl" id="L${n}"><a class="n" href="${anchor(n)}" data-n="${n}" aria-label="line ${n}"></a><span class="c" style="--i:${ind}">${code}</span>${badges.get(n) || ""}</div>`;
    }).join("\n");
    const dir = file.split("/").slice(0, -1).join("/");
    const base = file.split("/").pop();
    const pageDecls = outline.map((o) => {
      const d = byName.get(o.name);
      return [short(o.name), o.line, o.endLine, d ? d.id : null, d && nodes[d.id] ? 1 : 0];
    });
    const page = layout({
      R, title: `${base} · source`, current: file,
      tree: renderTree(tree, "", file, R),
      outline: outlineRows ? `<div class="src-outline"><div class="h">In this file (${outline.length})</div><ul>${outlineRows}</ul></div>` : "",
      main: `
    <div class="src-head">
      <code class="path">${dir ? `<span class="dir">${esc(dir)}/</span>` : ""}<b>${esc(base)}</b></code>
      <span class="muted small">${lines.length} lines · ${here.length} declaration${here.length === 1 ? "" : "s"} on the site</span>
      <span class="grow"></span>
      <a class="gh small" id="gh" href="${attr(githubSourceUrl(file))}" target="_blank" rel="noopener">view on GitHub ↗</a>
    </div>
    <div class="src-range" id="range" hidden></div>
    <div class="src-code lean" id="code">
${body}
    </div>`,
      script: `<script>window.SRC = ${JSON.stringify({ file, github: githubSourceUrl(file), root: R, decls: pageDecls })};</script>\n<script src="${R}src/source.js"></script>`,
    });
    const out = path.join(OUT, file + ".html");
    fs.mkdirSync(path.dirname(out), { recursive: true });
    fs.writeFileSync(out, page);
  }

  // Index page: every file, with how many of its declarations have explainers.
  const rows = files.map((f) => {
    const ds = declsByFile.get(f) || [];
    const ex = ds.filter((d) => nodes[d.id]).length;
    return `<tr><td><a href="${attr(f)}.html">${esc(f)}</a>${/^(Results|RakeSieve|PrimeSieve)\.lean$/.test(f) ? ` <span class="pill kind-theorem">headline</span>` : ""}</td><td>${index[f].lines}</td><td>${ds.length}</td><td>${ex || ""}</td></tr>`;
  }).join("");
  fs.writeFileSync(path.join(OUT, "index.html"), layout({
    R: "../", title: "Source", current: null, tree: renderTree(tree, "", null, "../"), outline: "",
    main: `
    <h1>The Lean source</h1>
    <p class="muted">All ${files.length} Lean files in <a href="https://github.com/${REPO}" target="_blank" rel="noopener">${REPO}</a>, highlighted and cross-linked.
    Names defined in this project jump to their definition here; a hand-checked list of Mathlib and core names opens the
    <a href="https://leanprover-community.github.io/mathlib4_docs/" target="_blank" rel="noopener">Mathlib docs</a>.
    A <span class="nb explained" style="float:none">¶ plain English</span> badge next to a declaration opens its node page; every node page links back to its lines here.
    Click a line number to link to it, and shift-click to select a range.</p>
    <p>Start with <a href="Results.lean.html"><code>Results.lean</code></a> (the five headline theorems), then <a href="PrimeSieve.lean.html"><code>PrimeSieve.lean</code></a> (why any sieve gives the next prime) and <a href="RakeSieve.lean.html"><code>RakeSieve.lean</code></a> (the rake-based sieve). <code>Rake_gte.lean</code> and <code>OldMain.lean</code> are not part of the Lean build (they are not listed in <code>lakefile.lean</code>); <code>Rake_gte.lean</code> contains three <code>sorry</code>s. Identifier links are matched from the source text (no Lean build), so a few may be missing; see the Trust page.</p>
    <table class="node-list"><thead><tr><th>file</th><th>lines</th><th>declarations</th><th>explained</th></tr></thead><tbody>${rows}</tbody></table>`,
    script: "",
  }));
  fs.writeFileSync(path.join(OUT, "source.css"), SOURCE_CSS);
  fs.writeFileSync(path.join(OUT, "source.js"), SOURCE_JS);
  fs.writeFileSync(path.join(OUT, "index.json"), JSON.stringify(index));
  return { stats, warnings, files, index };
}

function treeOf(files) {
  const root = {};
  for (const f of files) {
    const parts = f.split("/");
    let cur = root;
    for (const p of parts.slice(0, -1)) cur = cur[p] ??= {};
    cur[parts.at(-1)] = null;
  }
  return root;
}
function renderTree(node, prefix, current, R) {
  const ents = Object.entries(node).sort(([a, x], [b, y]) => ((x === null) - (y === null)) || a.localeCompare(b));
  return `<ul>${ents.map(([k, v]) => {
    const p = prefix + k;
    if (v === null) return `<li><a href="${attr(sourceUrl(p, null, null, R))}"${p === current ? ' class="current" aria-current="page"' : ""}>${esc(k.replace(/\.lean$/, ""))}</a></li>`;
    const open = !current || current.startsWith(p + "/");
    // On a file page, folders off the current file's path are not expanded (1,000+ files would make
    // every page carry the whole tree); they link to the full list on src/index.html instead.
    if (current && !open) return `<li class="dir"><a href="${attr(R)}src/index.html">${esc(k)}/</a></li>`;
    return `<li class="dir"><details${open ? " open" : ""}><summary>${esc(k)}</summary>${renderTree(v, p + "/", current, R)}</details></li>`;
  }).join("")}</ul>`;
}

function layout({ R, title, current, tree, outline, main, script }) {
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)} · RakeSieve, explained</title>
<link rel="stylesheet" href="${R}assets/style.css">
<link rel="stylesheet" href="${R}src/source.css">
</head>
<body class="srcpage">
<header class="top">
  <a class="brand" href="${R}index.html#/">rake<span>sieve</span> <em>explained</em></a>
  <nav>
    <a href="${R}index.html#/start">Start here</a>
    <a href="${R}index.html#/">Proof graph</a>
    <a href="${R}index.html#/nodes">Nodes</a>
    <a href="${R}src/index.html" class="on">Source</a>
    <a href="${R}index.html#/review">Review</a>
    <a href="${R}index.html#/trust">Trust</a>
    <a href="${R}index.html#/about">About</a>
    <a href="https://github.com/${REPO}" target="_blank" rel="noopener">GitHub</a>
  </nav>
</header>
<div class="src-layout">
  <aside class="src-side">
    <details class="src-files" open><summary>Files</summary><nav class="src-tree">${tree}</nav></details>
    ${outline}
  </aside>
  <main class="src-main">${main}
  </main>
</div>
<footer>
  The Lean library is by Michal Wallace, tangentstorm (<a href="https://github.com/tangentproofs/rakesieve">tangentproofs/rakesieve</a>).
  This is the verbatim Lean; the plain-English pages are community-written and may be wrong.
</footer>
${script}
</body>
</html>
`;
}

const SOURCE_CSS = `/* Browsable source pages (tools/build_source.mjs). Shares assets/style.css (Monokai, header, footer). */
body.srcpage main.src-main { max-width: none; margin: 0; padding: .8rem 1.4rem 2rem; min-width: 0; }
.src-layout { display: grid; grid-template-columns: 280px minmax(0, 1fr); min-height: calc(100vh - 3rem); }
.src-side { border-right: 1px solid var(--line); background: var(--panel); position: sticky; top: var(--hdr, 3rem); align-self: start;
  max-height: calc(100vh - var(--hdr, 3rem)); overflow-y: auto; padding: .6rem .8rem 1.5rem; font-size: .85rem; }
.src-side summary { cursor: pointer; color: var(--dim); text-transform: uppercase; letter-spacing: .05em; font-size: .72rem; font-weight: 600; }
.src-tree ul { list-style: none; margin: 0; padding-left: .8rem; } .src-tree > ul { padding-left: 0; }
.src-tree li { margin: 1px 0; } .src-tree li.dir summary { text-transform: none; letter-spacing: 0; font-size: .85rem; color: var(--fg); font-weight: 600; }
.src-tree a { color: var(--fg); display: block; padding: 0 .3rem; border-radius: 3px; } .src-tree a:hover { background: var(--panel2); text-decoration: none; }
.src-tree a.current { background: var(--pink); color: #111; font-weight: 600; }
.src-outline { margin-top: .8rem; border-top: 1px solid var(--line); padding-top: .6rem; }
.src-outline .h { color: var(--dim); text-transform: uppercase; letter-spacing: .05em; font-size: .72rem; font-weight: 600; margin-bottom: .3rem; }
.src-outline ul { list-style: none; margin: 0; padding: 0; }
.src-outline li { display: flex; align-items: baseline; gap: .3rem; }
.src-outline li > a:first-child { flex: 1; min-width: 0; color: var(--fg); font-family: "JetBrains Mono", ui-monospace, Menlo, monospace; font-size: .8rem;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap; padding: 0 .2rem; border-radius: 3px; }
.src-outline li > a:first-child:hover { background: var(--panel2); text-decoration: none; }
.src-outline li.on > a:first-child { background: #3e3d32; color: var(--yellow); }
.src-outline .k { color: var(--dim); font-size: .7rem; margin-right: .4em; }
.nb-mini { color: var(--unread); font-weight: 700; } .nb-mini.explained { color: var(--green); }
.src-main h1 { margin-top: .4rem; }
.src-head { display: flex; flex-wrap: wrap; align-items: baseline; gap: .4rem 1rem; margin-bottom: .6rem; }
.src-head .path { background: none; padding: 0; font-size: 1rem; } .src-head .path .dir { color: var(--dim); } .src-head .grow { flex: 1; }
.src-range { position: sticky; top: var(--hdr, 3rem); z-index: 5; display: flex; flex-wrap: wrap; align-items: baseline; gap: .3rem .9rem;
  background: #3a3520; border: 1px solid var(--yellow); border-radius: 6px; padding: .35rem .8rem; margin-bottom: .6rem; font-size: .9rem; }
.src-range b { color: var(--yellow); } .src-range code { background: none; } .src-range .grow { flex: 1; }
.src-range button { padding: 0 .5rem; font-size: .8rem; }
.src-code { background: var(--panel); border: 1px solid var(--line); border-left: 3px solid var(--pink); border-radius: 6px; padding: .5rem 0;
  font-family: "JetBrains Mono", "Fira Code", ui-monospace, Menlo, Consolas, monospace; font-size: .86rem; line-height: 1.5; }
.sl { display: flex; align-items: flex-start; scroll-margin-top: calc(var(--hdr, 3rem) + 3.2rem); padding-right: .6rem; }
.sl > .n { flex: none; width: 4.2em; text-align: right; padding-right: .9em; color: var(--unread); user-select: none; -webkit-user-select: none; }
.sl > .n::before { content: attr(data-n); } .sl > .n:hover { color: var(--fg); text-decoration: none; }
.sl > .c { flex: 1; min-width: 0; white-space: pre-wrap; overflow-wrap: anywhere; padding-left: calc((var(--i, 0) + 4) * 1ch + .6rem); text-indent: -4ch; }
.sl.hl { background: #3a3520; } .sl.hl > .n { color: var(--yellow); border-right: 3px solid var(--yellow); }
.sl.hl-first { box-shadow: inset 0 1px 0 #6b6230; } .sl.hl-last { box-shadow: inset 0 -1px 0 #6b6230; } .sl.hl-first.hl-last { box-shadow: inset 0 1px 0 #6b6230, inset 0 -1px 0 #6b6230; }
.sl:target:not(.hl) { background: #3a3520; }
.src-code a.ref { color: var(--green); border-bottom: 1px dotted #5f7f24; } .src-code a.ref:hover { background: #3a4a20; text-decoration: none; }
.src-code a.ext { color: inherit; border-bottom: 1px dotted #4f6f7a; } .src-code a.ext:hover { color: var(--blue); border-bottom-color: var(--blue); text-decoration: none; }
.src-code a .ty, .src-code a .kw { color: inherit; }
.nb { float: right; flex: none; margin-left: .6rem; font-family: system-ui, sans-serif; font-size: .72rem; line-height: 1.5; padding: 0 .5em; border-radius: 999px;
  border: 1px solid var(--line); color: var(--dim); user-select: none; -webkit-user-select: none; white-space: nowrap; align-self: center; }
.nb.explained { border-color: var(--green); color: var(--green); } .nb:hover { background: var(--panel2); text-decoration: none; }
@media (max-width: 800px) {
  .src-layout { grid-template-columns: 1fr; }
  .src-side { position: static; max-height: none; border-right: 0; border-bottom: 1px solid var(--line); }
  .src-side .src-files:not([open]) + .src-outline { display: none; }
  body.srcpage main.src-main { padding: .6rem .6rem 2rem; }
  body.srcpage header.top { position: static; }
  .sl > .n { width: 3em; padding-right: .5em; }
  .src-code { font-size: .78rem; }
  .nb { font-size: .66rem; }
}
`;

const SOURCE_JS = `// Line-range highlighting for the source pages: #L9 or #L9-L28. Click a line number to select it,
// shift-click to extend. The range bar names the declaration and links to its node page and GitHub.
(function () {
  "use strict";
  var S = window.SRC || {}, anchor = null;
  var hdr = document.querySelector("header.top");
  function setHdr() { var st = hdr && getComputedStyle(hdr).position === "sticky"; document.documentElement.style.setProperty("--hdr", (st ? hdr.offsetHeight : 0) + "px"); }
  setHdr(); addEventListener("resize", setHdr);
  if (window.matchMedia("(max-width: 800px)").matches) {
    var f = document.querySelector(".src-files"); if (f && S.file) f.open = false;
  }
  function parse(h) {
    var m = /^#L(\\d+)(?:-L(\\d+))?$/.exec(h || "");
    if (!m) return null;
    var a = +m[1], b = m[2] ? +m[2] : a;
    return a <= b ? [a, b] : [b, a];
  }
  function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }
  function apply(scroll) {
    document.querySelectorAll(".sl.hl").forEach(function (e) { e.classList.remove("hl", "hl-first", "hl-last"); });
    document.querySelectorAll(".src-outline li.on").forEach(function (e) { e.classList.remove("on"); });
    var bar = document.getElementById("range"), gh = document.getElementById("gh");
    var r = parse(location.hash);
    if (!r) { if (bar) bar.hidden = true; if (gh) gh.href = S.github; return; }
    for (var i = r[0]; i <= r[1]; i++) {
      var el = document.getElementById("L" + i);
      if (!el) continue;
      el.classList.add("hl");
      if (i === r[0]) el.classList.add("hl-first");
      if (i === r[1]) el.classList.add("hl-last");
    }
    var frag = "#L" + r[0] + (r[1] !== r[0] ? "-L" + r[1] : "");
    if (gh) gh.href = S.github + frag;
    var d = null;
    (S.decls || []).forEach(function (x) { if (!d && x[1] === r[0] && x[2] === r[1]) d = x; });
    if (!d) (S.decls || []).forEach(function (x) { if (!d && x[1] <= r[0] && r[1] <= x[2]) d = x; });
    document.querySelectorAll('.src-outline a[href="#L' + (d ? d[1] + (d[2] !== d[1] ? "-L" + d[2] : "") : "") + '"]').forEach(function (a) { a.parentNode.classList.add("on"); });
    if (bar) {
      var nm = S.file.split("/").pop();
      bar.innerHTML = "<span><b>" + (r[1] !== r[0] ? "Lines " + r[0] + "\\u2013" + r[1] : "Line " + r[0]) + "</b> of <code>" + esc(nm) + "</code></span>" +
        (d ? "<span>" + (d[1] === r[0] && d[2] === r[1] ? "" : "in ") + "<code>" + esc(d[0]) + "</code></span>" +
          (d[3] ? '<a href="' + esc(S.root + "index.html#/node/" + encodeURIComponent(d[3])) + '">' + (d[4] ? "\\u00b6 plain English" : "\\u00b6 node page") + "</a>" : "") : "") +
        '<span class="grow"></span><a class="small" href="' + esc(S.github + frag) + '" target="_blank" rel="noopener">these lines on GitHub \\u2197</a>' +
        '<button type="button" id="clear" title="Clear the highlight">\\u00d7</button>';
      bar.hidden = false;
      document.getElementById("clear").onclick = function () { history.replaceState(null, "", location.pathname + location.search); anchor = null; apply(false); };
    }
    if (scroll) {
      var first = document.getElementById("L" + r[0]);
      if (first) first.scrollIntoView({ block: r[1] - r[0] > 25 ? "start" : "center" });
    }
  }
  document.addEventListener("click", function (ev) {
    var a = ev.target.closest && ev.target.closest(".sl > a.n");
    if (!a) return;
    ev.preventDefault();
    var n = +a.dataset.n, cur = parse(location.hash);
    var h = (ev.shiftKey && (anchor || (cur && cur[0]))) ? "#L" + Math.min(anchor || cur[0], n) + "-L" + Math.max(anchor || cur[0], n) : "#L" + n;
    if (!ev.shiftKey) anchor = n;
    history.replaceState(null, "", h);
    apply(false);
  });
  addEventListener("hashchange", function () { apply(true); });
  apply(true);
})();
`;
