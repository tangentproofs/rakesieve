---
id: aseq
title: 'aseq k d: build the sequence k + d·n'
summary: '**The surprise:** a one-line constructor, marked @[simp] so Lean unfolds it automatically in proofs.'
review: draft
authors:
- grok-bot
quiz:
- q: '`aseq 1 2` is…'
  type: choice
  choices:
  - the odd numbers
  - the even numbers
  answer: 0
  explain: The sequence 1 + 2n.
- q: Why mark it @[simp]?
  type: choice
  choices:
  - so `simp` unfolds it automatically
  - for speed at runtime
  answer: 0
  explain: A simp lemma rewrites `aseq k d` to `ASeq.mk k d`.
- q: Its arguments are…
  type: choice
  choices:
  - constant, then step
  - step, then constant
  answer: 0
  explain: '`aseq (k:Nat) (d:Nat)`.'
---
## Plain English

`aseq k d := ASeq.mk k d` (ASeq.lean line 35): the [ASeq](#/node/ASeq) with constant k and step d. [Rake.term](#/node/Rake.term) uses it to read a term out of a rake.
