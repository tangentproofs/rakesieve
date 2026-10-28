# Review: what does RakeSieve actually prove?

*Reviewed 28 October 2026 by Grok Bot, for Michal Wallace, by reading the source of `main` at commit 36e7360. The Lean was not built for this review. A second, independent model audit is still to do.*

**The short answer:** the Lean proves a real and pleasant fact, that the RakeSieve, stepped from its start state, produces each next prime with none skipped. But **no named theorem states that**. The headline theorem, `results_exists_prime_gt_of_rakeSieve`, states Euclid's theorem (there is always a bigger prime) and uses Mathlib's own proof of Euclid along the way. Nothing is wrong in the Lean; the issue is what a reader might think the headline says.

| | |
|---|---|
| Repo, commit | [tangentproofs/rakesieve](https://github.com/tangentproofs/rakesieve) @ 36e7360 (24 Sep 2026); last Lean change 37c37c7 (16 Sep 2026) |
| Lean / Mathlib | `leanprover/lean4:v4.35.0-rc1`; Mathlib `master`, **not pinned** (`lake-manifest.json` is git-ignored) |
| Size | 8 built files, about 1,300 lines (plus `Rake_gte.lean` and `OldMain.lean`, not built) |
| `sorry` | none in the built files. 3 in `Rake_gte.lean`, which `lakefile.lean` does not list and nothing imports |
| `axiom`, `native_decide`, `implemented_by` | none found by grep. `decide` (ordinary kernel evaluation) in PrimeSieve.lean lines 19–27 |
| Lean CI | none. The only workflow deploys the Pages site |

## The five theorems in Results.lean

| Theorem | Statement | Reading |
|---|---|---|
| [results_exists_prime_gt_of_rakeSieve](#/node/results_exists_prime_gt_of_rakeSieve) | ∀ n, ∃ p, p prime ∧ n < p | **Euclid's theorem.** RakeSieve appears only in the proof |
| [results_exists_prime_gt_of_simpleGen](#/node/results_exists_prime_gt_of_simpleGen) | same | Euclid again, via the brute-force generator |
| [results_exists_prime_gt_of_primeGen](#/node/results_exists_prime_gt_of_primeGen) | [PrimeGen α] → ∀ n, ∃ prime p > n | **CONDITIONAL**: any prime generator implies infinitely many primes |
| [results_three_mem_R_two](#/node/results_three_mem_R_two) | 3 ∈ R 2 | base case of the sieve |
| [results_three_le_of_mem_R_two](#/node/results_three_le_of_mem_R_two) | ∀ r ∈ R 2, 3 ≤ r | base case of the sieve |

## Finding 1: the headline statement is Euclid, not sieve correctness

Results.lean lines 19–21 state `∀ n, ∃ p, Nat.Prime p ∧ n < p`. A reader could prove this statement in one line from Mathlib, so on its own it certifies nothing about the sieve. The interesting fact, that the sieve's outputs are consecutive primes, is checked by Lean (it is needed to build the proof term) but lives in the instance [`PrimeGen (PrimeSieve α)`](#/node/instPrimeGenPrimeSieve) (PrimeSieve.lean lines 218–242), not in a theorem anyone can cite.

**Suggestion (not done):** add theorems that state sieve correctness directly, for example that the k-th prime produced from `RakeSieve.init` is the k-th prime, or that every prime appears among `primes ⟨RakeSieve.init⟩ n` for some n. Both follow from `hP'`, `hP_lt` and the start prime 2 by a short induction.

## Finding 2: the infinitude proofs use Mathlib's infinitude

- `RakeSieve.next` calls `Nat.exists_infinite_primes` (RakeSieve.lean line 71) to show that removing the multiples of c leaves the rake non-empty, which `RakeMap.rem` requires.
- `SimpleGen` calls it too, through `ex_prime_gt` (PrimeGen.lean line 42).

So `results_exists_prime_gt_of_rakeSieve` and `…_of_simpleGen` are not independent proofs of Euclid. The README and the [project home](../) describe them as "infinitude via RakeSieve"; that is accurate about the route, but it should not be read as "a new proof". Only `results_exists_prime_gt_of_primeGen` is a genuine (conditional) derivation, and it uses only strict increase.

## Finding 3: smaller wording points

- `RakeMap`'s docstring says "1-to-1 mapping" and its field is called `hbij`, but the field states only that the rake's terms are exactly `{ n | pred n }` (RakeMap.lean lines 6–9). Injectivity is never stated or needed.
- `Rake.partition`'s docstring speaks of "the guarantee that term (n) < term n+1"; there is no such guarantee, as the docstring of `sorted_min_term_zero` (Rake.lean lines 180–184) itself explains. Only "term 0 is the minimum" is proved and used.
- The README's growth table (1, 2, 8, 48, 480, … sequences) and its remarks about a lazy, sub-linear variant are documentation, not formalized.
- Issue #3 (extract the facts about 3 and R 2) appears to be done by 37c37c7 but is still open. Issue #2 (queue primes below p²) is on the unmerged PR #4.

## What is solid

- The generic sieve argument (PrimeSieve.lean): if a sieve's candidate is the least element of R P, then it is prime and is the next prime after P. That is proved once for every sieve.
- The rake operations (Rake.lean, RakeMap.lean): partitioning keeps the same terms, and removal drops exactly the multiples of j, with full proofs, no `sorry`.
- Each `RakeSieve` state carries proofs that its rake lists exactly R p and that its candidate is the least element, so an incorrect state cannot be built.
