// Turn mentions of Lean files in rendered node HTML into links to the browsable source pages:
//   <code>Height.lean</code>               -> src/OAI/…/Height.lean.html
//   Main.lean, lines 10-28 / Main.lean lines 9–28 / <code>Main.lean</code> line 12
//                                          -> src/OAI/…/Main.lean.html#L10-L28 (highlighted range)
// Text already inside a link is left alone. Unknown file names are left as text; a range outside the
// file is reported through onErr (a build error). Tested by tools/test_source.mjs.
import { sourceUrl } from "../assets/source.js";

const RE = /(<code>)?\b((?:[A-Za-z0-9_-]+\/)*[A-Z][A-Za-z0-9_]*\.lean)(<\/code>)?(,?\s+lines?\s+(\d+)(?:\s*(?:-|–|—|to)\s*(\d+))?)?/g;

export function resolveLeanFile(name, files) {
  const hits = files.filter((f) => f === name || f.endsWith("/" + name));
  return hits.length === 1 ? hits[0] : null;
}

export function linkSourceRefs(html, files, linesOf = null, onErr = () => {}) {
  // Split off existing anchors and tags; only rewrite plain text (and <code> wrappers around it).
  return html.split(/(<a\b[\s\S]*?<\/a>)/).map((part, k) => {
    if (k % 2) return part;
    return part.replace(RE, (all, c1, name, c2, range, a, b) => {
      if ((c1 && !c2) || (!c1 && c2)) return all; // a partial <code> match; leave it
      const file = resolveLeanFile(name, files);
      if (!file) return all;
      let line = a ? +a : null, end = b ? +b : line;
      if (line && linesOf) {
        const n = linesOf(file).length;
        if (line < 1 || end > n || end < line) { onErr(`"${name} ${range.trim()}" is outside ${file} (${n} lines)`); return all; }
      }
      const text = (c1 ? `<code>${name}</code>` : name) + (range || "");
      return `<a class="srcref" href="${sourceUrl(file, line, end)}" title="${file}${line ? ` lines ${line}–${end}` : ""} (rendered source)">${text}</a>`;
    });
  }).join("");
}
