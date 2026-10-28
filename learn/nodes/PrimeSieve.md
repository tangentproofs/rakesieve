---
id: PrimeSieve
title: 'PrimeSieve: a wrapper that turns a sieve state into a generator'
summary: '**The surprise:** it holds nothing but the state. The wrapper exists only so Lean''s instance search can
  attach one generic proof, ''this is a prime generator'', to every sieve at once.'
review: draft
authors:
- grok-bot
caveats:
- The site's scanner reads section `variable`s by hand for this declaration (PrimeSieve.lean line 210); it does
  not run Lean.
quiz:
- q: How many fields does `PrimeSieve α` have?
  type: choice
  choices:
  - one, `state`
  - two
  - four
  answer: 0
  explain: PrimeSieve.lean line 212.
- q: Why wrap the state instead of making α itself a `PrimeGen`?
  type: choice
  choices:
  - so a single generic instance can cover every sieve type without overlapping other instances
  - for speed
  - because Lean forbids it
  answer: 0
  explain: '`instance : PrimeGen (PrimeSieve α)` is proved once for all α with the two sieve classes.'
- q: Which classes must α have?
  type: choice
  choices:
  - '`PrimeSieveState` and `PrimeSieveDriver`'
  - '`PrimeGen`'
  - '`Ord`'
  answer: 0
  explain: PrimeSieve.lean line 210.
---
## Plain English

`PrimeSieve α` is a structure with one field, `state : α` (PrimeSieve.lean lines 211–212), for a type α that has [PrimeSieveState](#/node/PrimeSieveState) and [PrimeSieveDriver](#/node/PrimeSieveDriver) instances (the section `variable` line, PrimeSieve.lean line 210).

Its step is [PrimeSieve.next](#/node/PrimeSieve.next), which runs the sieve once with the proofs supplied automatically, and the [driver instance](#/node/instPrimeGenPrimeSieve) makes it a [PrimeGen](#/node/PrimeGen). The main theorem uses `PrimeSieve RakeSieve` with state `RakeSieve.init`.
