---
id: ex_prime_gt
title: There is a prime above c (from Mathlib)
summary: 'This is where the simple generator borrows Euclid outright: a direct call to Mathlib''s `Nat.exists_infinite_primes`.'
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
  explain: PrimeGen.lean line 42.
- q: Is its statement Euclid's theorem?
  type: choice
  choices:
  - Yes, in the form ∀ c, ∃ prime p > c
  - 'No'
  answer: 0
  explain: Same content as the main theorem.
- q: Why is c + 1 passed instead of c?
  type: choice
  choices:
  - Mathlib's version gives c ≤ p; we need c < p
  - no reason
  answer: 0
  explain: The comment on PrimeGen.lean line 40 says so.
---
## Plain English

**Theorem (`ex_prime_gt`, PrimeGen.lean lines 39–45).** For every c there is p with [PrimeGt](#/node/PrimeGt) c p. It applies Mathlib's `Nat.exists_infinite_primes (c + 1)` (line 42). Used by [min_prime_gt](#/node/min_prime_gt), hence by [SimpleGen](#/node/SimpleGen).
