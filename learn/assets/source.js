// The single place that turns a Lean source location into a URL or a label. Everything that links to
// the source (node pages, the node list, start cards, walkthrough steps, the proof view, the build's
// "File.lean lines a–b" rewriting and the source pages themselves) goes through this module.
// Reader-facing links go to the on-site rendered source (proof-sites CONVENTIONS §7:
// src/<path>.lean.html#L<a>-L<b>, built by tools/build_source.mjs); GitHub is only the small secondary
// link. The agent prompt keeps the GitHub URL on purpose (agents work from the repo), via githubSourceUrl.
export const REPO = "tangentproofs/rakesieve";
export const BRANCH = "main";
export const BLOB = `https://github.com/${REPO}/blob/${BRANCH}`;
/** Site-relative directory of the rendered source pages (null → link to GitHub instead). */
export const SOURCE_BASE = "src/";

/** "#L<a>-L<b>" (or "#L<a>"; "" without lines): the anchor the source pages highlight. */
export const anchor = (from, to) => (from ? `#L${from}${to && to !== from ? `-L${to}` : ""}` : "");

/** GitHub URL for lines `from`–`to` (inclusive; both optional) of `file` (repo-relative path). */
export const githubSourceUrl = (file, from, to) => `${BLOB}/${file}${anchor(from, to)}`;

/** URL for that location given a rendered-source base (null → GitHub). Pure, for tests. */
export const sourceUrlFor = (base, file, from, to) => (base ? `${base}${file}.html${anchor(from, to)}` : githubSourceUrl(file, from, to));

/** URL a reader should follow for that source location. `root` prefixes it from deeper pages (e.g. "../../"). */
export const sourceUrl = (file, from, to, root = "") => (SOURCE_BASE ? root : "") + sourceUrlFor(SOURCE_BASE, file, from, to);

/** "Main.lean lines 9–28" (or "line 9"). With `full`, the whole repo path. */
export function sourceLabel(file, from, to, full = false) {
  const name = full ? file : file.split("/").pop();
  if (!from) return name;
  return to && to !== from ? `${name} lines ${from}–${to}` : `${name} line ${from}`;
}
