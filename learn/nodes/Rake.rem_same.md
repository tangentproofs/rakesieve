---
id: Rake.rem_same
title: rem adds no new terms
summary: '**The surprise:** the soundness half: whatever the reshuffling, rem only ever removes.'
review: draft
authors:
- grok-bot
quiz:
- q: Direction?
  type: choice
  choices:
  - terms of r.rem ⊆ terms of r
  - terms of r ⊆ terms of r.rem
  answer: 0
  explain: '`(∃m'', r''.term m'' = n) → (∃m, r.term m = n)`.'
- q: Together with drop and keep, terms of r.rem are exactly…
  type: choice
  choices:
  - the terms of r not divisible by j
  - the primes
  answer: 0
  explain: That is what `RakeMap.rem` records.
- q: Is HasNonMultiple assumed?
  type: choice
  choices:
  - 'Yes'
  - 'No'
  answer: 0
  explain: Otherwise `zer` produces 0, which need not be a term of r.
---
## Plain English

**Theorem (`Rake.rem_same`, Rake.lean lines 459–467).** Assuming HasNonMultiple, every term of r.rem is a term of r. See [Rake.rem](#/node/Rake.rem).
