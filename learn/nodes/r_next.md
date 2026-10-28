---
id: r_next
title: 'Sieving by the next prime: R p₁ = R p₀ minus multiples of p₁'
summary: This is the sieve of Eratosthenes as one equation. Crossing out the multiples of the next prime is exactly
  the move from 'no prime factor ≤ p₀' to 'no prime factor ≤ p₁', because no prime lies in between.
review: draft
authors:
- grok-bot
quiz:
- q: Why must p₁ be the *least* prime above p₀?
  type: choice
  choices:
  - otherwise a prime between them would not be sieved out
  - for speed
  - it need not be
  answer: 0
  explain: If a prime q with p₀ < q < p₁ existed, R p₀ minus multiples of p₁ would still contain q, but q ∉ R p₁.
- q: Which numbers are in R 3 but not R 5?
  type: choice
  choices:
  - multiples of 5 that have no factor 2 or 3, like 5, 25, 35
  - all multiples of 5
  - primes
  answer: 0
  explain: R 5 = R 3 minus multiples of 5 (5 is the least prime above 3).
- q: Where is this used?
  type: choice
  choices:
  - in the RakeSieve step, via `r_next_prop`
  - nowhere
  - in SimpleGen
  answer: 0
  explain: RakeSieve.lean line 96.
---
## Plain English

**R stands for *residue*.** R p is the set of numbers ≥ 2 that no prime ≤ p divides: what is left after crossing out the multiples of every prime up to p ([R](#/node/R)). For example, R 2 is the odd numbers from 3 up.

**Theorem (`r_next`, PrimeSieve.lean lines 60–96).** Let p₁ be the least prime greater than p₀ (a [MinPrimeGt](#/node/MinPrimeGt) p₀). Then for every n:

n ∈ [R](#/node/R) p₀ and p₁ ∤ n **if and only if** n ∈ R p₁.

Left to right is the interesting part: a prime q ≤ p₁ dividing n is either ≤ p₀ (excluded by n ∈ R p₀), equal to p₁ (excluded by p₁ ∤ n), or strictly between p₀ and p₁, which cannot happen because p₁ is the *least* prime above p₀. (The Lean argues through a prime factor f of q, which makes the case split work for any q.)

Its companion [r_next_prop](#/node/r_next_prop) restates it for predicates, which is how the RakeSieve uses it.
