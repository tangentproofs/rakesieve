#!/usr/bin/env python3
"""Write learn/nodes/<id>.md from the node data in learn/nodes_src/*.py (keeps the YAML valid)."""
import importlib.util, os, yaml
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = os.path.join(SITE, "nodes")
for f in sorted(os.listdir(os.path.join(SITE, "nodes_src"))):
    if not f.endswith(".py"): continue
    spec = importlib.util.spec_from_file_location(f[:-3], os.path.join(SITE, "nodes_src", f))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    for n in m.NODES:
        fm = {"id": n["id"], "title": n["title"], "summary": n["summary"], "review": "draft", "authors": ["grok-bot"]}
        if n["caveats"]: fm["caveats"] = n["caveats"]
        if n["widgets"]: fm["widgets"] = n["widgets"]
        fm["quiz"] = n["quiz"]
        text = "---\n" + yaml.safe_dump(fm, allow_unicode=True, sort_keys=False, width=110) + "---\n" + n["body"].lstrip("\n")
        open(os.path.join(out, n["id"] + ".md"), "w", encoding="utf-8").write(text)
print("ok")
