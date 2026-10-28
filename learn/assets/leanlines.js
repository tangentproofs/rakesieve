// Split highlighted Lean (HTML from lean.js highlight) into one balanced HTML fragment per source
// line, so each line can wrap with a hanging indent instead of scrolling sideways.
// Tested by tools/test_leanlines.mjs.

/** Split `html` at newlines. Tags left open at a line end are closed there and reopened on the
 *  next line, so every fragment is well-formed on its own. */
export function splitHtmlLines(html) {
  const lines = [];
  let cur = "", open = []; // stack of opening tags, e.g. '<span class="cm">'
  const re = /<\/?[a-zA-Z][^>]*>|\n|[^<\n]+/g;
  let m;
  while ((m = re.exec(html))) {
    const t = m[0];
    if (t === "\n") {
      for (let k = open.length - 1; k >= 0; k--) cur += `</${tagName(open[k])}>`;
      lines.push(cur);
      cur = open.join("");
    } else if (t.startsWith("</")) {
      open.pop();
      cur += t;
    } else if (t.startsWith("<")) {
      if (!t.endsWith("/>")) open.push(t);
      cur += t;
    } else cur += t;
  }
  lines.push(cur);
  return lines;
}
const tagName = (open) => open.match(/^<([a-zA-Z0-9]+)/)[1];

/** Leading-space count of a line of plain text (tabs count as 2). */
export const indentOf = (line) => { let n = 0; for (const ch of line) { if (ch === " ") n++; else if (ch === "\t") n += 2; else break; } return n; };

/** Wrap each line of highlighted Lean in <span class="ln" style="--i:N">, where N is that line's
 *  leading indentation in characters; the leading spaces themselves are removed (CSS turns --i into
 *  padding plus a hanging indent for wrapped continuation lines). `src` is the plain source the
 *  HTML came from; `tail` is extra HTML appended to the last line. */
export function wrapLeanLines(html, src, tail = "") {
  const parts = splitHtmlLines(html);
  const raw = src.split("\n");
  return parts.map((h, k) => {
    const n = indentOf(raw[k] ?? "");
    const body = h.replace(/^((?:<[^>]+>)*) +/, "$1") + (k === parts.length - 1 ? tail : "");
    return `<span class="ln" style="--i:${n}">${body || "&#8203;"}</span>`;
  }).join("");
}
