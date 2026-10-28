---
id: PrimeGt
title: 'PrimeGt n p: p is a prime above n'
summary: 'It is a two-word abbreviation that the whole library leans on: ''prime and bigger than n''.'
review: draft
authors:
- grok-bot
quiz:
- q: Is `PrimeGt 5 7` true?
  type: choice
  choices:
  - 'Yes'
  - 'No'
  answer: 0
  explain: 7 is prime and 5 < 7.
- q: Is `PrimeGt 5 5` true?
  type: choice
  choices:
  - 'Yes'
  - 'No'
  answer: 1
  explain: 5 < 5 is false.
- q: Is `PrimeGt 5 9` true?
  type: choice
  choices:
  - 'Yes'
  - 'No'
  answer: 1
  explain: 9 is not prime.
---
## Plain English

`PrimeGt n p := Nat.Prime p ∧ n < p` (PrimeGen.lean line 28). Used in [MinPrimeGt](#/node/MinPrimeGt) and [ex_prime_gt](#/node/ex_prime_gt).
