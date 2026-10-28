---
id: ex_prime_gt
title: There is a prime above c (from Mathlib)
summary: This is where the reference generator borrows Euclid outright, with a direct call to Mathlib's `Nat.exists_infinite_primes`.
  That is why it lives in SimpleGen.lean, off the RakeSieve's path.
review: draft
authors:
- grok-bot
quiz:
- q: Which Mathlib theorem does it call?
  type: choice
  choices:
  - '`Nat.exists_infinite_primes`'
  - '`Nat.find`'
  answer: 0
  explain: SimpleGen.lean line 19.
- q: Is its statement Euclid's theorem?
  type: choice
  choices:
  - Yes, in the form ∀ c, ∃ prime p > c
  - 'No'
  answer: 0
  explain: Same content as the infinitude corollary.
- q: Why is c + 1 passed instead of c?
  type: choice
  choices:
  - Mathlib's version gives c ≤ p; we need c < p
  - no reason
  answer: 0
  explain: The comment on SimpleGen.lean line 17 says so.
---
## Plain English

**Theorem (`ex_prime_gt`, SimpleGen.lean lines 16–22).** For every c there is p with [PrimeGt](#/node/PrimeGt) c p. It applies Mathlib's `Nat.exists_infinite_primes (c + 1)` (SimpleGen.lean line 19). Used by [min_prime_gt](#/node/min_prime_gt), hence by [SimpleGen](#/node/SimpleGen). The RakeSieve does not use it: SimpleGen.lean is not imported by Results.lean.
