#!/usr/bin/env python3
"""Keep the explainer's "File.lean lines a–b" references pointing at the Lean they were written about.

The nodes, pages and Start page cite Lean by line number. When the Lean changes, a bare number goes
stale silently (it still links somewhere, just to the wrong lines). So every reference is recorded in
learn/data/srcrefs.lock.json together with the text of the lines it cites:

  python3 tools/srcrefs_lock.py --check   # (npm test) fail if any reference's lines no longer read as locked
  python3 tools/srcrefs_lock.py --remap   # after a Lean change: re-point references whose text moved, then
                                          # rewrite nodes_src/, pages/, assets/app.js and the lock
  python3 tools/srcrefs_lock.py --lock    # record the current text for every reference (after writing new prose)

--remap looks for the locked text, line for line (whitespace-trimmed), first in the same file and then in
every .lean file (SimpleGen moved out of PrimeGen.lean, for example). If the text is gone, a reference that
covered a whole declaration follows that declaration (by name) and is listed for a human to re-read; any
other reference is reported as unresolved and the prose around it has to be rewritten by hand.
Run tools/write_nodes.py afterwards to regenerate nodes/*.md.
"""
import json, os, re, sys

LEARN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(LEARN)
LOCK = os.path.join(LEARN, "data", "srcrefs.lock.json")
# Where references are written (sources) and where they are rendered from (checked).
SOURCES = ["nodes_src", "pages", "assets/app.js"]
CHECKED = ["nodes", "pages", "assets/app.js"]
REF = re.compile(r"\b((?:[\w-]+/)*[A-Z]\w*\.lean)((?:</code>|`)?,?\s+lines?\s+)(\d+)(?:(\s*(?:-|–|—|to)\s*)(\d+))?")


def files_in(tops):
    for t in tops:
        p = os.path.join(LEARN, t)
        if os.path.isfile(p): yield p
        elif os.path.isdir(p):
            for f in sorted(os.listdir(p)):
                if f.endswith((".py", ".md")) and not f.startswith("_") or f == "_terms.py": yield os.path.join(p, f)


def lean_files():
    return sorted(f for f in os.listdir(ROOT) if f.endswith(".lean"))


_cache = {}
def lines(f):
    if f not in _cache:
        p = os.path.join(ROOT, f)
        _cache[f] = open(p, encoding="utf-8").read().split("\n") if os.path.exists(p) else None
    return _cache[f]


def text(f, a, b):
    ls = lines(f)
    if ls is None or a < 1 or b > len(ls) or b < a: return None
    return [x.strip() for x in ls[a - 1:b]]


def refs(path):
    src = open(path, encoding="utf-8").read()
    if path.endswith(".js"): src = re.sub(r"(?m)^\s*//.*$", "", src)  # code comments give examples, not references
    for m in REF.finditer(src):
        a = int(m.group(3)); b = int(m.group(5)) if m.group(5) else a
        yield m.group(1), a, b


key = lambda f, a, b: f"{f}:{a}-{b}"


def load():
    return json.load(open(LOCK, encoding="utf-8")) if os.path.exists(LOCK) else {}


def save(lock):
    json.dump(dict(sorted(lock.items())), open(LOCK, "w", encoding="utf-8"), indent=1, ensure_ascii=False)


def decl_at(f, a, b):
    """The declaration whose range is exactly [a, b], or which starts at a (a statement sub-range)."""
    for d in json.load(open(os.path.join(LEARN, "data", "decls.json"), encoding="utf-8")):
        if d["file"] == f and d["line"] == a and b <= d["endLine"]: return d["name"], d["endLine"] == b
    return None, None


def lock_all():
    lock = {}
    for p in files_in(SOURCES):
        for f, a, b in refs(p):
            t = text(f, a, b)
            if t is None: sys.exit(f"{os.path.relpath(p, LEARN)}: {f} lines {a}-{b} is outside the file")
            name, whole = decl_at(f, a, b)
            lock[key(f, a, b)] = {"text": t, **({"decl": name, "whole": whole} if name else {})}
    save(lock)
    print(f"locked {len(lock)} references")


def check():
    lock, bad = load(), []
    for p in files_in(CHECKED):
        for f, a, b in refs(p):
            k, where = key(f, a, b), os.path.relpath(p, LEARN)
            if k not in lock: bad.append(f"{where}: {f} lines {a}-{b} is not in data/srcrefs.lock.json (run tools/srcrefs_lock.py --lock after checking it)")
            elif text(f, a, b) != lock[k]["text"]: bad.append(f"{where}: {f} lines {a}-{b} no longer reads as when it was written (run tools/srcrefs_lock.py --remap)")
    if bad: print("FAIL\n" + "\n".join(sorted(set(bad)))); sys.exit(1)
    print("srcrefs_lock: ok")


def find(t, prefer, near):
    hits = []
    for f in [prefer] + [x for x in lean_files() if x != prefer]:
        ls = lines(f)
        if ls is None: continue
        s = [x.strip() for x in ls]
        for i in range(len(s) - len(t) + 1):
            if s[i:i + len(t)] == t: hits.append((f, i + 1))
        if hits and f == prefer: break
    if not hits: return None
    same = [h for h in hits if h[0] == prefer]
    if same: return min(same, key=lambda h: abs(h[1] - near))
    return hits[0] if len(hits) == 1 else None


def remap():
    lock, new, moved, review, lost = load(), {}, {}, [], []
    decls = {d["name"]: d for d in json.load(open(os.path.join(LEARN, "data", "decls.json"), encoding="utf-8"))}
    for k, e in lock.items():
        f, rng = k.rsplit(":", 1); a, b = map(int, rng.split("-"))
        if text(f, a, b) == e["text"]: new[k] = e; continue
        hit = find(e["text"], f, a)
        if hit:
            nf, na = hit; nb = na + b - a
        elif e.get("decl") in decls:
            d = decls[e["decl"]]; nf, na = d["file"], d["line"]
            nb = d["endLine"] if e["whole"] else na + b - a
            review.append(f"{k} -> {nf}:{na}-{nb} (followed {e['decl']}; its text changed, re-read the prose)")
        else:
            lost.append(k); continue
        moved[k] = (nf, na, nb)
        new[key(nf, na, nb)] = {**e, "text": text(nf, na, nb)}
    def sub(m):
        f, a = m.group(1), int(m.group(3)); b = int(m.group(5)) if m.group(5) else a
        if key(f, a, b) not in moved: return m.group(0)
        nf, na, nb = moved[key(f, a, b)]
        name = m.group(1).replace(os.path.basename(f), nf) if nf != f else m.group(1)
        if m.group(5): return f"{name}{m.group(2)}{na}{m.group(4)}{nb}"
        return f"{name}{m.group(2)}{na}" + (f"–{nb}" if nb != na else "")
    for p in files_in(SOURCES):
        s = open(p, encoding="utf-8").read(); s2 = REF.sub(sub, s)
        if s2 != s: open(p, "w", encoding="utf-8").write(s2)
    save(new)
    print(f"remapped {len(moved)} of {len(lock)} locked references")
    for r in review: print("review:", r)
    for k in lost: print("UNRESOLVED (text gone; rewrite the prose, then --lock):", k)
    if lost: sys.exit(2)


if __name__ == "__main__":
    {"--check": check, "--remap": remap, "--lock": lock_all}[sys.argv[1] if len(sys.argv) > 1 else "--check"]()
