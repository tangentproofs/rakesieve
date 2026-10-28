---
id: Rake.HasNonMultiple
title: 'HasNonMultiple: some term is not a multiple of j'
summary: '**The surprise:** this innocent hypothesis is where Euclid enters the sieve: proving it at each step is
  what needs Mathlib''s infinitude of primes.'
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
  - with a prime above c from Mathlib
  - by `decide`
  answer: 0
  explain: RakeSieve.lean line 71.
---
## Plain English

`HasNonMultiple r j := ∃ n, ¬ j ∣ n ∧ ∃ m, r.term m = n` (Rake.lean line 364): the rake r has a term not divisible by j. [Rake.rem](#/node/Rake.rem)'s theorems need it; [RakeMap.rem](#/node/RakeMap.rem) asks for it as an argument; [RakeSieve.next](#/node/RakeSieve.next) proves it with a prime from `Nat.exists_infinite_primes`.
