import { highlight, linkMap } from "./lean.js";
import { mountWidget } from "./widgets.js";
import { migrateProgress, emptyProgress, ownStatus, makeUnderstood, STATUS_ORDER, STATUS_LABEL, COLORS, PENDING_COLOR, quizScore, recordQuizResults, starString } from "./progress.js";
import { wrapLeanLines } from "./leanlines.js";
import { statementSet } from "./statement.js";
import { REPO, sourceUrl, githubSourceUrl, sourceLabel } from "./source.js";
import { mountProofView } from "./proofview.js";
// Comments: off until the repo exists with Discussions enabled; then fill in repoId / categoryId (CONVENTIONS §3).
const GISCUS = { repo: REPO, repoId: "", category: "Announcements", categoryId: "" };
const MATHLIB_DOCS = (n) => `https://leanprover-community.github.io/mathlib4_docs/find/?pattern=${encodeURIComponent(n)}#doc`;
const app = document.getElementById("app");
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
// "Main.lean lines 9–28" → the rendered, highlighted lines on this site (src/…), plus a small GitHub link.
const srcLink = (d, cls = "small muted") => `<span class="srclink ${cls}"><a href="${sourceUrl(d.file, d.line, d.endLine)}" title="${esc(d.file)}: open the highlighted source on this site">${esc(sourceLabel(d.file, d.line, d.endLine))}</a>
  <a class="gh" href="${githubSourceUrl(d.file, d.line, d.endLine)}" target="_blank" rel="noopener" title="the same lines on GitHub">GitHub ↗</a></span>`;

const [decls, nodes, proofs, pages] = await Promise.all([
  fetch("data/decls.json").then((r) => r.json()),
  fetch("data/nodes.json").then((r) => r.json()),
  fetch("data/proofs.json").then((r) => (r.ok ? r.json() : {})).catch(() => ({})),
  fetch("data/pages.json").then((r) => (r.ok ? r.json() : {})).catch(() => ({})),
]);
const byId = new Map(decls.map((d) => [d.id, d]));
const reachable = decls.filter((d) => d.depth !== null);

// Headline theorems, and what a reader needs to read their STATEMENTS (statement mentions only,
// transitively, stopping at Mathlib; proof-only dependencies are left out). See assets/statement.js.
// The five theorems of Results.lean, plus the instance that carries the sieve's real correctness guarantee
// (no named theorem in Results.lean states it; see the review). Main first.
const HEADLINES = ["results_exists_prime_gt_of_rakeSieve", "instPrimeGenPrimeSieve", "results_exists_prime_gt_of_primeGen",
  "results_exists_prime_gt_of_simpleGen", "results_three_mem_R_two", "results_three_le_of_mem_R_two"];
const STMT = statementSet(byId, HEADLINES);
const stmtSet = new Set(STMT.defs);
// Short glosses for the Mathlib notions the headline statements use (taken as given, not explained here).
const MATHLIB_GLOSS = {
  "Nat.Prime": "<code>Nat.Prime p</code>: p is a prime natural number (p ≥ 2 and its only divisors are 1 and p).",
  "Nat": "<code>Nat</code> (ℕ): the natural numbers 0, 1, 2, …",
  "Set": "<code>Set Nat</code>: a set of natural numbers, written <code>{ n | … }</code>; <code>n ∈ S</code> is membership.",
  "Nat.exists_infinite_primes": "<code>Nat.exists_infinite_primes n : ∃ p, n ≤ p ∧ Nat.Prime p</code>: Euclid's theorem as Mathlib states it. RakeSieve's proofs use it (see the review).",
  "Nat.find": "<code>Nat.find h</code>: the least n satisfying a decidable property, given a proof <code>h</code> that one exists.",
};

// ------------------------------------------------------------------ progress
// localStorage schema v2 (see assets/progress.js): { v: 2, nodes: { [id]: { viewed?, quizPassed?, signedOff?, answers? } } }.
// The key keeps its old "-v1" name; v1 data is migrated on load and on import.
const KEY = "rakesieve-learn-progress-v1";
let P = (() => { try { return migrateProgress(JSON.parse(localStorage.getItem(KEY))); } catch { return emptyProgress(); } })();
const save = () => localStorage.setItem(KEY, JSON.stringify(P));
const rec = (id) => (P.nodes[id] ??= {});

// signed: the reader ticked "I understand" (no longer gated by the quiz). Stubs have no explainer, so cannot be signed.
const signed = (id) => !!(nodes[id] && P.nodes[id]?.signedOff);
// understood: signed AND every meaning-dependency understood (Mathlib is taken as given).
const understood = makeUnderstood(signed, (id) => byId.get(id)?.meaningDeps);
// status: the node's own state, shown as three greens: signed (lightest), quiz (middle), both (darkest).
const status = (id) => ownStatus(P.nodes[id], !!nodes[id]);
// depsPending: marked understood, but something its statement mentions isn't understood yet.
const depsPending = (id) => signed(id) && !understood(id);
const statusLabel = (id) => STATUS_LABEL[status(id)] + (depsPending(id) ? " · mentions pending" : "");
function refresh() { understood.clear(); }

// The proof is understood when main is, and every declaration its proof uses is too.
function proofCoverage() {
  const n = reachable.filter((d) => understood(d.id)).length;
  return { n, total: reachable.length };
}

// ------------------------------------------------------------------ router
const routes = [
  [/^#?\/?$/, graphPage],
  [/^#\/node\/(.+)$/, (id) => nodePage(decodeURIComponent(id))],
  [/^#\/nodes(?:\?.*)?$/, () => listPage()],
  [/^#\/start$/, startPage],
  [/^#\/review$/, () => mdPage("review")],
  [/^#\/trust$/, () => mdPage("trust")],
  [/^#\/about$/, aboutPage],
];
function route() {
  refresh();
  const hsh = location.hash || "#/";
  app.className = "";
  document.querySelectorAll("header nav a").forEach((a) => a.classList.toggle("on", a.getAttribute("href") === hsh));
  for (const [re, f] of routes) { const m = hsh.match(re); if (m) { f(...m.slice(1)); window.scrollTo(0, 0); return; } }
  app.innerHTML = `<p>Not found. <a href="#/">Home</a></p>`;
}
addEventListener("hashchange", route);

// ------------------------------------------------------------------ graph page
let graphView = "spine";
function graphPage() {
  app.className = "wide";
  const cov = proofCoverage();
  const spine = Object.keys(nodes);
  const spineDone = spine.filter((id) => understood(id)).length;
  app.innerHTML = `
    <div class="graph-wrap">
      <div>
        <h1>RakeSieve: a prime sieve checked in Lean 4</h1>
        <p class="eli5">The main theorem's <i>statement</i> never mentions the sieve. It is word for word Euclid's "there is always a bigger prime", and the proof even calls Mathlib's own proof of Euclid along the way. The real verified content is elsewhere: every state of the sieve carries a proof that its list of arithmetic sequences produces <i>exactly</i> the numbers with no prime factor up to the current prime, so its smallest term is always the next prime. <a href="#/review">Read the review →</a></p>
        <p class="muted">The Lean is by Michal Wallace (tangentstorm). The job here is different: <b>you</b> are the checker.
        A node turns green when you tick <b>I understand</b> (lightest), pass its quiz (middle) or do both (darkest), and it counts as understood once everything its statement mentions is too, just as Lean won't accept a statement whose ingredients it doesn't know.</p>
        <p><a class="start-link" href="#/start">Start here: what the theorem says →</a>
        <span class="small muted">the theorem and the ${STMT.defs.length} definitions you need to read it, before any proof</span></p>
        <div class="toolbar">
          <button data-v="spine">Explained spine (${spine.length})</button>
          <button data-v="neighborhood">Spine + direct deps</button>
          <button data-v="files">Files (${new Set(decls.map((d) => d.module)).size})</button>
          <button data-v="all">All declarations (${decls.length})</button>
          <input id="find" type="text" placeholder="find a declaration…" style="max-width:16rem">
        </div>
        <div id="cy"></div>
        <p class="small muted">Click a node to open it. Solid edge = used in the statement/definition (needed to <i>understand</i> it); dashed = used only in the proof. Arrows point from a declaration to what it uses.</p>
      </div>
      <aside id="side">
        <div class="panel">
          <h3>Your progress</h3>
          <div>Spine: <b>${spineDone}</b> / ${spine.length} understood</div>
          <div class="progress-bar"><div style="width:${(100 * spineDone) / spine.length}%"></div></div>
          <div>Statement-level declarations: <b>${cov.n}</b> / ${cov.total} understood</div>
          <div class="progress-bar"><div style="width:${(100 * cov.n) / cov.total}%"></div></div>
          <p class="small muted">${HEADLINES.map((h) => `<a href="#/node/${encodeURIComponent(h)}">${esc(h)}</a>: ${understood(h) ? "statement understood" : "not yet"}`).join("<br>")}</p>
          <p class="small muted">The whole library is about 1,300 lines of Lean in 8 built files, all rendered on the <a href="src/index.html">Source</a> pages.</p>
        </div>
        <div class="panel legend">
          <h3>Legend</h3>
          ${STATUS_ORDER.map((k) => `<div><span class="sw" style="background:${COLORS[k]}"></span>${STATUS_LABEL[k]}</div>`).join("")}
          <div><span class="sw" style="background:transparent;border:2px dashed ${PENDING_COLOR}"></span>marked understood, a mention isn't yet</div>
          <div><span class="sw" style="background:transparent;border:2px solid #f92672"></span>headline theorem</div>
          <div><span class="sw stmt-ring"></span>needed to read the main statement</div>
        </div>
        <div class="panel small">
          <h3>Start here</h3>
          <p>Read <a href="#/start">what the theorem says</a>: the statement, then the definitions it uses, simplest first.</p>
          <ol>
            ${STMT.defs.map((id) => `<li><a href="#/node/${encodeURIComponent(id)}">${esc(id)}</a></li>`).join("")}
            ${HEADLINES.map((id) => `<li><a href="#/node/${encodeURIComponent(id)}">${esc(id)}</a> — the theorem</li>`).join("")}
          </ol>
          <p><a href="#/review">The review: is each statement faithful? →</a></p>
        </div>
        <div class="panel small">
          <h3>Progress file</h3>
          <button id="export">Export</button> <button id="import">Import</button> <button id="reset">Reset</button>
          <p class="muted">Stored only in this browser (localStorage).</p>
        </div>
      </aside>
    </div>`;
  app.querySelectorAll("[data-v]").forEach((b) => {
    b.classList.toggle("on", b.dataset.v === graphView);
    b.onclick = () => { graphView = b.dataset.v; graphPage(); };
  });
  wireProgressButtons();
  drawGraph(graphView);
}

function wireProgressButtons() {
  document.getElementById("export").onclick = () => {
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([JSON.stringify(P, null, 1)], { type: "application/json" }));
    a.download = "rakesieve-progress.json"; a.click();
  };
  document.getElementById("import").onclick = () => {
    const i = document.createElement("input"); i.type = "file"; i.accept = ".json";
    i.onchange = async () => { try { P = migrateProgress(JSON.parse(await i.files[0].text())); save(); route(); } catch (e) { alert("Could not read: " + e.message); } };
    i.click();
  };
  document.getElementById("reset").onclick = () => { if (confirm("Forget all sign-offs and quiz results in this browser?")) { P = emptyProgress(); save(); route(); } };
}

function drawGraph(view) {
  if (!window.cytoscape) { document.getElementById("cy").innerHTML = "<p class='err'>Graph library failed to load.</p>"; return; }
  if (window.cytoscapeDagre && !drawGraph.reg) { cytoscape.use(window.cytoscapeDagre); drawGraph.reg = true; }
  const els = [];
  let ids;
  if (view === "files") {
    const mods = [...new Set(decls.map((d) => d.module))];
    const modOf = new Map(decls.map((d) => [d.id, d.module]));
    const cnt = new Map(), expl = new Map(), und = new Map();
    for (const d of decls) {
      cnt.set(d.module, (cnt.get(d.module) || 0) + 1);
      if (nodes[d.id]) expl.set(d.module, (expl.get(d.module) || 0) + 1);
      if (understood(d.id)) und.set(d.module, (und.get(d.module) || 0) + 1);
    }
    for (const m of mods) {
      const u = und.get(m) || 0, c = cnt.get(m);
      const st = u === c ? "both" : u ? "signed" : expl.get(m) ? "explained" : "stub";
      els.push({ data: { id: "m:" + m, label: `${m}\n${u}/${c}`, color: COLORS[st], size: 20 + Math.sqrt(c) * 6, file: m } });
    }
    const seen = new Set();
    for (const d of decls) for (const [deps, kind] of [[d.meaningDeps, "m"], [d.proofDeps, "p"]]) for (const x of deps) {
      const a = d.module, b = modOf.get(x);
      if (a !== b && !seen.has(a + ">" + b)) { seen.add(a + ">" + b); els.push({ data: { id: `e:${a}>${b}`, source: "m:" + a, target: "m:" + b, kind: "p" } }); }
    }
  } else {
    if (view === "spine") ids = new Set(Object.keys(nodes));
    else if (view === "neighborhood") {
      ids = new Set(Object.keys(nodes));
      for (const id of Object.keys(nodes)) for (const x of [...byId.get(id).meaningDeps, ...byId.get(id).proofDeps]) ids.add(x);
    } else ids = new Set(decls.map((d) => d.id));
    for (const id of ids) {
      const d = byId.get(id), st = status(id);
      els.push({ data: { id, label: id.split(".").pop(), color: COLORS[st], pending: depsPending(id) ? 1 : 0, size: nodes[id] ? 26 : 12, main: HEADLINES.includes(id) ? 1 : 0, stmt: stmtSet.has(id) ? 1 : 0, explained: nodes[id] ? 1 : 0 } });
    }
    for (const id of ids) {
      const d = byId.get(id);
      for (const x of d.meaningDeps) if (ids.has(x)) els.push({ data: { id: `${id}>${x}`, source: id, target: x, kind: "m" } });
      for (const x of d.proofDeps) if (ids.has(x)) els.push({ data: { id: `${id}>>${x}`, source: id, target: x, kind: "p" } });
    }
  }
  const big = els.length > 1500;
  const cy = cytoscape({
    container: document.getElementById("cy"),
    elements: els,
    wheelSensitivity: 0.3,
    style: [
      { selector: "node", style: { "background-color": "data(color)", width: "data(size)", height: "data(size)", label: "data(label)", color: "#f8f8f2", "font-size": view === "all" ? 6 : 10, "text-wrap": "wrap", "text-valign": "bottom", "text-margin-y": 3, "text-outline-color": "#1e1f1c", "text-outline-width": 2 } },
      { selector: "node[explained = 0]", style: { "font-size": view === "all" ? 0 : 7, color: "#a59f85" } },
      { selector: "node[stmt = 1]", style: { "outline-width": 3, "outline-color": "#66d9ef", "outline-offset": 3, "outline-opacity": 1 } },
      { selector: "node[pending = 1]", style: { "border-width": 3, "border-style": "dashed", "border-color": PENDING_COLOR } },
      { selector: "node[main = 1]", style: { "border-width": 3, "border-color": "#f92672", "font-weight": "bold" } },
      { selector: "edge", style: { width: 1.2, "line-color": "#5c5b4f", "target-arrow-color": "#5c5b4f", "target-arrow-shape": "triangle", "arrow-scale": 0.7, "curve-style": big ? "haystack" : "bezier", opacity: 0.8 } },
      { selector: "edge[kind = 'p']", style: { "line-style": "dashed", opacity: 0.45 } },
      { selector: ".hl", style: { "border-width": 4, "border-color": "#fd971f" } },
      { selector: ".faded", style: { opacity: 0.12 } },
    ],
    layout: view === "all" ? { name: "cose", animate: false, nodeRepulsion: 4000, idealEdgeLength: 30, numIter: 600 }
      : { name: window.cytoscapeDagre ? "dagre" : "breadthfirst", rankDir: "TB", nodeSep: 50, rankSep: 60, animate: false },
  });
  cy.on("tap", "node", (e) => {
    const id = e.target.id();
    if (id.startsWith("m:")) { location.hash = "#/nodes?file=" + id.slice(2); return; }
    location.hash = "#/node/" + encodeURIComponent(id);
  });
  cy.on("mouseover", "node", (e) => { const n = e.target; cy.elements().addClass("faded"); n.closedNeighborhood().removeClass("faded"); });
  cy.on("mouseout", "node", () => cy.elements().removeClass("faded"));
  const find = document.getElementById("find");
  find.oninput = () => {
    cy.nodes().removeClass("hl");
    const q = find.value.trim().toLowerCase();
    if (!q) return;
    const hits = cy.nodes().filter((n) => n.id().toLowerCase().includes(q));
    hits.addClass("hl");
    if (hits.length && hits.length < 30) cy.fit(hits, 60);
  };
  find.onkeydown = (e) => {
    if (e.key !== "Enter") return;
    const q = find.value.trim().toLowerCase();
    const d = decls.find((d) => d.id.toLowerCase() === q) || decls.find((d) => d.id.toLowerCase().includes(q));
    if (d) location.hash = "#/node/" + encodeURIComponent(d.id);
  };
}

// ------------------------------------------------------------------ node page
function depLinks(list) {
  if (!list.length) return `<span class="muted small">none in this project</span>`;
  return list.map((id) => `<a class="st-${status(id)}" href="#/node/${encodeURIComponent(id)}" title="${statusLabel(id)}">${esc(id)}</a>`).join("");
}
function agentPrompt(d) {
  return `You are writing an informal explainer for one declaration of the Lean 4 proof in ${REPO}
(RakeSieve: arithmetic sequences, "rakes", and a prime sieve built from them, with a proof that it yields consecutive primes).
The declarations were read from the source text, not a Lean build.

Target: ${d.name}  (${d.kind})
Source: ${githubSourceUrl(d.file, d.line, d.endLine)}
Section variables in scope: ${d.variables.join(" ") || "(none)"}
Formal statement:
${d.statement}

It mentions these project declarations (explain them by name, link to them): ${d.meaningDeps.join(", ") || "none"}
Its proof uses: ${d.proofDeps.join(", ") || "n/a"}

Write learn/nodes/${d.id}.md following CONTRIBUTING.md and learn/schema/node.schema.json:
YAML frontmatter (id, title, summary, review: draft, authors, caveats, quiz of 3–5 questions with answers and
explanations, optional widgets) and a Markdown body with a '## Plain English' section.
Be faithful to the Lean statement as written (hypotheses, quantifier order, which side is complemented, universes
if they matter). Do not import claims from the paper that the Lean does not state. List anything you are unsure
of under caveats. Run 'cd learn && npm ci && npm run validate' before opening a PR.`;
}
function nodePage(id) {
  const d = byId.get(id);
  if (!d) { app.innerHTML = `<p>No declaration <code>${esc(id)}</code>. <a href="#/nodes">All nodes</a></p>`; return; }
  const n = nodes[id];
  const r = rec(id);
  if (!r.viewed) { r.viewed = Date.now(); save(); }
  const links = linkMap([...d.meaningDeps, ...d.proofDeps, id]);
  const editUrl = n ? `https://github.com/${REPO}/edit/main/learn/nodes/${encodeURIComponent(id)}.md`
    : `https://github.com/${REPO}/new/main/learn/nodes?filename=${encodeURIComponent(id)}.md`;
  const lean = wrapLeanLines(highlight(d.statement, links), d.statement, d.truncated ? `<span class="cm"> := … (proof omitted)</span>` : "");
  app.className = "node";
  // Layout (see .statusbar and .sbs in style.css):
  //   status bar (I think I understand this · quiz stars · colour), title, summary;
  //   plain English + widgets (left) beside the formal statement (right, sticky, lines wrap);
  //   the proof, step by step (full width; only for nodes with data/proofs.json entries);
  //   bonus quiz; edit links; discussion. Narrow screens stack in that order.
  app.innerHTML = `
    <div class="node-head">
      <div class="topline"><a class="small" href="#/">← graph</a><div class="statusbar" id="statusbar"></div></div>
      <h1>${n ? esc(n.title) : esc(id)}</h1>
      <div><span class="pill kind-${d.kind}">${d.kind}</span>${n ? `<span class="pill ${n.review === "draft" ? "draft" : ""}">${n.review}</span>` : ""}
      <span class="name">${esc(d.name)}</span></div>
      ${n ? `<p class="eli5 summary">${n.summaryHtml}</p>` : ""}
      ${HEADLINES.includes(id) ? `<p><a class="start-link" href="#/start">Start here: what the theorem says →</a> <span class="small muted">this statement and the ${STMT.defs.length} definitions it uses, simplest first</span></p>`
        : stmtSet.has(id) ? `<p class="small">Needed to read the main statement · <a href="#/start">what the theorem says →</a></p>` : ""}
      <p class="small muted status-note" id="status-note"></p>
    </div>
    <div class="sbs">
      <section class="sbs-plain" id="plain"></section>
      <section class="sbs-formal"><div class="sbs-formal-inner">
        <h2>Formal statement</h2>
        <pre class="lean wrap">${lean}</pre>
        <p class="small muted">${srcLink(d, "")}
        ${d.variables.length ? ` · section variables in scope: <code>${esc(d.variables.join("  "))}</code>` : ""}</p>
        <div class="small">
          <div><b>Mentions</b> (understand these first): <div class="deps">${depLinks(d.meaningDeps)}</div></div>
          ${!["theorem", "instance"].includes(d.kind) ? "" : d.proofDeps.length > 12 ? `<details class="usedby"><summary><b>Proof uses</b> (${d.proofDeps.length})</summary><div class="deps">${depLinks(d.proofDeps)}</div></details>` : `<div><b>Proof uses</b>: <div class="deps">${depLinks(d.proofDeps)}</div></div>`}
          ${d.mathlib.length ? `<div><b>From Mathlib</b> (taken as given): <div class="deps">${d.mathlib.map((m) => `<a href="${MATHLIB_DOCS(m)}" target="_blank" rel="noopener">${esc(m)}</a>`).join("")}</div></div>` : ""}
          ${d.usedBy.length ? `<details class="usedby"><summary><b>Used by</b> (${d.usedBy.length})</summary><div class="deps">${depLinks(d.usedBy.slice(0, 40))}${d.usedBy.length > 40 ? `<span>+${d.usedBy.length - 40} more</span>` : ""}</div></details>` : `<div><b>Used by</b>: <span class="muted">nothing in this project</span></div>`}
        </div>
      </div></section>
    </div>
    ${proofs[id] ? `<section class="proof-view" id="proof"><h2>The proof, step by step</h2>
      <p class="small muted">English for each step beside the Lean that does it. <span class="pv-src ok">explainer</span> = from this node's reviewed explainer;
      <span class="pv-src draft">draft</span> = not reviewed yet, so check it against the Lean.</p><div id="proof-view"></div></section>` : ""}
    <div id="content"></div>`;
  document.documentElement.style.setProperty("--hdr", (document.querySelector("header.top")?.offsetHeight || 0) + "px");
  if (proofs[id]) mountProofView(document.getElementById("proof-view"), proofs[id], {
    highlight: (s) => highlight(s, links), nodeHref: (x) => `#/node/${encodeURIComponent(x)}`,
    sourceUrl, githubSourceUrl, storageKey: "rakesieve-proofview",
  });
  const plain = document.getElementById("plain");
  const c = document.getElementById("content");
  if (!n) {
    plain.innerHTML = `
      <h2>Plain English</h2>
      <div class="panel stub"><h3>Needs explainer</h3>
      <p>Nobody has written a plain-English explanation and quiz for this declaration yet, so it can't be signed off.
      <a href="${editUrl}" target="_blank" rel="noopener">Write one on GitHub</a> (see <a href="https://github.com/${REPO}/blob/main/CONTRIBUTING.md">CONTRIBUTING.md</a>).</p>
      <details><summary>Prompt for an AI agent</summary><textarea class="prompt" readonly>${esc(agentPrompt(d))}</textarea></details></div>`;
    renderStatus(id);
  } else {
    plain.innerHTML = `
      <div class="eli5">${n.bodyHtml}</div>
      <div id="widgets"></div>
      ${n.caveatsHtml.length ? `<div class="panel caveats"><h3>Faithfulness notes</h3><ul>${n.caveatsHtml.map((x) => `<li>${x}</li>`).join("")}</ul></div>` : ""}`;
    c.innerHTML = `
      <h2 id="quiz-head">Bonus: check yourself</h2>
      <p class="small muted">Optional. Each question you get right fills a star in the bar at the top; all of them turns the node a darker green.</p>
      <div class="panel quiz" id="quiz"></div>
      <p class="small muted">Spotted an error or have a better explanation? <a href="${editUrl}" target="_blank" rel="noopener">Edit this node on GitHub</a>
      · <details style="display:inline"><summary>agent prompt</summary><textarea class="prompt" readonly>${esc(agentPrompt(d))}</textarea></details></p>`;
    const w = document.getElementById("widgets");
    for (const spec of n.widgets || []) mountWidget(w, spec);
    renderQuiz(id, n);
  }
  c.insertAdjacentHTML("beforeend", `<h2>Discussion</h2><div class="giscus-wrap" id="giscus"></div>`);
  mountGiscus(id);
}

const norm = (s) => String(s).toLowerCase().replace(/\s+/g, "").replace(/[`'"]/g, "");
function renderQuiz(id, n) {
  const qz = document.getElementById("quiz");
  const r = rec(id);
  const answers = r.answers || {};
  qz.innerHTML = n.quiz.map((q, i) => {
    let input;
    if (q.type === "choice") input = q.choicesHtml.map((c, j) => `<label class="choice"><input type="radio" name="q${i}" value="${j}" ${answers[i] === j ? "checked" : ""}> ${c}</label>`).join("");
    else input = `<input type="text" name="q${i}" value="${answers[i] != null ? esc(answers[i]) : ""}" placeholder="${q.type === "number" ? "a number" : "your answer"}">`;
    return `<div class="q" data-i="${i}"><div><b>Q${i + 1}.</b> ${q.qHtml}</div>${input}<div class="verdict"></div><div class="explain">${q.explainHtml}</div></div>`;
  }).join("") + `<button class="primary" id="check">Check answers</button> <span id="qres"></span>`;
  const check = () => {
    const ans = {}, oks = [];
    n.quiz.forEach((q, i) => {
      const box = qz.querySelector(`.q[data-i="${i}"]`);
      let ok = false, given;
      if (q.type === "choice") { const s = box.querySelector("input:checked"); given = s ? +s.value : null; ok = given === q.answer; }
      else {
        given = box.querySelector("input").value;
        ok = q.type === "number" ? given.trim() !== "" && Number(given) === q.answer : q.answer.some((a) => norm(a) === norm(given));
      }
      ans[i] = given;
      oks.push(ok);
      if (given === null || given === "") { box.classList.remove("answered"); box.querySelector(".verdict").innerHTML = ""; return; }
      box.classList.add("answered");
      box.querySelector(".verdict").innerHTML = ok ? `<span class="ok">✓ correct</span>` : `<span class="bad">✗ not quite — read the explanation and try again</span>`;
    });
    r.answers = ans;
    const sc = recordQuizResults(r, oks);
    save();
    const now = oks.filter(Boolean).length;
    document.getElementById("qres").innerHTML = sc.right === sc.total
      ? `<b class="ok" style="color:var(--green)">${starString(sc)} All ${sc.total} correct. Quiz passed.</b>`
      : `${now} / ${sc.total} correct this time · <span class="stars-inline">${starString(sc)}</span> ${sc.right} / ${sc.total} so far`;
    renderStatus(id);
  };
  document.getElementById("check").onclick = check;
  if (r.answers) check(); else renderStatus(id);
}

// The status bar at the very top of a node page: the "I think I understand this" assertion, the
// quiz stars (one per question, filled once answered correctly; click to jump to the quiz), and the
// node's colour. A short note under the summary says what is still missing.
function renderStatus(id) {
  refresh();
  const bar = document.getElementById("statusbar");
  if (!bar) return;
  const r = rec(id), d = byId.get(id), n = nodes[id];
  const st = status(id);
  const pending = d.meaningDeps.filter((x) => !understood(x));
  const links = (xs) => xs.map((x) => `<a href="#/node/${encodeURIComponent(x)}">${esc(x)}</a>`).join(", ");
  bar.className = `statusbar st-${st}`;
  bar.style.setProperty("--st", COLORS[st]);
  if (!n) {
    bar.innerHTML = `<span class="sw"></span><span class="lbl">${statusLabel(id)}</span>`;
    document.getElementById("status-note").innerHTML = "";
    return;
  }
  const sc = quizScore(r, n.quiz.length);
  bar.innerHTML = `
    <span class="sw" title="${esc(statusLabel(id))}"></span>
    <label class="iu"><input type="checkbox" id="so" ${r.signedOff ? "checked" : ""}> I think I understand this</label>
    <button type="button" class="stars" id="stars" title="Bonus quiz: ${sc.right} of ${sc.total} answered correctly. Click to go to the quiz."
      aria-label="Quiz score ${sc.right} of ${sc.total}"><span class="st">${starString(sc)}</span> <span class="ct">${sc.right}/${sc.total}</span></button>
    <span class="lbl">${statusLabel(id)}</span>`;
  document.getElementById("status-note").innerHTML = understood(id)
    ? `<span style="color:var(--both)">✓ Understood: you've marked this and everything it mentions.</span>${r.quizPassed ? "" : " The bonus quiz below would turn it dark green."}`
    : r.signedOff ? `It counts as <b>understood</b> once these are too: ${links(pending)}.`
    : pending.length ? `Mentions to understand too: ${links(pending)}.` : "";
  document.getElementById("so").onchange = (e) => { if (e.target.checked) r.signedOff = Date.now(); else delete r.signedOff; save(); renderStatus(id); };
  document.getElementById("stars").onclick = () => document.getElementById("quiz-head")?.scrollIntoView({ behavior: "smooth", block: "start" });
}

function mountGiscus(id) {
  const el = document.getElementById("giscus");
  if (location.protocol === "file:") { el.innerHTML = `<p class="muted small">Comments load on the published site.</p>`; return; }
  if (!GISCUS.repoId) { el.innerHTML = `<p class="muted small">Comments are not set up yet.</p>`; return; }
  const s = document.createElement("script");
  s.src = "https://giscus.app/client.js";
  Object.entries({
    "data-repo": GISCUS.repo, "data-repo-id": GISCUS.repoId, "data-category": GISCUS.category, "data-category-id": GISCUS.categoryId,
    "data-mapping": "specific", "data-term": `node: ${id}`, "data-strict": "1", "data-reactions-enabled": "1",
    "data-emit-metadata": "0", "data-input-position": "top", "data-theme": "dark", "data-lang": "en", "data-loading": "lazy",
  }).forEach(([k, v]) => s.setAttribute(k, v));
  s.crossOrigin = "anonymous"; s.async = true;
  el.append(s);
}

// ------------------------------------------------------------------ list page
function listPage(fileFilter) {
  const q = new URLSearchParams(location.hash.split("?")[1] || "");
  const file = fileFilter || q.get("file");
  const rows = decls.filter((d) => !file || d.module === file)
    .sort((a, b) => (!!nodes[b.id] - !!nodes[a.id]) || ((a.depth ?? 99) - (b.depth ?? 99)) || a.id.localeCompare(b.id));
  const fileDecl = file && rows[0];
  app.innerHTML = `<h1>${file ? `Declarations in ${esc(file)}.lean` : "All declarations"}</h1>
    ${fileDecl ? `<p class="small"><a href="${sourceUrl(fileDecl.file)}">Read ${esc(file)}.lean, highlighted →</a></p>` : ""}
    <p class="muted">${Object.keys(nodes).length} with explainers, ${decls.length - Object.keys(nodes).length} awaiting one. ${file ? `<a href="#/nodes">show all</a>` : ""}
    Agents: the work list is <a href="data/needs-explainer.json">data/needs-explainer.json</a>.</p>
    <input type="text" id="flt" placeholder="filter…" style="max-width:20rem">
    <table class="node-list"><thead><tr><th>declaration</th><th>kind</th><th>status</th><th>distance from a headline</th><th>file</th></tr></thead>
    <tbody>${rows.map((d) => `<tr data-id="${esc(d.id.toLowerCase())}"><td><a href="#/node/${encodeURIComponent(d.id)}">${esc(d.id)}</a></td><td><span class="pill kind-${d.kind}">${d.kind}</span></td><td><span class="pill st-${status(d.id)}">${statusLabel(d.id)}</span></td><td>${d.depth ?? "—"}</td><td class="small"><a class="muted" href="${sourceUrl(d.file, d.line, d.endLine)}" title="${esc(sourceLabel(d.file, d.line, d.endLine))}">${d.module}</a></td></tr>`).join("")}</tbody></table>`;
  document.getElementById("flt").oninput = (e) => {
    const v = e.target.value.toLowerCase();
    app.querySelectorAll("tbody tr").forEach((tr) => (tr.style.display = tr.dataset.id.includes(v) ? "" : "none"));
  };
}

// ------------------------------------------------------------------ start here (statement first)
function stmtCard(id, headline) {
  const d = byId.get(id), n = nodes[id], r = rec(id), st = status(id);
  const sc = n ? quizScore(r, n.quiz.length) : null;
  const lean = wrapLeanLines(highlight(d.statement, linkMap([...d.meaningDeps, id])), d.statement, d.truncated ? `<span class="cm"> := …</span>` : "");
  return `<div class="card${headline ? " headline" : ""}" style="--st:${COLORS[st]}">
    <div class="card-top">
      <span class="sw" title="${esc(statusLabel(id))}"></span>
      <a class="ttl" href="#/node/${encodeURIComponent(id)}">${n ? esc(n.title) : esc(id)}</a>
      <span class="pill kind-${d.kind}">${d.kind}</span>
      <span class="grow"></span>
      ${n ? `<label class="iu"><input type="checkbox" data-so="${esc(id)}" ${r.signedOff ? "checked" : ""}> I think I understand this</label>
      <a class="stars" href="#/node/${encodeURIComponent(id)}" title="Bonus quiz on its page: ${sc.right} of ${sc.total} right">${starString(sc)} <span class="ct">${sc.right}/${sc.total}</span></a>` : `<span class="small muted">no explainer yet</span>`}
    </div>
    ${n ? `<p class="eli5 one">${n.summaryHtml}</p>` : ""}
    <pre class="lean wrap">${lean}</pre>
    <div>${srcLink(d)}</div>
  </div>`;
}
function startPage() {
  app.className = "node";
  const y = startPage.keepScroll ? scrollY : 0;
  startPage.keepScroll = false;
  const done = STMT.defs.filter((id) => understood(id)).length;
  app.innerHTML = `
    <p class="small"><a href="#/">← graph</a></p>
    <h1>Start here: what the theorems say</h1>
    <p class="muted" style="max-width:60rem">Before any proof: the headline statement, then every definition you need to <i>read</i> it,
    simplest first. These come from the statement's own mentions, followed down to Mathlib. Whatever the <i>proof</i>
    uses comes later and is not listed here. You have marked <b>${done}</b> of ${STMT.defs.length} of these definitions understood.</p>
    <p class="muted" style="max-width:60rem">Five theorems are exported in <code>Results.lean</code>. The first three statements below say the same thing, Euclid's theorem; they differ only in which prime generator the proof runs. The second card is not a theorem but the instance that says the RakeSieve, stepped, yields each next prime with none skipped: that is where the sieve's correctness lives (see <a href="#/review">the review</a>).</p>
    <p class="muted" style="max-width:60rem"><b>R stands for <i>residue</i>.</b> In the statements below, <code>R p</code> is the set of numbers ≥ 2 that no prime ≤ p divides: what is left after crossing out the multiples of every prime up to p. So <code>R 2</code> is the odd numbers from 3 up, and the sieve's next prime is always the least element of <code>R p</code> (<a href="#/node/R">more on R</a>).</p>
    <h2>The statements</h2>
    ${HEADLINES.map((id) => stmtCard(id, true)).join("")}
    <h2>Definitions it uses (${STMT.defs.length}), simplest first</h2>
    ${STMT.defs.map((id) => stmtCard(id, false)).join("")}
    <h2>From Mathlib (taken as given)</h2>
    <ul class="mathlib-gloss">${STMT.mathlib.map((m) => `<li><a href="${MATHLIB_DOCS(m)}" target="_blank" rel="noopener"><code>${esc(m)}</code></a> — ${MATHLIB_GLOSS[m] || `<span class="muted">see the Mathlib docs</span>`}</li>`).join("")}</ul>
    <p>Next: <a href="#/">the proof graph</a>, where everything below these sits.</p>`;
  app.querySelectorAll("input[data-so]").forEach((cb) => cb.onchange = () => {
    const r = rec(cb.dataset.so);
    if (cb.checked) r.signedOff = Date.now(); else delete r.signedOff;
    save(); refresh(); startPage.keepScroll = true; startPage();
  });
  if (y) scrollTo(0, y);
}

// ------------------------------------------------------------------ markdown pages (review, trust)
function mdPage(key) {
  app.className = "node";
  const pg = pages[key];
  app.innerHTML = pg ? `<p class="small"><a href="#/">← graph</a></p><div class="eli5">${pg.html}</div>` : `<p>Page not found. <a href="#/">Home</a></p>`;
}

// ------------------------------------------------------------------ about
function aboutPage() {
  app.innerHTML = `<p class="small"><a href="#/">← graph</a></p><div class="eli5">${pages.about?.html || "<p>About page missing.</p>"}
  <p class="small muted">${decls.length} declarations on the site (${reachable.length} reached from the headlines), ${Object.keys(nodes).length} with explainers.</p></div>`;
}

route();
