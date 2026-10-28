---
id: results_three_le_of_mem_R_two
title: Nothing in R 2 is smaller than 3
summary: 'With the previous theorem this pins down the sieve''s first candidate: 3 is the *least* survivor after
  sieving by 2. That is exactly what the sieve needs to know 3 is the next prime.'
review: draft
authors:
- grok-bot
widgets:
- type: walkthrough
  title: The proof (PrimeSieve.lean, lines 30-37)
  config:
    steps:
    - text: Suppose r ∈ R 2 but r < 3
      lean: by_contra h
    - text: Since r ≥ 2, r = 2
      lean: 'have r2 : r = 2 := by omega'
    - text: But R 2 says the prime 2 does not divide r = 2, which is false
      lean: have := hrr 2 (by omega) Nat.prime_two
quiz:
- q: Why is 2 not in R 2?
  type: choice
  choices:
  - 2 is not prime
  - the prime 2 ≤ 2 divides 2
  - R 2 starts at 4
  answer: 1
  explain: R 2 requires that no prime q ≤ 2 divides n. For n = 2, q = 2 divides it.
- q: Combined with `results_three_mem_R_two`, what do we learn?
  type: choice
  choices:
  - 3 is the least element of R 2
  - R 2 is finite
  - 3 is the only element of R 2
  answer: 0
  explain: 3 is in R 2 and is ≤ every element of R 2.
- q: Which field of the RakeSieve structure does this discharge for the start state?
  type: choice
  choices:
  - '`hCinR`'
  - '`hRmin`'
  - '`hprop`'
  answer: 1
  explain: '`hRmin : ∀ r ∈ R p, c ≤ r` (RakeSieve.lean line 12); RakeSieve.lean line 53 uses this theorem.'
---
## Plain English

**R stands for *residue*.** R p is the set of numbers ≥ 2 that no prime ≤ p divides: what is left after crossing out the multiples of every prime up to p ([R](#/node/R)). For example, R 2 is the odd numbers from 3 up.

**Theorem (`results_three_le_of_mem_R_two`, Results.lean lines 8–9).** Every r ∈ R 2 satisfies 3 ≤ r.

Together with [3 ∈ R 2](#/node/results_three_mem_R_two), this says 3 is the minimum of [R](#/node/R) 2. The sieve's start state needs both: its candidate must be in R p (`hCinR`) and below everything else in R p (`hRmin`). See the [RakeSieve](#/node/RakeSieve) structure and RakeSieve.lean lines 48–53.

The proof: anything in R 2 is ≥ 2; if it were below 3 it would be 2, but 2 divides 2, so 2 is not in R 2.
