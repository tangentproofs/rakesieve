---
id: Rake.term_iff
title: Which numbers a rake produces
summary: Most of the proof is index arithmetic with mod and div, to show the round-robin order hits every k + x·d
  exactly where expected.
review: draft
authors:
- grok-bot
quiz:
- q: Given k = ks[i] and x, which n gives term n = k + x·d?
  type: choice
  choices:
  - n = i + x·q
  - n = x
  - n = i·x
  answer: 0
  explain: Rake.lean line 78 builds n := (i mod q) + x·q.
- q: Does the theorem depend on sortedness?
  type: choice
  choices:
  - 'No'
  - 'Yes'
  answer: 0
  explain: It holds for any rake, sorted or not.
- q: Why is it useful?
  type: choice
  choices:
  - it reduces term questions to questions about ks
  - it computes primes
  answer: 0
  explain: Used in the partition and rem proofs.
---
## Plain English

**Theorem (`Rake.term_iff`, Rake.lean lines 48–99).** m = r.term n for some n **iff** m = k + x·d for some k ∈ ks and some x. This turns questions about the term function into questions about the constants list, and every later rake proof uses it. See [Rake.term](#/node/Rake.term).
