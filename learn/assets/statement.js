// "Statement first": which project declarations a reader needs in order to read the headline
// theorem STATEMENTS. Follows only statement-level edges (`meaningDeps`, shown as "Mentions"),
// never proof edges (`proofDeps`), and stops at Mathlib (Mathlib names are not declarations here).
// Tested by tools/test_statement.mjs.

/** For headline ids `heads`, return
 *    defs:    the project declarations their statements mention, transitively, in dependency
 *             order (everything a definition mentions comes before it; ties by id), heads excluded;
 *    mathlib: the Mathlib names mentioned by the heads and those defs, sorted. */
export function statementSet(byId, heads) {
  const order = [], state = new Map(); // 1 = on stack, 2 = done
  const visit = (id) => {
    if (state.get(id) || !byId.has(id)) return;
    state.set(id, 1);
    for (const x of [...byId.get(id).meaningDeps].sort()) visit(x);
    state.set(id, 2);
    order.push(id);
  };
  for (const h of heads) visit(h);
  const headSet = new Set(heads);
  const defs = order.filter((id) => !headSet.has(id));
  const mathlib = [...new Set([...heads, ...defs].flatMap((id) => byId.get(id)?.mathlib || []))].sort();
  return { defs, mathlib };
}
