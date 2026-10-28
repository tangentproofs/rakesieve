// Widgets for this site. Only the proof-outline widget ("walkthrough") is used; its markup lives in
// assets/walkthrough.js (shared with the reference site, star-height).
import { h } from "./dom.js";
import { outlineHtml, stepDetailHtml } from "./walkthrough.js";

// A proof outline: every step shown at once. Click a step to show its note, Lean and the nodes it
// uses below the outline; the first step is selected to begin with.
function walkthroughWidget(el, cfg = {}) {
  const steps = cfg.steps || [];
  const listBox = h("div", { class: "flow wt" }), detail = h("div", { class: "wtdetail" });
  let i = 0;
  el.append(listBox, detail);
  function run() {
    listBox.innerHTML = outlineHtml(steps, i);
    listBox.querySelectorAll(".step").forEach((d) => d.addEventListener("click", (ev) => { if (ev.target.tagName !== "A") { i = +d.dataset.j; run(); } }));
    detail.innerHTML = stepDetailHtml(steps[i]);
  }
  run();
}

const REGISTRY = { walkthrough: walkthroughWidget };

export function mountWidget(container, spec) {
  const box = h("div", { class: "widget" });
  if (spec.titleHtml) box.append(h("h3", { html: spec.titleHtml }));
  else if (spec.title) box.append(h("h3", {}, spec.title));
  container.append(box);
  const f = REGISTRY[spec.type];
  if (!f) { box.append(h("p", { class: "err" }, `unknown widget ${spec.type}`)); return; }
  try { f(box, spec.config || {}); } catch (e) { box.append(h("p", { class: "err" }, e.message)); }
}
