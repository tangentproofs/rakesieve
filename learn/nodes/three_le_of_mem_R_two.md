---
id: three_le_of_mem_R_two
title: Nothing in R 2 is below 3 (the lemma behind the headline)
summary: '**The surprise:** with 3 ∈ R 2 it makes 3 the minimum of R 2, which is exactly what the start state must
  prove about its candidate.'
review: draft
authors:
- grok-bot
quiz:
- q: Why is 2 excluded from R 2?
  type: choice
  choices:
  - 2 divides 2
  - 2 is not prime
  answer: 0
  explain: The prime 2 ≤ 2 divides it.
- q: Which structure field does it provide for the start state?
  type: choice
  choices:
  - '`hRmin`'
  - '`hprop`'
  answer: 0
  explain: See RakeSieve.lean line 53.
- q: Is it proved by contradiction?
  type: choice
  choices:
  - 'Yes'
  - 'No'
  answer: 0
  explain: '`by_contra h` on PrimeSieve.lean line 32.'
---
## Plain English

**Theorem (`three_le_of_mem_R_two`, PrimeSieve.lean lines 30–37).** Every r ∈ [R](#/node/R) 2 has 3 ≤ r. Exported as [results_three_le_of_mem_R_two](#/node/results_three_le_of_mem_R_two), which has the proof outline. Used by [RakeSieve.init](#/node/RakeSieve.init).
