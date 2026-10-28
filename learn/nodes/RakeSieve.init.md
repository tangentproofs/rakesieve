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
  explain: RakeSieve.lean lines 51–56.
- q: What witness shows `rem 2` leaves something?
  type: choice
  choices:
  - 3, the term at m = 1
  - '2'
  - Mathlib's infinitude of primes
  answer: 0
  explain: '`use 3; use 1` (RakeSieve.lean line 24). Later steps use the survivor c + d instead.'
---
## Plain English

**R stands for *residue*.** R p is the set of numbers ≥ 2 that no prime ≤ p divides: what is left after crossing out the multiples of every prime up to p ([R](#/node/R)). For example, R 2 is the odd numbers from 3 up.

`RakeSieve.init` (RakeSieve.lean lines 22–62) is the start state:

- the rake map is [rm_ge2](#/node/RakeMap.rm_ge2) (the rake {2 + n}, i.e. every number ≥ 2) with the multiples of 2 removed by [RakeMap.rem](#/node/RakeMap.rem); its predicate is n ≥ 2 ∧ ¬ 2 ∣ n;
- p = 2, c = 3;
- `hprop`: n ≥ 2 ∧ ¬ 2 ∣ n ↔ n ∈ [R](#/node/R) 2 (proved inline, RakeSieve.lean lines 27–50);
- `hCinR` and `hRmin`: the two headline facts [3 ∈ R 2](#/node/results_three_mem_R_two) and [nothing in R 2 is below 3](#/node/results_three_le_of_mem_R_two);
- `hdfac`: the start rake's period is 1 · 2 = 2 ([RakeMap.rem_d](#/node/RakeMap.rem_d)), and its only prime factor, 2, is ≤ p (RakeSieve.lean lines 57–62).

To call `rem`, the code must show some term of {2 + n} is odd; it uses 3 = 2 + 1 (RakeSieve.lean line 24).
