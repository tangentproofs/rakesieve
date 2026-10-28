---
id: PrimeSieveDriver
title: 'PrimeSieveDriver: the candidate is the least survivor'
summary: '**The surprise:** two lines, ''C is in R P'' and ''C is below everything in R P'', are all a sieve needs
  to promise. From them alone the library proves C is prime and nothing was skipped, for every sieve.'
review: draft
authors:
- grok-bot
quiz:
- q: Which two facts does a `PrimeSieveDriver` supply?
  type: choice
  choices:
  - C is prime; C is odd
  - C ∈ R P; C ≤ every element of R P
  - P is prime; P < C
  answer: 1
  explain: '`hCinR` and `hRmin`.'
- q: Does a driver have to prove that C is prime?
  type: choice
  choices:
  - 'Yes'
  - No, `c_prime` derives it from `hCinR` and `hRmin`
  answer: 1
  explain: PrimeSieve.lean lines 173–193.
- q: For the RakeSieve, where do `hCinR` and `hRmin` come from?
  type: choice
  choices:
  - They are fields of the `RakeSieve` structure itself
  - From Mathlib
  - From `decide`
  answer: 0
  explain: The `RakeSieve` structure carries `hCinR` and `hRmin` (RakeSieve.lean lines 11–12); the driver instance
    just reads them (lines 130–132).
---
## Plain English

A `PrimeSieveDriver` for a sieve state type α (PrimeSieve.lean lines 124–126) adds two facts to [PrimeSieveState](#/node/PrimeSieveState), for every state g:

- `hCinR`: the candidate C g is in [R](#/node/R) (P g), i.e. it survived sieving by every prime up to P g;
- `hRmin`: C g ≤ n for every n in R (P g), i.e. it is the *least* survivor.

The docstring describes a prime sieve as something that models the numbers > 1 coprime to the known primes, repeatedly takes the minimum as the next prime, and then eliminates its multiples. These two fields are the formal version of "takes the minimum".

From them the library derives [c_prime](#/node/c_prime) (C is prime), [no_skipped_prime](#/node/no_skipped_prime) and [c_gt_p](#/node/c_gt_p), which is all that [nextState](#/node/nextState) needs.
