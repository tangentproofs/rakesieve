---
id: RakeSieve.init
title: 'RakeSieve.init: prime 2, odd numbers ≥ 3, candidate 3'
summary: 'The starting rake is built by the same operation as every later step: begin with 2 + n (all numbers ≥
  2) and remove the multiples of 2, leaving the single sequence 3 + 2n.'
review: draft
authors:
- grok-bot
quiz:
- q: What is the rake after `init`?
  type: choice
  choices:
  - 2 + n
  - 3 + 2n (the odd numbers ≥ 3)
  - 1 + 2n
  answer: 1
  explain: Removing multiples of 2 from 2 + n leaves 3 + 2n; the README walks through this.
- q: Which two Results.lean facts does `init` use?
  type: choice
  choices:
  - 3 ∈ R 2 and 3 ≤ everything in R 2
  - Euclid's theorem twice
  answer: 0
  explain: RakeSieve.lean lines 48–53.
- q: What witness shows `rem 2` leaves something?
  type: choice
  choices:
  - 3, the term at m = 1
  - '2'
  - Mathlib's infinitude of primes
  answer: 0
  explain: '`use 3; use 1` (RakeSieve.lean line 21). Later steps use Mathlib''s Euclid instead.'
---
## Plain English

`RakeSieve.init` (RakeSieve.lean lines 19–53) is the start state:

- the rake map is [rm_ge2](#/node/RakeMap.rm_ge2) (the rake {2 + n}, i.e. every number ≥ 2) with the multiples of 2 removed by [RakeMap.rem](#/node/RakeMap.rem); its predicate is n ≥ 2 ∧ ¬ 2 ∣ n;
- p = 2, c = 3;
- `hprop`: n ≥ 2 ∧ ¬ 2 ∣ n ↔ n ∈ [R](#/node/R) 2 (proved inline, RakeSieve.lean lines 24–47);
- `hCinR` and `hRmin`: the two headline facts [3 ∈ R 2](#/node/results_three_mem_R_two) and [nothing in R 2 is below 3](#/node/results_three_le_of_mem_R_two).

To call `rem`, the code must show some term of {2 + n} is odd; it uses 3 = 2 + 1 (RakeSieve.lean line 21).
