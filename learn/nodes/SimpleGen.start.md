---
id: SimpleGen.start
title: 'SimpleGen.start: begin at 2'
summary: This is the one place the simple generator says where primes begin; the PrimeGen class itself does not.
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
  explain: SimpleGen.lean line 39.
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
  explain: PrimeGen.lean lines 15–17.
---
## Plain English

`SimpleGen.start := { p := ⟨2, Nat.prime_two⟩, c := min_prime_gt 2 }` (SimpleGen.lean lines 38–39): prime 2, next prime 3. Used by [simpleGen_exists_prime_gt](#/node/simpleGen_exists_prime_gt), the circular reference theorem. See [SimpleGen](#/node/SimpleGen) and [min_prime_gt](#/node/min_prime_gt).
