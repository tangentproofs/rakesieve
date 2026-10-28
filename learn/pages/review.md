# Review: what does RakeSieve actually prove?

*Reviewed 28 October 2026 by Grok Bot, for Michal Wallace, by reading the source at commit 1557758 (PR #5, "prove the rake never runs empty without Euclid"). This site did not build the Lean. The build, the no-Euclid check and `#print axioms` were run on the tcode server for PR #5 (see [Trust](#/trust)). A second, independent model audit is still to do.*

**The short answer:** Lean checks that the RakeSieve, stepped from its start state, produces each next prime with none skipped, and that it reaches every prime. Both are now stated as named theorems. The sieve also proves for itself that it never runs empty. Its witness is the term c + d, where d is the rake's period, the product of the primes sifted so far. So infinitude of primes follows as a corollary of the algorithm, with no use of Mathlib's infinitude theorem. The idea is still Euclid's (c + p# plays the part of p# + 1), but the argument is no longer circular.

| | |
|---|---|
| Repo, commit | [tangentproofs/rakesieve](https://github.com/tangentproofs/rakesieve) @ 1557758 (PR #5, 28 Oct 2026) |
| Lean / Mathlib | `leanprover/lean4:v4.35.0-rc1`; Mathlib `master`, **not pinned** (`lake-manifest.json` is git-ignored). PR #5 was built against Mathlib `09a9e06e` |
| Size | 10 built files, about 1,400 lines (plus `Rake_gte.lean` and `OldMain.lean`, not built) |
| `sorry` | none in the built files. 3 in `Rake_gte.lean`, which `lakefile.lean` does not list and nothing imports |
| Axioms | `propext`, `Classical.choice`, `Quot.sound` for each RakeSieve headline (`#print axioms`, PR #5 build) |
| Mathlib's infinitude of primes | **not used** by any headline. NoEuclidCheck.lean walks each headline's full dependency closure |
| Lean CI | none. The only workflow deploys the Pages site |

## The theorems in Results.lean

Below, R stands for *residue*: [R](#/node/R) p is the set of numbers ≥ 2 that no prime ≤ p divides, what survives after crossing out the multiples of every prime up to p.

| Theorem | Statement | Reading |
|---|---|---|
| [results_rakeSieve_never_empty](#/node/results_rakeSieve_never_empty) | every state has a rake term not divisible by its candidate c | the sieve can always take another step; the witness is c + d |
| [results_rakeSieve_step](#/node/results_rakeSieve_step) | one step makes c the new prime; c is prime, c > p, no prime between | **sieve correctness**, per step |
| [results_rakeSieve_emits_every_prime](#/node/results_rakeSieve_emits_every_prime) | ∀ prime q, ∃ k, the prime after k steps from `init` is q | **completeness**: every prime appears |
| [results_exists_prime_gt_of_rakeSieve](#/node/results_exists_prime_gt_of_rakeSieve) | ∀ n, ∃ p, p prime ∧ n < p | **corollary**: Euclid's theorem, proved through the sieve without Mathlib's Euclid |
| [results_exists_prime_gt_of_primeGen](#/node/results_exists_prime_gt_of_primeGen) | [PrimeGen α] → ∀ n, ∃ prime p > n | **CONDITIONAL**: any prime generator implies infinitely many primes |
| [results_three_mem_R_two](#/node/results_three_mem_R_two) | 3 ∈ R 2 | base case of the sieve |
| [results_three_le_of_mem_R_two](#/node/results_three_le_of_mem_R_two) | ∀ r ∈ R 2, 3 ≤ r | base case of the sieve |

The old `results_exists_prime_gt_of_simpleGen` is gone from Results.lean. It survives as [simpleGen_exists_prime_gt](#/node/simpleGen_exists_prime_gt) in SimpleGen.lean, marked circular.

## Finding 1 (resolved by PR #5): the sieve's correctness is now stated

The earlier review found that no named theorem said the sieve was correct. The headline only stated Euclid's theorem, and the sieve's guarantees were hidden in the instance [`PrimeGen (PrimeSieve α)`](#/node/instPrimeGenPrimeSieve). It suggested adding a theorem that every prime appears. PR #5 adds three: [never empty](#/node/results_rakeSieve_never_empty), [each step](#/node/results_rakeSieve_step) and [every prime](#/node/results_rakeSieve_emits_every_prime). The last uses a new generic lemma, [PrimeGen.exists_iterate_P_eq](#/node/PrimeGen.exists_iterate_P_eq).

## Finding 2 (resolved by PR #5): infinitude is no longer circular

Before PR #5, `RakeSieve.next` called Mathlib's `Nat.exists_infinite_primes` to show that removing the multiples of c left the rake non-empty, which `RakeMap.rem` requires. So the infinitude theorem used infinitude of primes inside every step.

Now the rake supplies its own witness ([RakeSieve.survivor](#/node/RakeSieve.survivor), RakeSieve.lean lines 72–82):

- c is a term of the rake, and one period later the rake produces c + d ([Rake.term_add_len](#/node/Rake.term_add_len));
- each state carries a new invariant, `hdfac`: every prime factor of the period d is ≤ p. It holds at `init`, where d = 2, and every step keeps it, because the step multiplies d by the new prime ([RakeMap.rem_d](#/node/RakeMap.rem_d));
- c is a prime above p, so c ∤ d, and therefore c ∤ c + d.

**Honest reading.** This is Euclid's argument. The period d is p#, the product of the primes up to p, so c + d is Euclid's p# + 1 in the sieve's own terms. What changed is that the argument is carried by the data structure, as an invariant that the sieve maintains, instead of being imported as a theorem. `hdfac` is not a smuggled hypothesis. Like `hCinR` and `hRmin`, it is a structure field proved at `init` and re-proved by `next`.

**Machine check.** NoEuclidCheck.lean walks the full constant-dependency closure of every headline, plus `RakeSieve.next`, `survivor` and `init`, through Mathlib and core. It fails the build if the closure reaches anything declared in `Mathlib.Data.Nat.Prime.Infinite` or a deny-list of infinitude results. As a control, it must find `Nat.exists_infinite_primes` in `simpleGen_exists_prime_gt`. Both checks passed in the PR #5 build (output on the [Trust](#/trust) page).

The proofs still use ordinary Mathlib facts about primes, such as `Nat.Prime.dvd_mul` and `Nat.exists_prime_and_dvd`, and they use `Nat.find`. None of these involve infinitude.

## Finding 3: smaller wording points

- `RakeMap`'s docstring says "1-to-1 mapping" and its field is called `hbij`, but the field states only that the rake's terms are exactly `{ n | pred n }` (RakeMap.lean lines 6–9). Injectivity is never stated or needed.
- `Rake.partition`'s docstring speaks of "the guarantee that term (n) < term n+1". There is no such guarantee, as the docstring of `sorted_min_term_zero` (Rake.lean lines 187–191) itself explains. Only "term 0 is the minimum" is proved and used.
- The README's growth table (1, 2, 8, 48, 480, … sequences) and its remarks about a lazy, sub-linear variant are documentation, not formalized.
- Lean does not state that the period d *equals* p#, only that its prime factors are ≤ p. The equality is true of the code but is not needed.
- Issue #3 (extract the facts about 3 and R 2) appears to be done by 37c37c7 but is still open. Issue #2 (queue primes below p²) is on the unmerged PR #4.

## What is solid

- The generic sieve argument (PrimeSieve.lean): if a sieve's candidate is the least element of R P, then it is prime and is the next prime after P. That is proved once for every sieve.
- The rake operations (Rake.lean, RakeMap.lean): partitioning keeps the same terms, and removal drops exactly the multiples of j and multiplies the period by j, with full proofs and no `sorry`.
- Each `RakeSieve` state carries proofs that its rake lists exactly R p, that its candidate is the least element, and that its period has no prime factor above p. An incorrect state cannot be built, and the sieve can always take another step.
