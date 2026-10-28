---
id: exists_prime_gt_of_primeGen
title: A generator whose primes strictly increase passes every n
summary: '**The surprise:** no number theory at all, just counting: the prime goes up by at least one per step and
  starts at 2 or more, so after n + 1 steps it exceeds n.'
review: draft
authors:
- grok-bot
quiz:
- q: Which witness does the proof offer?
  type: choice
  choices:
  - the prime after n + 1 steps
  - n + 1
  - the least prime above n
  answer: 0
  explain: '`P (next^[k] g₀)` with k = n + 1.'
- q: Is it ever tight, i.e. is the witness the *least* prime above n?
  type: choice
  choices:
  - not necessarily; the proof only needs some prime above n
  - always
  answer: 0
  explain: The witness can be far above n.
- q: Which field of PrimeGen is used?
  type: choice
  choices:
  - '`hP_lt`'
  - '`hP''`'
  answer: 0
  explain: Via `P_iterate_add_le`.
---
## Plain English

**Theorem (`exists_prime_gt_of_primeGen`, PrimeGen.lean lines 112–118).** For any [PrimeGen](#/node/PrimeGen) α, any state g₀ and any n, some prime p satisfies n < p.

The witness is the generator's prime after n + 1 steps. By [PrimeGen.P_iterate_add_le](#/node/PrimeGen.P_iterate_add_le) it is at least P g₀ + n + 1 ≥ n + 3. It is prime because generator values are [NPrime](#/node/NPrime)s. This is what [results_exists_prime_gt_of_primeGen](#/node/results_exists_prime_gt_of_primeGen) exports.
