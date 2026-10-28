#!/usr/bin/env python3
"""Write learn/nodes/<id>.md from the node data in learn/nodes_src/*.py (keeps the YAML valid).

  python3 tools/write_nodes.py          # write nodes/, and delete node files no source defines any more
  python3 tools/write_nodes.py --check  # (npm test) fail if nodes/ is not what nodes_src/ generates
"""
import importlib.util, os, sys, yaml
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = os.path.join(SITE, "nodes")
check = "--check" in sys.argv
sys.path.insert(0, os.path.join(SITE, "nodes_src"))  # node files share wording from nodes_src/_terms.py
want = {}
for f in sorted(os.listdir(os.path.join(SITE, "nodes_src"))):
    if not f.endswith(".py") or f.startswith("_"): continue
    spec = importlib.util.spec_from_file_location(f[:-3], os.path.join(SITE, "nodes_src", f))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    for n in m.NODES:
        fm = {"id": n["id"], "title": n["title"], "summary": n["summary"], "review": "draft", "authors": ["grok-bot"]}
        if n["caveats"]: fm["caveats"] = n["caveats"]
        if n["widgets"]: fm["widgets"] = n["widgets"]
        fm["quiz"] = n["quiz"]
        assert n["id"] + ".md" not in want, f"node {n['id']} is defined twice"
        want[n["id"] + ".md"] = "---\n" + yaml.safe_dump(fm, allow_unicode=True, sort_keys=False, width=110) + "---\n" + n["body"].lstrip("\n")
have = {f for f in os.listdir(out) if f.endswith(".md")}
if check:
    bad = sorted(f for f in want if f not in have or open(os.path.join(out, f), encoding="utf-8").read() != want[f]) + sorted(have - set(want))
    if bad: sys.exit("FAIL: nodes/ is stale; run python3 tools/write_nodes.py: " + ", ".join(bad))
    print(f"write_nodes: ok ({len(want)} nodes)"); sys.exit()
for f, text in want.items(): open(os.path.join(out, f), "w", encoding="utf-8").write(text)
for f in have - set(want): os.remove(os.path.join(out, f)); print("removed stale", f)
print("ok")
