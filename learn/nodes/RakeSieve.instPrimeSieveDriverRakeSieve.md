---
id: RakeSieve.instPrimeSieveDriverRakeSieve
title: The RakeSieve satisfies the driver
summary: There is nothing to prove here. Every RakeSieve state already carries `hCinR` and `hRmin` as fields, so
  the driver instance just reads them off.
review: draft
authors:
- grok-bot
caveats:
- An anonymous instance; the site's name for it is an approximation.
quiz:
- q: Where are the driver facts proved for the RakeSieve?
  type: choice
  choices:
  - inside `init` and `next`, when each state is built
  - in this instance
  - nowhere
  answer: 0
  explain: The structure's fields are proofs.
- q: How long is the instance?
  type: choice
  choices:
  - three lines
  - a hundred lines
  answer: 0
  explain: RakeSieve.lean lines 130–132.
- q: Which two fields does it supply?
  type: choice
  choices:
  - '`hCinR` and `hRmin`'
  - '`hP''` and `hP_lt`'
  answer: 0
  explain: Those are the fields of `PrimeSieveDriver`.
---
## Plain English

`instance : PrimeSieveDriver RakeSieve` (RakeSieve.lean lines 130–132) sets `hCinR x := x.hCinR` and `hRmin x := x.hRmin`, after unfolding C and P. The work was done when each state was built: in [RakeSieve.init](#/node/RakeSieve.init) and in [RakeSieve.next](#/node/RakeSieve.next). See [PrimeSieveDriver](#/node/PrimeSieveDriver).
