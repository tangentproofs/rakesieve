---
id: RakeSieve.instPrimeSieveStateRakeSieve
title: The RakeSieve is a sieve state
summary: 'The proof that the candidate grows reuses the generic r_gt_p: the new candidate is in R of the new prime,
  so it exceeds the new prime, which is the old candidate.'
review: draft
authors:
- grok-bot
caveats:
- An anonymous instance; this site names it `RakeSieve.instPrimeSieveStateRakeSieve`, which may differ from the
  name Lean generates.
quiz:
- q: What is `C` for a RakeSieve state?
  type: choice
  choices:
  - its field `c`
  - its rake's last term
  answer: 0
  explain: '`C x := x.c` (RakeSieve.lean line 115).'
- q: Why is the new candidate bigger than the old one?
  type: choice
  choices:
  - it lies in R (new p), so it exceeds new p = old c
  - the rake grows
  answer: 0
  explain: RakeSieve.lean lines 123–126.
- q: Which step function does it use?
  type: choice
  choices:
  - '`RakeSieve.next`'
  - '`PrimeSieve.next`'
  answer: 0
  explain: '`next := .next` (RakeSieve.lean line 116).'
---
## Plain English

`instance : PrimeSieveState RakeSieve` (RakeSieve.lean lines 113–126): P is the state's prime p, C its candidate c, the step is [RakeSieve.next](#/node/RakeSieve.next). The `hNext` proof shows the new p is the old c (by unfolding `next`) and the new c exceeds the old c (the new c is in R (new p), so [r_gt_p](#/node/r_gt_p) applies).
