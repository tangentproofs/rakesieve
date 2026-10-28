---
id: ASeq
title: 'ASeq: an arithmetic sequence k + d·n'
summary: '**The surprise:** the basic object is just two numbers. The odd numbers are (1, 2), all numbers ≥ 2 are
  (2, 1), and the whole sieve is built by composing such pairs.'
review: draft
authors:
- grok-bot
quiz:
- q: Which ASeq lists 3, 5, 7, 9, …?
  type: choice
  choices:
  - k = 3, d = 2
  - k = 2, d = 3
  - k = 1, d = 2
  answer: 0
  explain: The sequence 3 + 2n.
- q: What is the 4th term (n = 4) of k = 5, d = 6?
  type: choice
  choices:
  - '29'
  - '24'
  - '35'
  answer: 0
  explain: 5 + 6·4 = 29.
- q: Can d be 0?
  type: choice
  choices:
  - 'Yes: then every term equals k'
  - No, the type forbids it
  answer: 0
  explain: '`d : Nat` allows 0; `Rake.partition` comments on why d = 0 is awkward.'
---
## Plain English

An `ASeq` (ASeq.lean lines 6–9) is a pair: a constant k and a step d. It stands for the sequence k, k + d, k + 2d, … ; its n-th term is [ASeq.term](#/node/ASeq.term) s n = k + d·n. [aseq](#/node/aseq) k d builds one.

Examples from the file: `nats = aseq 0 1`, `evens = aseq 0 2`, `odds = aseq 1 2` (ASeq.lean lines 40–42), checked with `#guard` on their first ten terms.

ASeq.lean also proves that composing sequences composes their terms (`ASeq.compose_def`), but the rake code works with constants and a shared step directly.
