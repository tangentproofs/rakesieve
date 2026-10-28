---
id: RakeMap.min_term_zero
title: A rake map's first term is its smallest
summary: A one-line wrapper, but it is the step that turns 'sorted list' into 'this is the next prime'.
review: draft
authors:
- grok-bot
quiz:
- q: Which proof does it reuse?
  type: choice
  choices:
  - '`Rake.sorted_min_term_zero`'
  - '`c_prime`'
  answer: 0
  explain: RakeMap.lean line 19.
- q: Why is the rake map sorted?
  type: choice
  choices:
  - '`hord` is a field'
  - luck
  answer: 0
  explain: Every RakeMap carries it.
- q: Where is it used?
  type: choice
  choices:
  - RakeSieve.next, for `hRmin`
  - SimpleGen
  answer: 0
  explain: RakeSieve.lean line 125.
---
## Plain English

**Theorem (`RakeMap.min_term_zero`, RakeMap.lean lines 18–19).** rm.term 0 ≤ rm.term n for every n. It is [Rake.sorted_min_term_zero](#/node/Rake.sorted_min_term_zero) applied with the map's sortedness proof. [RakeSieve.next](#/node/RakeSieve.next) uses it on its last line.
