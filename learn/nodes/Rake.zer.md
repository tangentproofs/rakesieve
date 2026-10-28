---
id: Rake.zer
title: 'Rake.zer: the placeholder rake {0}'
summary: It exists only so `rem` always returns something; the sieve proves it is never actually reached.
review: draft
authors:
- grok-bot
quiz:
- q: What are its terms?
  type: choice
  choices:
  - only 0
  - all numbers
  answer: 0
  explain: Step 0 and constant 0 give 0 forever.
- q: When does `rem` return it?
  type: choice
  choices:
  - when every constant is a multiple of j
  - never, by definition
  answer: 0
  explain: See Rake.lean line 361.
- q: Does the sieve ever reach it?
  type: choice
  choices:
  - No, HasNonMultiple rules it out
  - 'Yes'
  answer: 0
  explain: That is why RakeMap.rem asks for a non-multiple.
---
## Plain English

`zer := { d := 0, ks := [0] }` (Rake.lean line 26): the rake whose only term is 0. [Rake.rem](#/node/Rake.rem) returns it if every sequence would be removed; `rem_def` (Rake.lean lines 370–409) shows that cannot happen when the rake has a non-multiple.
