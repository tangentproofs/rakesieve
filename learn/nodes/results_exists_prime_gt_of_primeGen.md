---
id: results_exists_prime_gt_of_primeGen
title: Any prime generator proves Euclid (CONDITIONAL)
summary: '**The surprise:** this one *is* a genuine proof of infinitude, but conditional: if you hand it any prime
  generator at all, primes go on forever. Only strict increase is used; the ''no skipped prime'' half is not needed.'
review: draft
authors:
- grok-bot
caveats:
- Conditional on a PrimeGen instance. Every concrete instance in this repository is built with the help of Mathlib's
  `Nat.exists_infinite_primes`.
widgets:
- type: walkthrough
  title: The proof (PrimeGen.lean, lines 112-118)
  config:
    steps:
    - text: Take k = n + 1 steps
      lean: let k := n + 1
    - text: After k steps the prime has grown by at least k
      lean: PrimeGen.P_iterate_add_le g₀ k
      link: PrimeGen.P_iterate_add_le
    - text: The starting prime is at least 2 (it is prime)
      lean: Nat.Prime.two_le (P g₀).prop
    - text: Offer the prime after k steps as the witness; it is prime because generator values are primes
      lean: refine ⟨P (next^[k] g₀), (P (next^[k] g₀)).prop, ?_⟩
      link: NPrime
    - text: 'Arithmetic: 2 + (n + 1) > n'
      lean: omega
quiz:
- q: What is assumed?
  type: choice
  choices:
  - 'nothing: it is Euclid''s theorem outright'
  - a `PrimeGen` instance on some type α, and a state g₀
  - the Riemann hypothesis
  - that the RakeSieve is correct
  answer: 1
  explain: 'The signature is `{α : Type} [PrimeGen α] (g₀ : α) (n : Nat)` (Results.lean line 11).'
- q: Which field of `PrimeGen` does the proof use?
  type: choice
  choices:
  - '`hP''` (no skipped prime)'
  - '`hP_lt` (strict increase)'
  - both
  - neither
  answer: 1
  explain: '`PrimeGen.P_iterate_add_le` is proved by induction from `hP_lt` (PrimeGen.lean line 106).'
- q: Why can't `hP'` alone prove infinitude?
  type: choice
  choices:
  - it can
  - a generator that stays on the same prime forever satisfies `hP'`
  - '`hP''` is false for SimpleGen'
  answer: 1
  explain: If `next g = g`, there is nothing strictly between P g and P g, so `hP'` holds, but only one prime is
    ever produced. PrimeGen.lean lines 24–25 say this.
---
## Plain English

**Theorem (`results_exists_prime_gt_of_primeGen`, Results.lean lines 11–13). CONDITIONAL.** Let α be any type with a [PrimeGen](#/node/PrimeGen) instance, and g₀ any state. Then for every n there is a prime p > n.

The hypothesis is the `PrimeGen` instance (and a state g₀ to start from). Given those, the proof is elementary and does **not** use Mathlib's infinitude of primes: after k steps the prime has gone up by at least k ([PrimeGen.P_iterate_add_le](#/node/PrimeGen.P_iterate_add_le)), and the first prime is at least 2, so after n + 1 steps it is at least n + 3 > n.

So the honest reading is: *infinitely many primes follows from the existence of a generator whose primes strictly increase*. That moves the work into building a generator. The two concrete generators in this library ([SimpleGen](#/node/SimpleGen) and the RakeSieve) both use Mathlib's `Nat.exists_infinite_primes` to get built, so neither gives an independent proof of Euclid. See the [main theorem](#/node/results_exists_prime_gt_of_rakeSieve).

Only `hP_lt` (strict increase) is used. The docstring of [exists_prime_gt_of_primeGen](#/node/exists_prime_gt_of_primeGen) says why `hP'` alone would not do: a generator stuck on one prime skips nothing.
