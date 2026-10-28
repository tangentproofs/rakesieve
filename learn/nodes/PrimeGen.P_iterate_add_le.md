---
id: PrimeGen.P_iterate_add_le
title: After k steps the prime has grown by at least k
summary: 'Strict increase on natural numbers is already a growth guarantee: each step adds at least 1, so k steps
  add at least k.'
review: draft
authors:
- grok-bot
quiz:
- q: What does `next^[k] g` mean?
  type: choice
  choices:
  - next applied k times to g
  - the k-th power of next's value
  answer: 0
  explain: Mathlib's function iteration notation.
- q: What proof technique?
  type: choice
  choices:
  - induction on k
  - contradiction
  - '`decide`'
  answer: 0
  explain: PrimeGen.lean lines 102–108.
- q: Does it need `hP'`?
  type: choice
  choices:
  - 'No'
  - 'Yes'
  answer: 0
  explain: Only strict increase.
---
## Plain English

**Theorem (`PrimeGen.P_iterate_add_le`, PrimeGen.lean lines 100–108).** For any state g and k, P g + k ≤ P (next^[k] g), where next^[k] is next applied k times.

Induction on k, using `hP_lt` at each step. Used by [exists_prime_gt_of_primeGen](#/node/exists_prime_gt_of_primeGen).
