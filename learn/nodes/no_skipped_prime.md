---
id: no_skipped_prime
title: No prime lies between P and the candidate
summary: '**The surprise:** the proof is three lines of idea: a prime above P has no small prime factor, so it survives
  the sieve, so it is at least the least survivor C.'
review: draft
authors:
- grok-bot
quiz:
- q: Why is a prime q > P in R P?
  type: choice
  choices:
  - its only prime factor is q itself, which is > P
  - because q is odd
  - by definition of prime
  answer: 0
  explain: '`Nat.prime_dvd_prime_iff_eq` turns p ∣ q into p = q.'
- q: Which driver field closes the argument?
  type: choice
  choices:
  - '`hCinR`'
  - '`hRmin`'
  answer: 1
  explain: C is ≤ everything in R P.
- q: Is this the same as `nosk' (P g) (C g)`?
  type: choice
  choices:
  - 'Yes'
  - 'No'
  answer: 0
  explain: The statement is `¬ ∃ q, Nat.Prime q ∧ P g < q ∧ q < C g`.
---
## Plain English

**Theorem (`no_skipped_prime`, PrimeSieve.lean lines 133–151).** For any driven sieve state g there is no prime q with P g < q < C g.

Proof: such a q is ≥ 2, and any prime p ≤ P dividing q would equal q (both prime), but q > P. So q ∈ [R](#/node/R) (P g). The driver's `hRmin` then gives C g ≤ q, contradicting q < C g.

This is the proof of [nosk'](#/node/nosk') that a sieve step needs, and gives `hP'` in the [driver instance](#/node/instPrimeGenPrimeSieve).
