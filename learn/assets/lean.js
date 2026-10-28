// Tiny Lean 4 highlighter (Monokai). Identifiers that name a declaration in
// `links` (a Map from token → node id) become links to that node's page.
// `refAt(start, tok, cls)` (optional) may return HTML for an identifier token that starts at UTF-16
// offset `start` of `src`, or null to fall back; the source pages (tools/build_source.mjs) use it
// to link exact cross-references from Lean's .ilean data. `cls` highlights a plain token.
const KW = new Set(("theorem lemma def abbrev inductive structure class instance where fun λ let have show by " +
  "match with if then else do return namespace end section universe variable open scoped noncomputable " +
  "private protected omit in at calc deriving extends Type Sort Prop forall exists").split(" "));
const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const IDENT = /^[A-Za-z_\u00C0-\u024F\u0370-\u03FF\u1F00-\u1FFF\u2100-\u214F𝒜-𝔷][A-Za-z0-9_'!?\u00C0-\u024F\u0370-\u03FF\u1F00-\u1FFF\u2080-\u209C\u2100-\u214F.]*/u;

export function highlight(src, links = new Map(), href = (id) => `#/node/${encodeURIComponent(id)}`, refAt = null) {
  let out = "", i = 0;
  const link = (tok) => {
    if (links.has(tok)) return `<a class="ref" href="${href(links.get(tok))}">${esc(tok)}</a>`;
    const parts = tok.split(".");
    if (parts.length > 1) {
      const last = parts.pop();
      const head = parts.join(".") + ".";
      if (links.has(last)) return `${cls(parts.join("."))}.<a class="ref" href="${href(links.get(last))}">${esc(last)}</a>`;
      return cls(head.slice(0, -1)) + "." + esc(last);
    }
    return null;
  };
  const cls = (tok) => {
    if (KW.has(tok)) return `<span class="kw">${tok}</span>`;
    if (/^[A-Z]/.test(tok)) return `<span class="ty">${esc(tok)}</span>`;
    return esc(tok);
  };
  while (i < src.length) {
    const rest = src.slice(i);
    let m;
    if ((m = rest.match(/^--[^\n]*/)) || (m = rest.match(/^\/-[\s\S]*?-\//))) {
      out += `<span class="cm">${esc(m[0])}</span>`;
    } else if ((m = rest.match(/^"(?:[^"\\]|\\.)*"/)) || (m = rest.match(/^'[^'\\]'/))) {
      out += `<span class="str">${esc(m[0])}</span>`;
    } else if ((m = rest.match(/^\.[a-z][A-Za-z0-9_]*/)) && !/[A-Za-z0-9_)\]]/.test(src[i - 1] || "")) {
      out += `<span class="ctor">${esc(m[0])}</span>`;
    } else if ((m = rest.match(/^\d+/))) {
      out += `<span class="num">${m[0]}</span>`;
    } else if ((m = rest.match(IDENT))) {
      let tok = m[0].replace(/\.+$/, "");
      m = [tok];
      out += (refAt && refAt(i, tok, cls)) ?? link(tok) ?? cls(tok);
    } else if ((m = rest.match(/^(:=|→|↔|∀|∃|∧|∨|¬|≤|≥|≠|∈|∉|⊓|⊔|⨆|⨅|ᶜ|∗|\*|\+|<\+:|=>|\||×|•|∘|→\*|→ₗ)/))) {
      out += `<span class="op">${esc(m[0])}</span>`;
    } else {
      m = [src[i]];
      out += esc(src[i]);
    }
    i += m[0].length;
  }
  return out;
}

// token → id map for a declaration's neighbourhood.
export function linkMap(ids) {
  const map = new Map();
  const ambiguous = new Set();
  for (const id of ids) {
    const parts = id.split(".");
    for (let k = 0; k < parts.length; k++) {
      const suf = parts.slice(k).join(".");
      if (map.has(suf) && map.get(suf) !== id) ambiguous.add(suf);
      else map.set(suf, id);
    }
  }
  for (const a of ambiguous) map.delete(a);
  return map;
}
