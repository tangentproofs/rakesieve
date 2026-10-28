---
id: MinPrimeGt
title: 'MinPrimeGt n: the least prime above n, with proof'
summary: '''The next prime'' is a structure, not a number: the number, a proof it is a prime above n, and a proof
  nothing smaller is.'
review: draft
authors:
- grok-bot
quiz:
- q: What does `hmin` say?
  type: choice
  choices:
  - no q < p is a prime greater than n
  - p is minimal among all primes
  answer: 0
  explain: '`∀q:Nat, q < p → (¬ PrimeGt n q)`.'
- q: Is MinPrimeGt 7 unique?
  type: choice
  choices:
  - its number p must be 11
  - p could be 11 or 13
  answer: 0
  explain: 11 is the least prime above 7, and `hmin` rules out anything else.
- q: Which lemma about R needs a MinPrimeGt?
  type: choice
  choices:
  - '`r_next`'
  - '`r_gt_p`'
  answer: 0
  explain: Sieving by the *next* prime.
---
## Plain English

A `MinPrimeGt n` (PrimeGen.lean lines 31–34) has a number p, a proof `hpgt` that p is prime and n < p ([PrimeGt](#/node/PrimeGt)), and a proof `hmin` that no q < p is a prime above n. So p is *the* next prime after n. [min_prime_gt](#/node/min_prime_gt) builds one with `Nat.find`; [RakeSieve.next](#/node/RakeSieve.next) builds one from the sieve's candidate.
