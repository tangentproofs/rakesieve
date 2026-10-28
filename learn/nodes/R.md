---
id: R
title: 'R P: the numbers that survive sieving by every prime up to P'
summary: The whole sieve is driven by this one set. Its least element is always the next prime, and sieving by a
  new prime p is exactly the step from R (previous prime) to R p.
review: draft
authors:
- grok-bot
quiz:
- q: Is 9 in R 2?
  type: choice
  choices:
  - 'Yes'
  - 'No'
  answer: 0
  explain: 9 ≥ 2 and the only prime ≤ 2 is 2, which does not divide 9.
- q: Is 9 in R 3?
  type: choice
  choices:
  - 'Yes'
  - 'No'
  answer: 1
  explain: 3 ≤ 3 is prime and divides 9.
- q: What is the least element of R 5?
  type: choice
  choices:
  - '6'
  - '7'
  - '25'
  answer: 1
  explain: R 5 drops multiples of 2, 3 and 5; 6 is a multiple of 2, so the least survivor is 7, the next prime.
- q: Does R P contain only primes?
  type: choice
  choices:
  - 'Yes'
  - No, e.g. 25 ∈ R 3
  answer: 1
  explain: 25 = 5·5 has no prime factor ≤ 3.
---
## Plain English

`R P = { n | n ≥ 2 ∧ ∀ q ≤ P, q prime → ¬ q ∣ n }` (PrimeSieve.lean line 16). The comment calls it the "residue": the numbers from 2 up that no prime ≤ P divides. These are what is left after the sieve of Eratosthenes has crossed out the multiples of every prime up to P.

Examples: R 2 = {3, 5, 7, 9, 11, …} (odd numbers ≥ 3); R 3 = {5, 7, 11, 13, 17, 19, 23, 25, …}.

Three facts make it useful:
- everything in R P is bigger than P ([r_gt_p](#/node/r_gt_p));
- the least element of R P is the next prime after P ([c_prime](#/node/c_prime), [no_skipped_prime](#/node/no_skipped_prime));
- if p₁ is the next prime after p₀, then R p₁ = R p₀ minus the multiples of p₁ ([r_next](#/node/r_next)).

Note that R P is defined for any number P, prime or not, and contains composites (25 ∈ R 3).
