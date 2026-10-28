---
id: RakeMap.rem_d
title: 'RakeMap.rem_d: removing multiples of j multiplies the period by j'
summary: Crossing out a prime's multiples never shrinks the rake's period. It always multiplies it by that prime,
  so after sieving by 2, 3, 5, …, p the period is their product.
review: draft
authors:
- grok-bot
quiz:
- q: Start with d = 2 and remove the multiples of 3. What is the new period?
  type: choice
  choices:
  - '6'
  - '3'
  - '2'
  answer: 0
  explain: 2 · 3 = 6, as in 5 + 6n and 7 + 6n.
- q: Why does sorting not change the period?
  type: choice
  choices:
  - sort only reorders and dedups the constants
  - it does change it
  answer: 0
  explain: '`(rm.rake.rem hj).sort.prop.1` (RakeMap.lean line 78).'
- q: Which RakeSieve invariant does it keep alive?
  type: choice
  choices:
  - '`hdfac`'
  - '`hRmin`'
  answer: 0
  explain: RakeSieve.lean line 129.
---
## Plain English

**Theorem (`RakeMap.rem_d`, RakeMap.lean lines 72–80).** For a [RakeMap](#/node/RakeMap) rm, a positive j and a proof that something survives, the rake of `rm.rem j` has period rm.rake.d · j.

[RakeMap.rem](#/node/RakeMap.rem) first splits each sequence into j sequences with step d · j ([Rake.partition](#/node/Rake.partition)), then drops some sequences and sorts. Dropping and sorting keep the step. The proof reads this off `Rake.rem_def` and the spec of `sort`.

[RakeSieve.init](#/node/RakeSieve.init) uses it to show its period is 1 · 2 = 2. [RakeSieve.next](#/node/RakeSieve.next) uses it to show the new period is d · c, which keeps the invariant `hdfac` (every prime factor of the period is ≤ the current prime).
