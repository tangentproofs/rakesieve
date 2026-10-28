---
id: nextState
title: 'nextState: one sieve step, with the proofs filled in'
summary: '**The surprise:** the step a user calls takes no proofs, because the library proves the step''s preconditions
  itself, for every driven sieve, every time.'
review: draft
authors:
- grok-bot
quiz:
- q: Which two proofs does `nextState` pass to the sieve's `next`?
  type: choice
  choices:
  - '`c_prime` and `no_skipped_prime`'
  - '`r_gt_p` and `r_next`'
  answer: 0
  explain: PrimeSieve.lean lines 206–208.
- q: Does a caller of `nextState` need to prove anything?
  type: choice
  choices:
  - 'Yes'
  - 'No'
  answer: 1
  explain: The proofs come from the driver.
- q: For the RakeSieve, which function does `nextState` end up calling?
  type: choice
  choices:
  - '`RakeSieve.next`'
  - '`SimpleGen.next`'
  answer: 0
  explain: The RakeSieve's `PrimeSieveState` instance sets `next := .next` (RakeSieve.lean line 116).
---
## Plain English

`nextState s` (PrimeSieve.lean lines 205–208) is `PrimeSieveState.next s (c_prime …) (no_skipped_prime …)`: it runs the sieve's own step, passing in the two proofs that step demands, [c_prime](#/node/c_prime) and [no_skipped_prime](#/node/no_skipped_prime). [PrimeSieve.next](#/node/PrimeSieve.next) applies it to the wrapped state.
