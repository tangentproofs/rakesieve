---
id: PrimeSieve.next
title: 'PrimeSieve.next: step the wrapped sieve'
summary: It is nothing more than `nextState` applied inside the wrapper; all the mathematics is in the proofs it
  carries along.
review: draft
authors:
- grok-bot
quiz:
- q: What does `PrimeSieve.next` change?
  type: choice
  choices:
  - only the wrapped state, by one sieve step
  - the type α
  answer: 0
  explain: PrimeSieve.lean line 215.
- q: Which `PrimeGen` field is it?
  type: choice
  choices:
  - '`P`'
  - '`next`'
  answer: 1
  explain: PrimeSieve.lean line 220.
- q: Does it need proofs from the caller?
  type: choice
  choices:
  - 'No'
  - 'Yes'
  answer: 0
  explain: '`nextState` supplies them.'
---
## Plain English

`PrimeSieve.next x = { state := nextState x.state }` (PrimeSieve.lean lines 214–215). It is the `next` of the [driver instance](#/node/instPrimeGenPrimeSieve). See [nextState](#/node/nextState).
