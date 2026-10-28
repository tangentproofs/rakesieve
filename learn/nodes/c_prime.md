---
id: c_prime
title: The candidate is prime
summary: 'No sieve ever tests the candidate for primality. Its primality is a theorem: a prime factor would be either
  ≤ P (sieved out) or between P and C (impossible).'
review: draft
authors:
- grok-bot
quiz:
- q: Does any sieve in this library run a primality test on C?
  type: choice
  choices:
  - 'Yes'
  - No, C's primality is proved from the driver facts
  answer: 1
  explain: '`c_prime` is a theorem about every driven state.'
- q: Which two lemmas cover the two cases of a prime factor q?
  type: choice
  choices:
  - '`hCinR` (q ≤ P) and `no_skipped_prime` (q > P)'
  - '`r_next` and `r_gt_p`'
  answer: 0
  explain: PrimeSieve.lean lines 180–187.
- q: Why is C ≥ 2?
  type: choice
  choices:
  - C > P and P is prime, so P ≥ 2
  - by definition
  answer: 0
  explain: PrimeSieve.lean lines 188–192.
---
## Plain English

**Theorem (`c_prime`, PrimeSieve.lean lines 173–193).** For any driven sieve state g, C g is prime.

Proof by [no_prime_factors_im_no_factors](#/node/no_prime_factors_im_no_factors): C ≥ 2 because C > P ≥ 2 ([c_gt_p](#/node/c_gt_p)). A prime q < C dividing C would be ≤ P, impossible since C ∈ [R](#/node/R) P, or > P, impossible by [no_skipped_prime](#/node/no_skipped_prime).

It supplies the `hC` argument of every sieve step ([nextState](#/node/nextState)).
