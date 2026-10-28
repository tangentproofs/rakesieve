---
id: r_gt_p
title: Everything in R P is bigger than P
summary: 'This is why sieving works at all: a number ≤ P that is at least 2 has a prime factor ≤ P, so it cannot
  survive. Every survivor, including the next candidate, is beyond P.'
review: draft
authors:
- grok-bot
quiz:
- q: Why can't 4 be in R 5?
  type: choice
  choices:
  - 4 is even, and 2 ≤ 5 is a prime dividing it
  - 4 < 5 is not allowed by definition
  - 4 is in R 5
  answer: 0
  explain: R 5 requires that no prime ≤ 5 divide n; 2 divides 4. In general any 2 ≤ r ≤ p has a prime factor ≤ p.
- q: Which Mathlib fact does the proof use?
  type: choice
  choices:
  - every n ≠ 1 has a prime factor
  - infinitely many primes
  - unique factorization
  answer: 0
  explain: '`Nat.exists_prime_and_dvd` (PrimeSieve.lean line 48).'
- q: Does the lemma need p to be prime?
  type: choice
  choices:
  - 'Yes'
  - No, it holds for every natural number p
  answer: 1
  explain: 'The statement is `∀ p : Nat, ∀ r ∈ R p, r > p`.'
---
## Plain English

**R stands for *residue*.** R p is the set of numbers ≥ 2 that no prime ≤ p divides: what is left after crossing out the multiples of every prime up to p ([R](#/node/R)). For example, R 2 is the odd numbers from 3 up.

**Lemma (`r_gt_p`, PrimeSieve.lean lines 40–53).** For every r ∈ [R](#/node/R) p, r > p.

Proof: suppose r ≤ p. Since r ≥ 2, r has some prime factor f (Mathlib's `Nat.exists_prime_and_dvd`), and f ≤ r ≤ p. But membership in R p says no prime ≤ p divides r. Contradiction.

It gives [c_gt_p](#/node/c_gt_p) (the candidate is beyond the current prime) and is used in the RakeSieve's step to show the candidate grows.
