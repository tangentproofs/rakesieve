#!/usr/bin/env python3
"""Build learn/data/decls.json and learn/data/xref.json from the Lean source text, WITHOUT a Lean build.

The reference sites (star-height and others) extract declarations from a compiled build
(ExtractDecls.lean) and identifier references from Lean's .ilean files. This site is built from the
source text instead (the owner asked for no Lean builds on our servers), as subexponential-sat was:

  * declarations: `def/theorem/lemma/abbrev/structure/class/instance` lines in FILES (the modules
    listed in lakefile.lean, plus the exe root Main.lean, read from the lakefile), with namespace, line range and verbatim header text;
  * anonymous instances get the name Lean would most likely generate (inst + class + type); the
    real auto-generated name may differ slightly, which only matters for this site's ids;
  * mentions (meaningDeps) / proof uses (proofDeps): identifier tokens of the statement (and of a
    definition's body) / of a theorem's proof, resolved against the declarations found here;
  * Mathlib links: tokens in the hand-checked list MATHLIB below.

Every declaration is marked `"extracted": false` so the site and its Trust page say so.
"""
import hashlib, json, os, re

LEARN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(LEARN)
OUT = os.path.join(LEARN, "data")


def built_files():
    """The modules lakefile.lean builds (every `lean_lib X` plus the exe's `root`), as files, in import
    order. Read from the lakefile so a new or moved module (SimpleGen.lean, NoEuclidCheck.lean) is
    scanned without editing this script."""
    lake = open(os.path.join(ROOT, "lakefile.lean"), encoding="utf-8").read()
    mods = re.findall(r"^lean_lib\s+«?(\w+)»?", lake, re.M) + re.findall(r"root\s*:=\s*`(\w+)", lake)
    imports = {m: [i for i in re.findall(r"^import\s+(\S+)", open(os.path.join(ROOT, m + ".lean"), encoding="utf-8").read(), re.M) if i in mods] for m in mods}
    order, seen = [], set()
    def visit(m):
        if m in seen: return
        seen.add(m)
        for i in imports[m]: visit(i)
        order.append(m)
    for m in mods: visit(m)
    return [m + ".lean" for m in order]


def headlines():
    """The site's headline list lives in one place, assets/app.js (HEADLINES); the scan measures depth from it.
    Every theorem in Results.lean must be on it, so a new headline cannot be left off the site."""
    app = open(os.path.join(LEARN, "assets", "app.js"), encoding="utf-8").read()
    return json.loads(re.search(r"const HEADLINES = (\[[^\]]*\]);", app).group(1))


FILES = built_files()
HEADS = headlines()

# Mathlib / core names used in the project (checked by hand against the Mathlib docs).
MATHLIB = """Nat Nat.Prime Nat.find Nat.find_spec Nat.find_min Nat.exists_infinite_primes Nat.prime_two
Nat.Prime.two_le Nat.exists_prime_and_dvd Nat.prime_dvd_prime_iff_eq Nat.prime_def_lt Nat.le_of_dvd Nat.dvd_trans
Nat.mod_lt Nat.div_add_mod Nat.Prime.pos Set List List.Pairwise List.Nodup List.dedup List.mergeSort List.Perm
List.range List.map List.filter List.length List.mergeSort_perm List.sortedLE_mergeSort List.mem_iff_get
List.get_mem Subtype Subtype.ext_iff Function.iterate_succ_apply' Fin Bool Prop Dvd Repr Ord LT LE Coe
ToString Inhabited Std.Total Option IO exists_apply_eq_apply""".split()
ALIASES = {n: n for n in MATHLIB}

DECL = re.compile(r"^\s*(?:@\[[^\]]*\]\s*)?(?:(?:private|protected|noncomputable|partial|unsafe)\s+)*(def|theorem|lemma|abbrev|structure|inductive|class|instance)\b\s*([^\s:({\[]*)")
TOK = re.compile(r"[A-Za-z_\u00c0-\u024f\u0370-\u03ff\u1d00-\u1dbf\u2080-\u209f][\w.'\u00c0-\u024f\u0370-\u03ff\u1d00-\u1dbf\u2080-\u209f!?₀-₉]*")
OPEN, CLOSE = "([{⟨⦃", ")]}⟩⦄"


def cut(text, kind):
    """Header up to the top-level ':=' (or ' where' / first top-level '|'). Whole text for types."""
    if kind in ("structure", "inductive", "class"): return text.rstrip(), ""
    depth, i = 0, 0
    while i < len(text):
        c = text[i]
        if c in OPEN: depth += 1
        elif c in CLOSE: depth = max(0, depth - 1)
        elif depth == 0 and text.startswith(":=", i): return text[:i].rstrip(), text[i:]
        elif depth == 0 and re.match(r"\swhere\b", text[i:i + 7]): return text[:i].rstrip(), text[i:]
        elif depth == 0 and kind != "theorem" and c == "\n" and re.match(r"\n\s*\|", text[i:]): return text[:i].rstrip(), text[i:]
        i += 1
    return text.rstrip(), ""


def inst_name(header):
    """inst + class + type heads, e.g. `instance : PrimeGen (PrimeSieve α) where` -> instPrimeGenPrimeSieve."""
    h = header.split(":", 1)[1] if ":" in header else header
    h = re.split(r"\swhere\b|:=", h)[0]
    h = re.sub(r"\([^()]*:=[^()]*\)", "", h)  # named arguments like (α := ASeq)
    parts = [t.split(".")[-1] for t in TOK.findall(h) if t[0].isupper()]
    return "inst" + "".join(parts)


def scan(file):
    lines = open(os.path.join(ROOT, file), encoding="utf-8").read().split("\n")
    ns, starts, in_comment = [], [], 0
    for k, ln in enumerate(lines):
        s = ln.strip()
        was = in_comment
        in_comment += ln.count("/-") - ln.count("-/")
        if was > 0: continue
        if m := re.match(r"^namespace\s+(\S+)", ln): ns.append(m.group(1)); starts.append(("ns", k)); continue
        if m := re.match(r"^end\s+(\S+)\s*$", ln):
            if ns and ns[-1] == m.group(1): ns.pop()
            starts.append(("end", k)); continue
        if re.match(r"^(section|end|open|variable|universe|set_option|elab|macro|syntax|macro_rules|attribute|initialize|#|/-|--)\b", ln) or re.match(r"^(#|/-|--)", ln): starts.append(("other", k)); continue
        if m := DECL.match(ln):
            kind, name = m.group(1), m.group(2)
            if kind == "instance" and not name:
                hdr = " ".join(lines[k:k + 3])
                name = inst_name(hdr)
            if not name: continue
            full = ".".join(ns + [name]) if not name.startswith("_root_.") else name[7:]
            starts.append(("decl", k, kind, full, kind == "instance" and not m.group(2)))
    out = []
    for j, st in enumerate(starts):
        if st[0] != "decl": continue
        k, kind, full, anon = st[1], st[2], st[3], st[4]
        end = (starts[j + 1][1] if j + 1 < len(starts) else len(lines)) - 1
        while end > k and (not lines[end].strip() or lines[end].strip().startswith(("--", "/-", "-/"))): end -= 1
        text = "\n".join(lines[k:end + 1])
        out.append({"name": full, "kind": "theorem" if kind == "lemma" else kind, "file": file,
                    "line": k + 1, "endLine": end + 1, "text": text, "anonInstance": anon,
                    "ns": full.rsplit(".", 1)[0] if "." in full else ""})
    return out


def main():
    decls = []
    for f in FILES:
        for d in scan(f):
            d["id"] = d["name"]
            decls.append(d)
    by_full = {d["name"]: d for d in decls}

    def resolve(tok, d):
        if tok in by_full: return by_full[tok]
        ns = d["ns"].split(".") if d["ns"] else []
        for i in range(len(ns), 0, -1):
            c = ".".join(ns[:i] + [tok])
            if c in by_full: return by_full[c]
        cands = [e for e in decls if e["name"].endswith("." + tok) and not e["anonInstance"]]
        return cands[0] if len(cands) == 1 else None

    def dot(suffix):
        cands = [e for e in decls if e["name"].endswith(suffix) and not e["anonInstance"]]
        return cands[0] if len(cands) == 1 else None

    for d in decls:
        stmt, proof = cut(d["text"], d["kind"])
        # short definitions read best with their body (R, nosk', PrimeGt, aseq …); long ones show the header
        d["statement"] = d["text"].rstrip() if d["kind"] in ("def", "abbrev") and d["text"].count("\n") < 6 else stmt
        meaning_text = stmt if d["kind"] in ("theorem", "instance") else d["text"]

        # names bound by the declaration's own binders, e.g. `(pred: Nat → Prop)` in `structure RakeMap`,
        # are local variables, not references to a declaration that happens to share the name
        bound = {b for grp in re.findall(r"[({⦃\[]\s*([^():{}\[\]⦃⦄]+?)\s*:(?!=)", stmt) for b in grp.split()}

        def deps(text):
            out = []
            clean = re.sub(r"--[^\n]*|/-[\s\S]*?-/", "", text)
            for m in TOK.finditer(clean):
                if m.start() and clean[m.start() - 1] == ".": continue
                t = m.group(0)
                if t in bound: continue
                # `s.survivor` / `rs₀.rm.rem` (dot notation on a variable): fall back to the last field,
                # when exactly one declaration ends with it
                for cand in (t, t.rstrip("."), "." + t.rstrip(".").rsplit(".", 1)[-1] if "." in t.rstrip(".") else None):
                    if not cand: continue
                    e = resolve(cand, d) if not cand.startswith(".") else dot(cand)
                    if e and e is not d and not e["anonInstance"] and e["id"] not in out: out.append(e["id"]); break
            return out
        d["meaningDeps"] = deps(meaning_text)
        d["proofDeps"] = [x for x in deps(proof) if x not in d["meaningDeps"]] if d["kind"] in ("theorem", "instance") else []
        ml = []
        for t in TOK.findall(re.sub(r"--[^\n]*|/-[\s\S]*?-/", "", meaning_text)):
            n = ALIASES.get(t)
            if n and n not in ml and n not in by_full: ml.append(n)
        d["mathlib"] = ml
    # Instances are found by type class search, not by name, so their edges are added by hand: anything
    # that steps a `PrimeSieve RakeSieve` goes through the PrimeSieve driver instance and the RakeSieve's
    # two sieve instances; SimpleGen's corollary goes through SimpleGen's PrimeGen instance.
    VIA_SIEVE = ["instPrimeGenPrimeSieve", "RakeSieve.instPrimeSieveStateRakeSieve", "RakeSieve.instPrimeSieveDriverRakeSieve"]
    MANUAL = {"results_exists_prime_gt_of_rakeSieve": VIA_SIEVE, "results_rakeSieve_emits_every_prime": VIA_SIEVE,
              "results_rakeSieve_step": VIA_SIEVE[1:], "results_rakeSieve_never_empty": VIA_SIEVE[1:],
              "simpleGen_exists_prime_gt": ["instPrimeGenSimpleGen"]}
    # `variable (α : Type) [PrimeSieveState α] [PrimeSieveDriver α]` (PrimeSieve.lean line 210) is in scope for
    # these declarations; the classes it names are part of what they mean.
    SECTION_VARS = ["(α : Type)", "[PrimeSieveState α]", "[PrimeSieveDriver α]"]
    ids = {d["id"]: d for d in decls}
    for k in ("PrimeSieve", "PrimeSieve.next", "instPrimeGenPrimeSieve"):
        ids[k]["variables"] = SECTION_VARS
        for v in ("PrimeSieveState", "PrimeSieveDriver"):
            if v not in ids[k]["meaningDeps"]: ids[k]["meaningDeps"].append(v)
            if v in ids[k]["proofDeps"]: ids[k]["proofDeps"].remove(v)
    # `variable (r: Rake) {j: Nat} (hj: 0<j)` (Rake.lean line 350) is in scope for rem and HasNonMultiple.
    for k in ("Rake.rem", "Rake.HasNonMultiple"):
        ids[k]["variables"] = ["(r: Rake)", "{j: Nat}", "(hj: 0<j)"]
    for k, vs in MANUAL.items():
        for v in vs:
            assert k in ids and v in ids, f"MANUAL instance edge {k} -> {v}: no such declaration in {FILES}"
            if v not in ids[k]["proofDeps"]: ids[k]["proofDeps"].append(v)
    for d in decls: d["usedBy"] = sorted(e["id"] for e in decls if d["id"] in e["meaningDeps"] + e["proofDeps"])
    results = [d["name"] for d in decls if d["file"] == "Results.lean" and d["kind"] == "theorem"]
    missing = [h for h in HEADS if h not in ids] + [r for r in results if r not in HEADS]
    assert not missing, f"assets/app.js HEADLINES and Results.lean disagree: {missing}"
    dist = {h: 0 for h in HEADS}
    frontier = list(dist)
    while frontier:
        nxt = []
        for i in frontier:
            for j in ids[i]["meaningDeps"] + ids[i]["proofDeps"]:
                if j not in dist: dist[j] = dist[i] + 1; nxt.append(j)
        frontier = nxt
    out = []
    for d in sorted(decls, key=lambda d: (FILES.index(d["file"]), d["line"])):
        out.append({"id": d["id"], "name": d["name"], "kind": d["kind"], "file": d["file"],
                    "module": d["file"][:-5], "line": d["line"], "endLine": d["endLine"],
                    "statement": d["statement"], "variables": d.get("variables", []), "truncated": False,
                    "mathlib": d["mathlib"], "meaningDeps": d["meaningDeps"], "proofDeps": d["proofDeps"],
                    "usedBy": d["usedBy"], "depth": dist.get(d["id"]), "extracted": False,
                    **({"autoName": True} if d["anonInstance"] else {})})
    json.dump(out, open(os.path.join(OUT, "decls.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)

    # Heuristic xref (same format as build_xref.py) for every .lean file at the repo root.
    names, mods, ni, mi = [], [], {}, {}
    def nix(n):
        if n not in ni: ni[n] = len(names); names.append(n)
        return ni[n]
    def mix(m):
        if m not in mi: mi[m] = len(mods); mods.append(m)
        return mi[m]
    files = {}
    for rel in sorted(f for f in os.listdir(ROOT) if f.endswith(".lean")):
        raw = open(os.path.join(ROOT, rel), "rb").read()
        text = raw.decode("utf-8")
        here = [d for d in decls if d["file"] == rel]
        refs = []
        for l0, ln in enumerate(text.split("\n")):
            code = ln.split("--", 1)[0]
            ctx = next((d for d in reversed(here) if d["line"] <= l0 + 1), {"ns": ""})
            for m in TOK.finditer(code):
                if m.start() and code[m.start() - 1] == ".": continue
                t = m.group(0).rstrip(".")
                c0 = len(ln[:m.start()].encode("utf-16-le")) // 2
                c1 = c0 + len(t.encode("utf-16-le")) // 2
                target, mod = None, None
                e = resolve(t, ctx)
                if e and not e["anonInstance"] and not (e["file"] == rel and e["line"] == l0 + 1):
                    target, mod = e["name"], "project"
                elif t in ALIASES:
                    target, mod = ALIASES[t], "Mathlib"
                if target: refs.append([l0, c0, c1, nix(target), mix(mod)])
        files[rel] = {"sha256": hashlib.sha256(raw).hexdigest(),
                      "decls": [[nix(d["name"]), d["line"] - 1, d["endLine"] - 1] for d in here],
                      "refs": refs}
    json.dump({"version": 1, "heuristic": True, "names": names, "mods": mods, "files": files},
              open(os.path.join(OUT, "xref.json"), "w", encoding="utf-8"), separators=(",", ":"), ensure_ascii=False)
    print(f"decls: {len(out)} ({sum(1 for d in out if d['depth'] is not None)} reachable); xref: {len(files)} files, {sum(len(v['refs']) for v in files.values())} refs")


if __name__ == "__main__":
    main()
