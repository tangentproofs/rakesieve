# Trust: what has and hasn't been checked

This site **explains** a Lean library. It does not re-check it. Here is exactly what rests on what.

## Lean checking

| | rakesieve @ 1557758 (PR #5) |
|---|---|
| Built by this site | **no** (by the owner's choice: no Lean builds on our servers for the explainer) |
| Built for PR #5 | **yes**, once, on the tcode server: `lake build Results SimpleGen NoEuclidCheck leansieve`, 1719 jobs, success. Toolchain `leanprover/lean4:v4.35.0-rc1`, Mathlib pinned locally to `09a9e06e` |
| Built publicly | **no public build.** The repository's only workflow deploys GitHub Pages; there is no Lean CI |
| Reproducible build | not guaranteed: the lakefile requires Mathlib at `master` and `lake-manifest.json` is git-ignored, so the `09a9e06e` pin above is not committed |
| `#print axioms` | `propext`, `Classical.choice`, `Quot.sound` (the standard three) for `results_rakeSieve_never_empty`, `results_rakeSieve_step`, `results_rakeSieve_emits_every_prime` and `results_exists_prime_gt_of_rakeSieve` (PR #5 build) |
| `sorry` | none in the 10 built files (grep). Three in `Rake_gte.lean`, which is not in `lakefile.lean` and is not imported |
| `axiom`, `native_decide`, `implemented_by`, `extern` | none found by grep |
| Mathlib's infinitude of primes | **not reachable from any headline** (NoEuclidCheck, below). Used only by the circular reference generator in SimpleGen.lean (`ex_prime_gt`, SimpleGen.lean line 19), which Results.lean does not import |

## The no-Euclid check (NoEuclidCheck.lean)

NoEuclidCheck.lean is a `lean_lib`, so building it runs the check. `#assert_no_euclid` walks the full constant-dependency closure of each named theorem through Mathlib and core. It fails the build if the closure contains any constant declared in `Mathlib.Data.Nat.Prime.Infinite` (the home of `Nat.exists_infinite_primes`) or any name on a deny-list of infinitude results. `#assert_uses_euclid` is the control: it must *find* Euclid in the circular `simpleGen_exists_prime_gt`, so a walk that saw nothing could not pass silently. Output of the PR #5 build:

```
ok: results_rakeSieve_never_empty: 4555 constants in its dependency closure, none from Mathlib.Data.Nat.Prime.Infinite or the deny-list
ok: results_rakeSieve_step: 4558 constants …
ok: results_rakeSieve_emits_every_prime: 5106 constants …
ok: results_exists_prime_gt_of_rakeSieve: 5084 constants …
ok: results_three_mem_R_two: 1606 constants …
ok: results_three_le_of_mem_R_two: 1832 constants …
ok: RakeSieve.next: 4526 constants …
ok: RakeSieve.survivor: 3356 constants …
ok: RakeSieve.init: 4496 constants …
control ok: simpleGen_exists_prime_gt depends on Euclid via [Nat.exists_infinite_primes] (3335 constants in closure)
```

The PR also reports that `Mathlib.Data.Nat.Prime.Infinite` is not even transitively imported by `Results`. These outputs are copied from the PR; this site did not re-run them.

**What the check does not say.** It shows that no *infinitude theorem* is used. It does not show that the argument is new: the survivor c + d is Euclid's p# + 1 idea, carried by the sieve's own data (see the [review](#/review)).

## This site's own data

- **Declarations were read from the source text, not from a Lean build.** `learn/tools/scan_decls.py` reads the list of built modules from `lakefile.lean` and finds their declarations with exact lines and text. Every declaration carries `"extracted": false`. The "mentions" edges are matched by name. Dot-notation uses such as `s.survivor` are resolved when exactly one declaration has that last name, and may still miss some.
- **Line references are locked.** Every "File.lean lines a–b" on this site is recorded in `learn/data/srcrefs.lock.json` with the text of those lines. `npm test` fails if the Lean under a reference changes. `tools/srcrefs_lock.py --remap` moves references whose text moved, and lists the ones whose text is gone so they can be rewritten by hand.
- **Anonymous instances** (for example `instance : PrimeGen (PrimeSieve α)`) are given the name Lean most likely generates, such as `instPrimeGenPrimeSieve`. Lean's actual generated names were not checked.
- **Identifier links on the source pages are matched by name** (`data/xref.json` is marked `"heuristic": true`). Project names link to their definition. A short hand-checked list of Mathlib and core names links to the Mathlib docs.
- **Explanations** are drafts by Grok Bot (`review: draft`), not reviewed by a human or a second model.

## To upgrade this page

Commit a `lake-manifest.json`, add a Lean CI job that builds `NoEuclidCheck` and prints the axioms, and replace the "no" entries above.
