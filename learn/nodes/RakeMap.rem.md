---
id: RakeMap.rem
title: 'RakeMap.rem: remove multiples of j, keeping the certificate'
summary: '**The surprise:** it cannot be called without proof that something will survive, which is why the RakeSieve
  needs Euclid at every step.'
review: draft
authors:
- grok-bot
quiz:
- q: What predicate does the result describe?
  type: choice
  choices:
  - prop n ∧ ¬ j ∣ n
  - prop n ∨ j ∣ n
  answer: 0
  explain: The return type.
- q: Why must j be positive?
  type: choice
  choices:
  - partitioning by 0 would leave no sequences
  - for printing
  answer: 0
  explain: Comment, RakeMap.lean lines 39–41.
- q: Why sort at the end?
  type: choice
  choices:
  - partition and filter make the constants unsorted, and RakeMap requires sorted
  - for speed
  answer: 0
  explain: '`hord` must hold.'
---
## Plain English

`rm.rem j hj hnmr` (RakeMap.lean lines 48–68): given a [RakeMap](#/node/RakeMap) for prop, a positive j and a proof that some term is not a multiple of j, it returns a RakeMap for **prop n ∧ ¬ j ∣ n**. Inside, it applies [Rake.rem](#/node/Rake.rem), uses rem_drop/rem_keep/rem_same to update the iff, then sorts the constants (`Rake.sort`, which removes duplicates and merge-sorts) so the result is sorted again.

The comment above it suggests a future version returning `Option Rake` instead of requiring the proof.
