---
id: RakeSieve.next
title: 'RakeSieve.next: remove the multiples of c, take the first term'
summary: The step needs Mathlib's 'there is always a bigger prime' just to know the rake will not come out empty.
  The sieve's own correctness rests on Euclid, which is why its infinitude theorem is not an independent proof.
review: draft
authors:
- grok-bot
caveats:
- Uses Mathlib's `Nat.exists_infinite_primes` (RakeSieve.lean line 71); see the main theorem's caveats.
quiz:
- q: Why does the step need a non-multiple of c among the rake's terms?
  type: choice
  choices:
  - '`rem` requires a proof it won''t remove everything'
  - for speed
  - to sort the rake
  answer: 0
  explain: 'RakeMap.rem''s argument `hnmr: ∃n m, ¬j∣n ∧ rm.term m = n` (RakeMap.lean line 48).'
- q: Where does that non-multiple come from?
  type: choice
  choices:
  - a prime q > c from `Nat.exists_infinite_primes`
  - the number c + 1
  - '`decide`'
  answer: 0
  explain: RakeSieve.lean line 71.
- q: Why is the first term the least survivor?
  type: choice
  choices:
  - the rake is sorted, so term 0 is its minimum
  - by luck
  - it is proved by `decide`
  answer: 0
  explain: '`rs.min_term_zero k` (RakeSieve.lean line 111).'
- q: What is the new prime of the returned state?
  type: choice
  choices:
  - the old candidate c
  - the old prime + 2
  answer: 0
  explain: '`p := ⟨c''.p, hC₀⟩` where `c''.p = rs₀.c` (RakeSieve.lean line 97).'
---
## Plain English

**R stands for *residue*.** R p is the set of numbers ≥ 2 that no prime ≤ p divides: what is left after crossing out the multiples of every prime up to p ([R](#/node/R)). For example, R 2 is the odd numbers from 3 up.

`RakeSieve.next rs₀ hC₀ hNS` (RakeSieve.lean lines 55–111) takes a state, a proof that its candidate c is prime, and a proof that no prime lies between p and c ([nosk'](#/node/nosk')). It returns the state with prime c:

1. Package c as the least prime above p (a [MinPrimeGt](#/node/MinPrimeGt)), using [r_gt_p](#/node/r_gt_p) for c > p.
2. Prove that removing c's multiples leaves at least one term: Mathlib's `Nat.exists_infinite_primes` gives a prime q > c (RakeSieve.lean line 71); q is in R p, so it is a term of the rake, and c ∤ q.
3. Remove the multiples of c with [RakeMap.rem](#/node/RakeMap.rem) (RakeSieve.lean line 87).
4. The new candidate c₁ is the new rake's first term (RakeSieve.lean line 88).
5. The new predicate means R c, by [r_next_prop](#/node/r_next_prop) (RakeSieve.lean line 96); c₁ is in it, and is ≤ every term because the rake is sorted ([RakeMap.min_term_zero](#/node/RakeMap.min_term_zero), RakeSieve.lean line 111).

Step 2 could be replaced by an explicit witness, but that witness would essentially be Euclid's own argument (a number with no prime factor up to c), so the dependence is natural rather than accidental.
