---
id: PrimeSieveState
title: 'PrimeSieveState: a sieve''s state, its prime, its candidate, its step'
summary: 'The step function demands proofs as inputs: you may only advance a sieve after proving the candidate is
  prime and nothing was skipped. The interface makes an unjustified step impossible to write.'
review: draft
authors:
- grok-bot
quiz:
- q: What does `next` require besides the state?
  type: choice
  choices:
  - nothing
  - proofs that C is prime and that no prime lies strictly between P and C
  - the list of all primes so far
  answer: 1
  explain: '`next (s:α) (hC: Nat.Prime (C s)) (hN: nosk'' (P s) (C s)): α` (PrimeSieve.lean line 9).'
- q: After one step, what is the new prime P?
  type: choice
  choices:
  - the old P + 1
  - the old candidate C
  - the new candidate
  answer: 1
  explain: '`hNext` gives `P s'' = C s`.'
- q: Does `PrimeSieveState` alone guarantee C is the least survivor?
  type: choice
  choices:
  - 'Yes'
  - No, that is `PrimeSieveDriver`'s `hRmin`
  answer: 1
  explain: '`PrimeSieveDriver` adds `hCinR` and `hRmin` (PrimeSieve.lean lines 124–126).'
---
## Plain English

A `PrimeSieveState` on a type α (PrimeSieve.lean lines 6–11) provides, for each state s:

- `P s : NPrime`, the latest prime found ([NPrime](#/node/NPrime));
- `C s : Nat`, the candidate for the next prime;
- `next s hC hN : α`, one sieve step, which needs a proof `hC` that C s is prime and a proof `hN : nosk' (P s) (C s)` that no prime lies strictly between ([nosk'](#/node/nosk'));
- `hNext`: after the step, the new prime is the old candidate (P s' = C s) and the candidate grew (C s' > C s).

On its own this says nothing about whether C really is the next prime. That job belongs to [PrimeSieveDriver](#/node/PrimeSieveDriver), which ties C to the set [R](#/node/R).
