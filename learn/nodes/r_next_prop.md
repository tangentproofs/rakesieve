---
id: r_next_prop
title: 'r_next for predicates: how a sieve tracks R step by step'
summary: The RakeSieve never computes R directly. It carries a predicate, adds '∧ not a multiple of c' at each step,
  and this lemma certifies that the predicate still means exactly R.
review: draft
authors:
- grok-bot
quiz:
- q: What is h₁ in the RakeSieve step?
  type: choice
  choices:
  - the predicate of the rake after removing multiples of the new prime
  - the list of primes
  - the candidate
  answer: 0
  explain: '`h₁ := rs.pred`, with `rs = rs₀.rm.rem c''.p …` (RakeSieve.lean lines 87–94).'
- q: What does the lemma conclude?
  type: choice
  choices:
  - h₁ describes R of the new prime
  - h₁ is decidable
  - h₀ = h₁
  answer: 0
  explain: '`h₁ n ↔ n ∈ R m.p`.'
- q: Which lemma does it rest on?
  type: choice
  choices:
  - '`r_next`'
  - '`c_prime`'
  - '`r_gt_p`'
  answer: 0
  explain: The proof is `simp[hh₁, hh₀]; exact r_next p₀ m`.
---
## Plain English

**Theorem (`r_next_prop`, PrimeSieve.lean lines 110–114).** Suppose h₀ n ↔ n ∈ [R](#/node/R) p₀, and h₁ n ↔ h₀ n ∧ ¬ (m.p ∣ n), where m.p is the least prime above p₀. Then h₁ n ↔ n ∈ R m.p.

It is [r_next](#/node/r_next) with names for the two predicates. The comment above it (PrimeSieve.lean lines 98–109) explains the design: a sieve models R p by a bijection with its data structure, and whatever it does to sift out the next prime corresponds to adding `∧ ¬(p₁∣n)` to the predicate. The RakeSieve uses it once per step (RakeSieve.lean line 96).
