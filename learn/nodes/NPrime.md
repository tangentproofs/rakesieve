---
id: NPrime
title: 'NPrime: a natural number packaged with a proof that it is prime'
summary: A value of this type cannot be a non-prime. Every prime a generator hands out carries its own certificate,
  so 'the output is prime' never has to be proved again.
review: draft
authors:
- grok-bot
quiz:
- q: Can you build an `NPrime` holding 4?
  type: choice
  choices:
  - 'Yes'
  - 'No: you would need a proof of `Nat.Prime 4`, which is false'
  answer: 1
  explain: 'An `NPrime` is a subtype value: the number together with a proof that it is prime.'
- q: How is the number 2 packaged as an `NPrime` in this library?
  type: choice
  choices:
  - '`⟨2, Nat.prime_two⟩`'
  - '`NPrime.mk 2`'
  - '`2 : NPrime` with no proof'
  answer: 0
  explain: See `SimpleGen.start` (SimpleGen.lean line 39) and `RakeSieve.init` (RakeSieve.lean line 25).
- q: What does `(P g).prop` give you, for a generator state g?
  type: choice
  choices:
  - the number
  - a proof that the number is prime
  - the next state
  answer: 1
  explain: '`.prop` is the proof component of a subtype value; `exists_prime_gt_of_primeGen` uses it (PrimeGen.lean
    line 73).'
---
## Plain English

`NPrime` is the type `{ n : Nat // Nat.Prime n }` (PrimeGen.lean line 6): a pair of a natural number and a proof that it is prime. Lean can only build one by supplying the proof, for example `⟨2, Nat.prime_two⟩`.

The library adds conveniences: two `NPrime`s are equal when their numbers are ([NPrime.eq_iff](#/node/NPrime.eq_iff)), they print as their number, and they coerce to `Nat` (PrimeGen.lean lines 8–11).

Because [PrimeGen](#/node/PrimeGen)'s `P` returns an `NPrime`, every generator's output is prime *by its type*.
