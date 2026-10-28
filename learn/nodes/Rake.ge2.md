---
id: Rake.ge2
title: 'Rake.ge2: every number from 2 up'
summary: The sieve's raw material is one sequence, 2 + 1·n.
review: draft
authors:
- grok-bot
quiz:
- q: What are its first terms?
  type: choice
  choices:
  - 2, 3, 4, 5, …
  - 2, 4, 6, …
  answer: 0
  explain: The sequence 2 + n.
- q: Its step d is
  type: choice
  choices:
  - '1'
  - '2'
  answer: 0
  explain: See Rake.lean line 28.
- q: Is it sorted?
  type: choice
  choices:
  - Yes, by default
  - 'No'
  answer: 0
  explain: '`sorted` defaults to true with automatic proofs for a one-element list.'
---
## Plain English

`ge2 := { d := 1, ks := [2] }` (Rake.lean line 28): the [Rake](#/node/Rake) whose only sequence is 2 + n. [RakeMap.rm_ge2](#/node/RakeMap.rm_ge2) proves its terms are exactly the numbers ≥ 2.
