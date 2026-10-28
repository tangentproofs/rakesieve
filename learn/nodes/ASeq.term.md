---
id: ASeq.term
title: 'ASeq.term: the n-th term, k + d·n'
summary: An ASeq can be used as a function (s n) because of a coercion that points at this one line.
review: draft
authors:
- grok-bot
quiz:
- q: '`(aseq 0 2).term 10` is'
  type: choice
  choices:
  - '20'
  - '12'
  - '10'
  answer: 0
  explain: 0 + 2·10, checked by the `#guard` on ASeq.lean line 50.
- q: Is term 0 always k?
  type: choice
  choices:
  - 'Yes'
  - 'No'
  answer: 0
  explain: k + d·0 = k.
- q: Do terms ever decrease?
  type: choice
  choices:
  - No, d·n grows with n (or stays fixed if d = 0)
  - 'Yes'
  answer: 0
  explain: d is a natural number.
---
## Plain English

`term s n = s.k + s.d * n` (ASeq.lean line 45). A `CoeFun` instance (line 48) lets you write `s n` for it. See [ASeq](#/node/ASeq).
