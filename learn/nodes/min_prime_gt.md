---
id: min_prime_gt
title: 'min_prime_gt n: the least prime above n, found by Nat.find'
summary: It is computable in principle, since Nat.find just counts upward, but only because Euclid guarantees the
  search stops.
review: draft
authors:
- grok-bot
quiz:
- q: What does `Nat.find` need?
  type: choice
  choices:
  - a proof that some number satisfies the property
  - an upper bound only
  answer: 0
  explain: Here `ex_prime_gt n`.
- q: What is `(min_prime_gt 13).p`?
  type: choice
  choices:
  - '13'
  - '17'
  - '15'
  answer: 1
  explain: 17 is the least prime above 13.
- q: Who uses it?
  type: choice
  choices:
  - SimpleGen
  - RakeSieve
  answer: 0
  explain: '`SimpleGen.next` and `SimpleGen.start`.'
---
## Plain English

`min_prime_gt n` (SimpleGen.lean lines 24–28) is the [MinPrimeGt](#/node/MinPrimeGt) n whose number is `Nat.find (ex_prime_gt n)`: the least p satisfying [PrimeGt](#/node/PrimeGt) n p. `Nat.find_spec` and `Nat.find_min` give the two proofs. It is [SimpleGen](#/node/SimpleGen)'s step.
