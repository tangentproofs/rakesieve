---
id: SimpleGen.start
title: 'SimpleGen.start: begin at 2'
summary: '**The surprise:** the one place the simple generator says where primes begin; the PrimeGen class itself
  does not.'
review: draft
authors:
- grok-bot
quiz:
- q: What is the start prime?
  type: choice
  choices:
  - '2'
  - '3'
  - '1'
  answer: 0
  explain: PrimeGen.lean line 62.
- q: What is its `c` field's number?
  type: choice
  choices:
  - '3'
  - '5'
  answer: 0
  explain: The least prime above 2.
- q: Why is the start not part of PrimeGen?
  type: choice
  choices:
  - by design; see the class docstring
  - an oversight
  answer: 0
  explain: PrimeGen.lean lines 16–18.
---
## Plain English

`SimpleGen.start := { p := ⟨2, Nat.prime_two⟩, c := min_prime_gt 2 }` (PrimeGen.lean lines 61–62): prime 2, next prime 3. Used by [results_exists_prime_gt_of_simpleGen](#/node/results_exists_prime_gt_of_simpleGen). See [SimpleGen](#/node/SimpleGen) and [min_prime_gt](#/node/min_prime_gt).
