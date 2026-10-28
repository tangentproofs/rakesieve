---
id: results_three_mem_R_two
title: 3 survives sieving by 2
summary: 'A fact this small is a headline because it is the sieve''s base case: after crossing out multiples of
  2, the number 3 is still there. Lean checks it by computation (`decide`), not by reasoning.'
review: draft
authors:
- grok-bot
widgets:
- type: walkthrough
  title: The proof (PrimeSieve.lean, lines 19-27)
  config:
    steps:
    - text: 3 ≥ 2, by computation
      lean: refine ⟨by decide, ?_⟩
    - text: Any prime q ≤ 2 is at least 2, so q = 2
      lean: have := Nat.Prime.two_le hq'
    - text: 2 does not divide 3, by computation
      lean: decide
quiz:
- q: Which set is R 2?
  type: choice
  choices:
  - all numbers ≥ 2
  - the odd numbers ≥ 3
  - the primes
  - the even numbers
  answer: 1
  explain: R 2 = { n | n ≥ 2 ∧ ∀ q ≤ 2, q prime → ¬ q ∣ n }. The only prime ≤ 2 is 2, so these are the n ≥ 2 that
    are odd.
- q: How does Lean check `¬ 2 ∣ 3`?
  type: choice
  choices:
  - '`native_decide`'
  - '`decide` (evaluated by the kernel)'
  - an axiom
  answer: 1
  explain: 'PrimeSieve.lean line 27: `decide`. That is ordinary kernel evaluation, with no extra trust.'
- q: Where is this fact used?
  type: choice
  choices:
  - As the base case for RakeSieve.init's proof that its candidate 3 is in R 2
  - Nowhere
  - In Main.lean only
  answer: 0
  explain: 'RakeSieve.lean line 50: `simpa [p] using three_mem_R_two`.'
---
## Plain English

**R stands for *residue*.** R p is the set of numbers ≥ 2 that no prime ≤ p divides: what is left after crossing out the multiples of every prime up to p ([R](#/node/R)). For example, R 2 is the odd numbers from 3 up.

**Theorem (`results_three_mem_R_two`, Results.lean lines 5–6).** 3 ∈ R 2: the number 3 is at least 2 and is not divisible by any prime q ≤ 2.

[R](#/node/R) P is the set of numbers that survive a sieve once every prime up to P has crossed out its multiples. So R 2 is the odd numbers from 3 up, and this theorem says 3 is one of them.

Why it matters: the RakeSieve starts with prime p = 2 and candidate c = 3 ([RakeSieve.init](#/node/RakeSieve.init)). Every sieve state must prove that its candidate lies in R p; for the start state that proof is this theorem (RakeSieve.lean line 50). It was moved out of `RakeSieve.init` into PrimeSieve.lean so that any sieve can reuse it (issue #3).
