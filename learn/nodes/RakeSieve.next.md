---
id: RakeSieve.next
title: 'RakeSieve.next: remove the multiples of c, take the first term'
summary: 'To cross out c''s multiples, the step must first prove that something will survive, and the rake supplies
  the survivor itself: the term c + d, one period past c. No theorem about infinitely many primes is used.'
review: draft
authors:
- grok-bot
caveats:
- No infinitude theorem is used. The survivor is Euclid's idea (c + p# for p# + 1), carried by the invariant `hdfac`.
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
  - the rake's own term c + d, via `RakeSieve.survivor`
  - a prime q > c from `Nat.exists_infinite_primes`
  - '`decide`'
  answer: 0
  explain: '`have hsurv … := rs₀.survivor hC₀` (RakeSieve.lean line 98).'
- q: Why is the first term the least survivor?
  type: choice
  choices:
  - the rake is sorted, so term 0 is its minimum
  - by luck
  - it is proved by `decide`
  answer: 0
  explain: '`rs.min_term_zero k` (RakeSieve.lean line 125).'
- q: What is the new prime of the returned state?
  type: choice
  choices:
  - the old candidate c
  - the old prime + 2
  answer: 0
  explain: '`p := ⟨c''.p, hC₀⟩` where `c''.p = rs₀.c` (RakeSieve.lean line 111).'
---
## Plain English

**R stands for *residue*.** R p is the set of numbers ≥ 2 that no prime ≤ p divides: what is left after crossing out the multiples of every prime up to p ([R](#/node/R)). For example, R 2 is the odd numbers from 3 up.

`RakeSieve.next rs₀ hC₀ hNS` (RakeSieve.lean lines 84–136) takes a state, a proof that its candidate c is prime, and a proof that no prime lies between p and c ([nosk'](#/node/nosk')). It returns the state with prime c:

1. Package c as the least prime above p (a [MinPrimeGt](#/node/MinPrimeGt)), using [r_gt_p](#/node/r_gt_p) for c > p.
2. Prove that removing c's multiples leaves at least one term: [RakeSieve.survivor](#/node/RakeSieve.survivor) gives the term c + d, which c does not divide (RakeSieve.lean line 98).
3. Remove the multiples of c with [RakeMap.rem](#/node/RakeMap.rem) (RakeSieve.lean line 101).
4. The new candidate c₁ is the new rake's first term (RakeSieve.lean line 102).
5. The new predicate means R c, by [r_next_prop](#/node/r_next_prop) (RakeSieve.lean line 110); c₁ is in it, and is ≤ every term because the rake is sorted ([RakeMap.min_term_zero](#/node/RakeMap.min_term_zero), RakeSieve.lean line 125).

6. Re-prove the invariant `hdfac` for the new state. The new period is d · c ([RakeMap.rem_d](#/node/RakeMap.rem_d)), so its prime factors are those of d, all ≤ p < c, together with c itself (RakeSieve.lean lines 126–136).

Step 2 used to ask Mathlib for a prime above c (`Nat.exists_infinite_primes`). That made the sieve's infinitude corollary circular. The survivor c + d is the same idea as Euclid's p# + 1, but it is now built from the rake's own data.
