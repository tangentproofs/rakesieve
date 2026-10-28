---
id: List.Sorted
title: 'List.Sorted: a local stand-in for ''sorted by r'''
summary: '**The surprise:** the library defines its own `List.Sorted` as `List.Pairwise`, a small shim kept so the
  code survives Mathlib renaming its sorted-list API.'
review: draft
authors:
- grok-bot
quiz:
- q: Is [2, 5, 9] `Sorted (· < ·)`?
  type: choice
  choices:
  - 'Yes'
  - 'No'
  answer: 0
  explain: Each pair in order satisfies <.
- q: Is [2, 2, 3] `Sorted (· < ·)`?
  type: choice
  choices:
  - 'Yes'
  - 'No'
  answer: 1
  explain: 2 < 2 fails.
- q: Why define it locally?
  type: choice
  choices:
  - it is an abbreviation for `List.Pairwise`, kept stable across Mathlib versions
  - Mathlib has no lists
  answer: 0
  explain: Rake.lean lines 9–13.
---
## Plain English

`List.Sorted r l := l.Pairwise r` (Rake.lean line 11): every earlier element is related to every later one. With r = (<), it means strictly increasing. [Rake](#/node/Rake) uses it for its constant list.
