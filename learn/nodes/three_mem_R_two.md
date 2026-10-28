---
id: three_mem_R_two
title: 3 ∈ R 2 (the lemma behind the headline)
summary: '**The surprise:** shared by every sieve: it lives in PrimeSieve.lean, not in the RakeSieve, so any future
  sieve can start from it.'
review: draft
authors:
- grok-bot
quiz:
- q: Which file holds it?
  type: choice
  choices:
  - PrimeSieve.lean
  - RakeSieve.lean
  answer: 0
  explain: Moved there in 37c37c7 so every sieve can use it.
- q: How is ¬ 2 ∣ 3 checked?
  type: choice
  choices:
  - '`decide`'
  - '`native_decide`'
  answer: 0
  explain: By `decide`, PrimeSieve.lean line 27.
- q: Which Results.lean theorem re-exports it?
  type: choice
  choices:
  - '`results_three_mem_R_two`'
  - '`results_exists_prime_gt_of_rakeSieve`'
  answer: 0
  explain: See Results.lean lines 5–6.
---
## Plain English

**Theorem (`three_mem_R_two`, PrimeSieve.lean lines 19–27).** 3 ∈ [R](#/node/R) 2. Exported as [results_three_mem_R_two](#/node/results_three_mem_R_two), which has the proof outline. Used by [RakeSieve.init](#/node/RakeSieve.init).
