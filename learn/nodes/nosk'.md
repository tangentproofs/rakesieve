---
id: nosk'
title: 'nosk'': no prime strictly between P and C'
summary: '**The surprise:** the apostrophe-named one-liner is the heart of ''next prime'': it is the claim that
  nothing was skipped, and a sieve step is only allowed to run once it has been proved.'
review: draft
authors:
- grok-bot
quiz:
- q: Is `nosk' 3 5` true?
  type: choice
  choices:
  - 'Yes: 4 is the only number strictly between, and it is not prime'
  - 'No'
  answer: 0
  explain: The only q with 3 < q < 5 is 4, which is not prime.
- q: Is `nosk' 7 13` true?
  type: choice
  choices:
  - 'Yes'
  - 'No: 11 is a prime strictly between'
  answer: 1
  explain: 11 is prime and 7 < 11 < 13.
- q: Does `nosk' P C` say C is prime?
  type: choice
  choices:
  - 'Yes'
  - No, it only says no prime lies strictly between
  answer: 1
  explain: Primality of C is a separate argument `hC` of `PrimeSieveState.next`.
---
## Plain English

`nosk' P C` (PrimeSieve.lean line 5) abbreviates **¬ ∃ q, q is prime ∧ P < q ∧ q < C**: there is no prime strictly between P and C. "nosk" is short for "no skip".

[PrimeSieveState](#/node/PrimeSieveState)'s `next` takes a proof of `nosk' (P s) (C s)` as an argument. In other words a sieve step may only be taken once someone has proved that the candidate C is the very next prime after P. The generic driver supplies that proof ([no_skipped_prime](#/node/no_skipped_prime)).
