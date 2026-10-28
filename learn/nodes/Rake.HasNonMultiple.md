---
id: Rake.HasNonMultiple
title: 'HasNonMultiple: some term is not a multiple of j'
summary: This innocent hypothesis is where Euclid's idea enters the sieve. The RakeSieve proves it at every step
  with its own survivor, c + d, instead of importing infinitude of primes.
review: draft
authors:
- grok-bot
quiz:
- q: Does {d = 2, ks = [4]} have a non-multiple of 2?
  type: choice
  choices:
  - 'No'
  - 'Yes'
  answer: 0
  explain: 4 + 2n is always even.
- q: Does {d = 2, ks = [3]} have a non-multiple of 3?
  type: choice
  choices:
  - Yes, e.g. 5
  - 'No'
  answer: 0
  explain: 5 = 3 + 2·1.
- q: How does the RakeSieve prove it?
  type: choice
  choices:
  - with its own term c + d, one period past c
  - with a prime above c from Mathlib
  - by `decide`
  answer: 0
  explain: '`RakeSieve.survivor` (RakeSieve.lean lines 72–82).'
---
## Plain English

`HasNonMultiple r j := ∃ n, ¬ j ∣ n ∧ ∃ m, r.term m = n` (Rake.lean line 371): the rake r has a term not divisible by j. [Rake.rem](#/node/Rake.rem)'s theorems need it; [RakeMap.rem](#/node/RakeMap.rem) asks for it as an argument; [RakeSieve.next](#/node/RakeSieve.next) proves it with [RakeSieve.survivor](#/node/RakeSieve.survivor): the term c + d is not a multiple of c.
