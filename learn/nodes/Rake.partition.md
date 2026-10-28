---
id: Rake.partition
title: 'Rake.partition: split each sequence into j sequences'
summary: The rake grows j-fold but produces exactly the same numbers; it only changes how they are grouped, so that
  divisibility by j can be read off the constants.
review: draft
authors:
- grok-bot
quiz:
- q: Partition {d = 2, ks = [3]} by 3. What do you get?
  type: choice
  choices:
  - d = 6, ks = [3, 5, 7]
  - d = 3, ks = [3]
  - d = 6, ks = [3]
  answer: 0
  explain: 3 + 0·2, 3 + 1·2, 3 + 2·2 with step 6 (the README's example).
- q: How many constants after partitioning q constants by j?
  type: choice
  choices:
  - j·q
  - q + j
  - q
  answer: 0
  explain: '`length_partition`.'
- q: Why must j be positive?
  type: choice
  choices:
  - j = 0 would leave no sequences
  - for speed
  answer: 0
  explain: The docstring, Rake.lean lines 227–231.
---
## Plain English

`r.partition j` (Rake.lean lines 232–239) replaces step d by d·j and the constants by k + i·d for every constant k and i = 0, …, j−1. Each old sequence k + d·n splits into j sequences by n mod j.

[partition_term_iff](#/node/Rake.partition_term_iff) proves the terms are unchanged. After partitioning by j, the step d·j is a multiple of j, so a sequence k + d·j·n is all multiples of j if j ∣ k, and none otherwise. That is what makes [Rake.rem](#/node/Rake.rem) work.

The result is marked `sorted := false`.
