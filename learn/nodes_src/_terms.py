# Shared wording for terms that many nodes use. Files starting with "_" hold no nodes;
# tools/write_nodes.py skips them, and the node files import from here.
NODES = []

# R is the sieve's central set. Every node that writes "R" must say what it is before the first use
# (tools/test_terms.mjs checks this), so a reader who lands on any page is never left guessing.
R_NOTE = ("**R stands for *residue*.** R p is the set of numbers ≥ 2 that no prime ≤ p divides: "
          "what is left after crossing out the multiples of every prime up to p ([R](#/node/R)). "
          "For example, R 2 is the odd numbers from 3 up.")

# Body opening for nodes that mention R.
PLAIN_R = "\n## Plain English\n\n" + R_NOTE + "\n\n"
