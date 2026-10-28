---
id: RakeSieve.survivor
title: 'RakeSieve.survivor: the rake proves it never runs empty'
summary: The sieve finds its own survivor without asking anyone for a bigger prime. The candidate c sits somewhere
  in the rake, one full turn later the rake produces c + d, and c cannot divide c + d.
review: draft
authors:
- grok-bot
caveats:
- Euclid's argument in the sieve's own terms. It removes the circularity, not Euclid's idea.
quiz:
- q: Why is c + d a term of the rake?
  type: choice
  choices:
  - one period past term m₀ = c, by `Rake.term_add_len`
  - because c + d is prime
  - by `decide`
  answer: 0
  explain: '`rw [Rake.term_add_len, hm₀]` (RakeSieve.lean line 82).'
- q: Which invariant rules out c ∣ d?
  type: choice
  choices:
  - '`hdfac`: every prime factor of d is ≤ p'
  - '`hRmin`'
  - '`hprop`'
  answer: 0
  explain: '`s.hdfac s.c hC hcd` (RakeSieve.lean line 78).'
- q: Does it need c to be prime?
  type: choice
  choices:
  - 'Yes: `hdfac` speaks about prime factors, so it is applied to c as a prime'
  - 'No'
  answer: 0
  explain: 'The hypothesis `hC : Nat.Prime s.c`.'
---
## Plain English

**R stands for *residue*.** R p is the set of numbers ≥ 2 that no prime ≤ p divides: what is left after crossing out the multiples of every prime up to p ([R](#/node/R)). For example, R 2 is the odd numbers from 3 up.

**Theorem (`RakeSieve.survivor`, RakeSieve.lean lines 72–82).** For every [RakeSieve](#/node/RakeSieve) state s whose candidate c is prime, some term of the rake is not a multiple of c. Exported as [results_rakeSieve_never_empty](#/node/results_rakeSieve_never_empty), which has the proof outline. [RakeSieve.next](#/node/RakeSieve.next) uses it to call [RakeMap.rem](#/node/RakeMap.rem).

The witness is c + d, where d is the rake's period (the common step of its sequences):

- c is in R p, so it is a term of the rake, say term m₀;
- [Rake.term_add_len](#/node/Rake.term_add_len): term (m₀ + len) = c + d;
- if c divided c + d, it would divide d, so c ≤ p by the invariant `hdfac`. But c > p ([r_gt_p](#/node/r_gt_p)).

The docstring (RakeSieve.lean lines 64–71) says plainly that this is Euclid's argument, with c + p# in the part of p# + 1. The difference is that it is carried by the data structure, and no infinitude theorem is imported.
