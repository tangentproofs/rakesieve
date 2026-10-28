---
id: SimpleGen
title: 'SimpleGen: the obvious prime generator (reference spec, circular)'
summary: It is the specification as a program, 'the next prime is the least prime above this one'. It exists so
  the RakeSieve has something to be compared with. It assumes Euclid, so it proves nothing about infinitude.
review: draft
authors:
- grok-bot
quiz:
- q: What does a SimpleGen hold?
  type: choice
  choices:
  - a prime and the least prime above it
  - a rake
  answer: 0
  explain: Fields `p` and `c`.
- q: Is the `#guard` on its first ten primes a proof?
  type: choice
  choices:
  - it is a compile-time check by evaluation, not a theorem in Results.lean
  - it is an axiom
  answer: 0
  explain: '`#guard` fails compilation if the equation evaluates to false.'
- q: How does it find each prime?
  type: choice
  choices:
  - Nat.find
  - sieving
  answer: 0
  explain: via `min_prime_gt`.
---
## Plain English

A `SimpleGen` (SimpleGen.lean lines 30–32) holds a prime p and the [least prime above it](#/node/MinPrimeGt). Its step moves to that prime ([SimpleGen.next](#/node/SimpleGen.next)), and [its PrimeGen instance](#/node/instPrimeGenSimpleGen) is proved directly from `hmin` and `hpgt`. SimpleGen.lean opens by saying it is a reference spec that assumes Euclid's theorem and is not on the RakeSieve's headline path. The `#guard` on SimpleGen.lean line 57 checks by evaluation that its first ten primes from [SimpleGen.start](#/node/SimpleGen.start) are 2, 3, 5, …, 29.
