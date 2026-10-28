# Trust: what has and hasn't been checked

This site **explains** a Lean library. It does not re-check it. Here is exactly what rests on what.

## Lean checking

| | rakesieve @ 36e7360 |
|---|---|
| Built by this site | **no** (by the owner's choice: no Lean builds on our servers) |
| Built publicly | **no public build found.** The repository's only workflow deploys GitHub Pages; there is no Lean CI |
| Reproducible build | not guaranteed: Mathlib is required at `master` and `lake-manifest.json` is git-ignored, so each build may get a different Mathlib |
| `#print axioms` | not run. We expect the three standard axioms (`propext`, `Classical.choice`, `Quot.sound`), as `aesop`, `omega` and `by_contra` typically use them; unverified |
| `sorry` | none in the 8 built files (grep). Three in `Rake_gte.lean`, which is not in `lakefile.lean` and is not imported |
| `axiom`, `native_decide`, `implemented_by`, `extern` | none found by grep |
| Mathlib's `Nat.exists_infinite_primes` | used by `RakeSieve.next` (RakeSieve.lean line 71) and `ex_prime_gt` (PrimeGen.lean line 42); see the [review](#/review) |

## This site's own data

- **Declarations were read from the source text, not from a Lean build.** `learn/tools/scan_decls.py` finds the declarations of the 8 built files with their exact lines and text. Every declaration carries `"extracted": false`. The "mentions" edges are matched by name and may miss dot-notation uses.
- **Anonymous instances** (for example `instance : PrimeGen (PrimeSieve α)`) are given the name Lean most likely generates, such as `instPrimeGenPrimeSieve`. Lean's actual generated names were not checked.
- **Identifier links on the source pages are matched by name** (`data/xref.json` is marked `"heuristic": true`). Project names link to their definition. A short hand-checked list of Mathlib and core names links to the Mathlib docs.
- **Explanations** are drafts by Grok Bot (`review: draft`), not reviewed by a human or a second model.

## To upgrade this page

Commit a `lake-manifest.json`, build on a capable machine, run `#print axioms` for each headline, add a Lean CI job, and replace the "no" entries above.
