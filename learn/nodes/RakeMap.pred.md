---
id: RakeMap.pred
title: 'RakeMap.pred: the property a rake map describes'
summary: It ignores its argument's contents entirely; the predicate lives in the type, and this just reads it back.
review: draft
authors:
- grok-bot
quiz:
- q: 'What does `rm.pred` return for `rm : RakeMap p`?'
  type: choice
  choices:
  - p
  - the rake
  answer: 0
  explain: Definition.
- q: Does it inspect the rake?
  type: choice
  choices:
  - 'No'
  - 'Yes'
  answer: 0
  explain: The argument is unused (`_`).
- q: Where is it used?
  type: choice
  choices:
  - RakeSieve.init and next set `prop := rm.pred`
  - nowhere
  answer: 0
  explain: RakeSieve.lean lines 26 and 97.
---
## Plain English

`pred (_ : RakeMap p) := p` (RakeMap.lean line 15). Used to name a [RakeMap](#/node/RakeMap)'s predicate, e.g. `prop := rm.pred` in [RakeSieve.init](#/node/RakeSieve.init).
