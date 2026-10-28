---
id: Rake.partition_term_iff
title: Partitioning keeps exactly the same terms
summary: The 'easy' direction, that old terms survive the split, is the long one, a calc chain of mod and div rewrites
  over nearly 60 lines.
review: draft
authors:
- grok-bot
quiz:
- q: Does partition add or remove numbers?
  type: choice
  choices:
  - neither
  - adds
  - removes
  answer: 0
  explain: Same set of terms.
- q: Which half is longer in the source?
  type: choice
  choices:
  - '`partition_term_keep`'
  - '`partition_term_same`'
  answer: 0
  explain: Rake.lean lines 287–345.
- q: Is it an iff for every n?
  type: choice
  choices:
  - 'Yes'
  - Only for primes
  answer: 0
  explain: '`∀n, … ↔ …`.'
---
## Plain English

**Theorem (`Rake.partition_term_iff`, Rake.lean lines 347–351).** n is a term of r.partition j iff n is a term of r. It combines `partition_term_same` (Rake.lean lines 255–285) and `partition_term_keep` (Rake.lean lines 287–345). See [Rake.partition](#/node/Rake.partition).
