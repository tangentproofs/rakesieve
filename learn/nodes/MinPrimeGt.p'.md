---
id: MinPrimeGt.p'
title: 'MinPrimeGt.p'': the next prime is prime'
summary: '**The surprise:** a one-line projection, handy enough to get its own name.'
review: draft
authors:
- grok-bot
quiz:
- q: What does it return?
  type: choice
  choices:
  - a proof that m.p is prime
  - the number m.p
  answer: 0
  explain: It is `m.hpgt.left`.
- q: Which field does it read?
  type: choice
  choices:
  - '`hpgt`'
  - '`hmin`'
  answer: 0
  explain: '`hpgt : PrimeGt n p`, whose left part is primality.'
- q: Is it a theorem or a definition?
  type: choice
  choices:
  - theorem
  - def
  answer: 0
  explain: Declared with `theorem` on PrimeGen.lean line 35.
---
## Plain English

`MinPrimeGt.p' m : Nat.Prime m.p` (PrimeGen.lean line 35): the first half of `hpgt`. See [MinPrimeGt](#/node/MinPrimeGt).
