---
id: c_gt_p
title: The candidate is beyond the current prime
summary: '**The surprise:** a one-line consequence, but it is the whole reason the generated primes strictly increase,
  the property that turned out to be needed for infinitude.'
review: draft
authors:
- grok-bot
quiz:
- q: Which driver field does it use?
  type: choice
  choices:
  - '`hCinR`'
  - '`hRmin`'
  answer: 0
  explain: C ∈ R P, then `r_gt_p`.
- q: Which `PrimeGen` field does it supply?
  type: choice
  choices:
  - '`hP''`'
  - '`hP_lt`'
  answer: 1
  explain: Strict increase.
- q: Does it need C to be the *least* survivor?
  type: choice
  choices:
  - 'Yes'
  - No, only that C survives
  answer: 1
  explain: Any survivor exceeds P.
---
## Plain English

**Theorem (`c_gt_p`, PrimeSieve.lean lines 129–131).** For any driven sieve state g, C g > P g.

Because C g ∈ [R](#/node/R) (P g) (the driver's `hCinR`) and everything in R P exceeds P ([r_gt_p](#/node/r_gt_p)). The [driver instance](#/node/instPrimeGenPrimeSieve) uses it for `hP_lt`.
