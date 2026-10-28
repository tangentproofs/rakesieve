---
id: no_prime_factors_im_no_factors
title: No prime factor below c means c is prime
summary: '**The surprise:** the library proves this small classical fact by hand rather than finding it in Mathlib:
  a number ≥ 2 with no prime factor below it has no factor at all but 1 and itself.'
review: draft
authors:
- grok-bot
quiz:
- q: Is the hypothesis 'no prime p < c divides c' enough without c ≥ 2?
  type: choice
  choices:
  - 'Yes'
  - 'No: c = 1 has no prime factors and is not prime'
  answer: 1
  explain: 'Hence `h2lc : 2 ≤ c`.'
- q: Which characterization of primes closes the proof?
  type: choice
  choices:
  - '`Nat.prime_def_lt`'
  - Wilson's theorem
  - '`Nat.Prime.two_le`'
  answer: 0
  explain: PrimeSieve.lean line 170.
- q: Does 25 satisfy the hypothesis?
  type: choice
  choices:
  - 'Yes'
  - 'No: 5 < 25 is prime and divides 25'
  answer: 1
  explain: So the lemma says nothing about 25.
---
## Plain English

**Lemma (`no_prime_factors_im_no_factors`, PrimeSieve.lean lines 153–170).** If c ≥ 2 and no prime p < c divides c, then c is prime.

Proof: a divisor m < c with m ≠ 1 would have a prime factor p, which divides c and is ≤ m < c, contradiction. So the only divisors below c are 1, which is Mathlib's `Nat.prime_def_lt`.

Used by [c_prime](#/node/c_prime).
