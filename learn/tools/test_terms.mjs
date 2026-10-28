#!/usr/bin/env node
// Every page that writes the residue set "R" must say what R is before its first use, so a reader
// who lands anywhere is never left guessing. Checks node summaries + bodies (learn/nodes/*.md),
// the markdown pages, and the "Start here" intro in assets/app.js. Titles and quizzes are exempt
// (they are read after the summary).   node tools/test_terms.mjs
import fs from "node:fs";
import path from "node:path";
import yaml from "js-yaml";

const SITE = path.dirname(path.dirname(new URL(import.meta.url).pathname));
// a standalone R: not part of a word, identifier, `code` span or link target like #/node/R
const R_USE = /(?<![\w`/.])R(?![\w`])/;
const fails = [];
const check = (where, text) => {
  const m = R_USE.exec(text);
  if (!m) return;
  const g = text.toLowerCase().indexOf("residue");
  // "residue" must come first, or in the same breath ("R stands for residue", "R 2, the residue …")
  if (g < 0 || g > m.index + 40) fails.push(`${where}: "R" used before saying it stands for residue: …${text.slice(Math.max(0, m.index - 60), m.index + 30).replace(/\n/g, " ")}…`);
};
for (const f of fs.readdirSync(path.join(SITE, "nodes")).filter((f) => f.endsWith(".md")).sort()) {
  const src = fs.readFileSync(path.join(SITE, "nodes", f), "utf8");
  const [, fm, body] = src.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  const d = yaml.load(fm);
  check(`nodes/${f} summary`, d.summary);
  check(`nodes/${f} body`, d.summary.includes("residue") ? "residue " + body : body);
}
for (const f of fs.readdirSync(path.join(SITE, "pages")).filter((f) => f.endsWith(".md"))) check(`pages/${f}`, fs.readFileSync(path.join(SITE, "pages", f), "utf8"));
const app = fs.readFileSync(path.join(SITE, "assets", "app.js"), "utf8");
const start = app.slice(app.indexOf("function startPage()"), app.indexOf("<h2>The statements</h2>"));
check("assets/app.js startPage intro", start.replace(/\$\{[^}]*\}/g, ""));
if (!/R stands for/.test(start)) fails.push("assets/app.js startPage: intro must explain R (the residue) before the statements");
if (fails.length) { console.error("FAIL\n" + fails.join("\n")); process.exit(1); }
console.log("test_terms: ok");
