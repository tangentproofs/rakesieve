---
id: RakeMap.rm_ge2
title: 'rm_ge2: the rake 2 + n describes the numbers ≥ 2'
summary: 'The first certified fact in the sieve''s chain: the single sequence 2 + n lists exactly the numbers from
  2 up.'
review: draft
authors:
- grok-bot
quiz:
- q: Which m gives term m = n for n ≥ 2?
  type: choice
  choices:
  - n − 2
  - n
  - n/2
  answer: 0
  explain: '`use n-2` (RakeMap.lean line 32).'
- q: What is its predicate?
  type: choice
  choices:
  - 2 ≤ n
  - n prime
  answer: 0
  explain: It is part of the type `RakeMap (λ n => 2 ≤ n)`.
- q: What comes next in the sieve?
  type: choice
  choices:
  - removing multiples of 2
  - removing multiples of 3
  answer: 0
  explain: '`rm_ge2 |>.rem 2` (RakeSieve.lean line 23).'
---
## Plain English

`rm_ge2 : RakeMap (λ n => 2 ≤ n)` (RakeMap.lean lines 27–34): the rake [Rake.ge2](#/node/Rake.ge2), with the proof that n ≥ 2 iff n = 2 + m for some m. [RakeSieve.init](#/node/RakeSieve.init) removes the multiples of 2 from it.
