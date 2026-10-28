---
id: RakeSieve
title: 'RakeSieve: a sieve state that carries its own correctness proof'
summary: 'Each state is data plus four proofs: its rake lists exactly the residue R p (the survivors of sieving
  up to p), its candidate is the least element of R p, and the rake''s period has no prime factor above p. That
  last proof keeps the sieve from ever running empty.'
review: draft
authors:
- grok-bot
caveats:
- 'The queue of primes below p² described in the README and issue #2 is on the unmerged branch `feature/rakesieve-queue-below-psq`
  (PR #4), not in main.'
quiz:
- q: What does `hprop` say?
  type: choice
  choices:
  - the rake's predicate holds exactly on R p
  - p is prime
  - the rake is sorted
  answer: 0
  explain: '`hprop : ∀ n:Nat, prop n ↔ n ∈ R p` (RakeSieve.lean line 10).'
- q: Can you build a `RakeSieve` whose candidate is not the least element of R p?
  type: choice
  choices:
  - 'Yes'
  - No, `hRmin` must be proved
  answer: 1
  explain: Every value of the structure includes the proof `hRmin`.
- q: Where does the candidate come from in `RakeSieve.next`?
  type: choice
  choices:
  - the rake's first term
  - '`Nat.find`'
  - a primality test
  answer: 0
  explain: '`let c₁ := rs.rake.term 0` (RakeSieve.lean line 102).'
- q: What does `hdfac` say?
  type: choice
  choices:
  - every prime factor of the rake's period is ≤ p
  - the rake has at most p sequences
  - c divides the period
  answer: 0
  explain: '`hdfac : ∀ q, Nat.Prime q → q ∣ rm.rake.d → q ≤ p.val` (RakeSieve.lean line 15).'
- q: Is `hdfac` an assumption that smuggles in infinitude of primes?
  type: choice
  choices:
  - 'No: like `hCinR`, it is a field proved at `init` and re-proved by every step'
  - 'Yes'
  answer: 0
  explain: RakeSieve.lean lines 57–62 prove it for `init` and lines 126–136 for `next`.
---
## Plain English

**R stands for *residue*.** R p is the set of numbers ≥ 2 that no prime ≤ p divides: what is left after crossing out the multiples of every prime up to p ([R](#/node/R)). For example, R 2 is the odd numbers from 3 up.

A `RakeSieve` (RakeSieve.lean lines 5–15) has:

- `prop : Nat → Prop` and `rm : RakeMap prop`: a [RakeMap](#/node/RakeMap), i.e. a rake (a sorted list of arithmetic sequences with a common step) whose terms are exactly the numbers satisfying `prop`;
- `p : NPrime`, the current prime, and `c : Nat`, the candidate;
- `hprop`: **prop n ↔ n ∈ [R](#/node/R) p**, so the rake's terms are exactly the survivors of sieving up to p;
- `hCinR`: c ∈ R p; `hRmin`: c ≤ r for every r ∈ R p;
- `hdfac` (RakeSieve.lean line 15): **every prime factor of the rake's period d is ≤ p**. The period is the common step of the rake's sequences. It starts at 2 and is multiplied by each new prime, so it is in fact p# = 2·3·5·…·p, though Lean only states the factor bound.

So c is the least survivor, and by the generic lemmas it is the next prime. `hdfac` is what lets the sieve prove it never runs empty: c is a prime above p, so it does not divide d, and so the term c + d survives when c's multiples are removed ([RakeSieve.survivor](#/node/RakeSieve.survivor)). In the actual sieve, c is the rake's first term (RakeSieve.lean line 102).

The commented-out field `Q : Array RakeMap` is the planned queue of primes below p² (issue #2, open pull request #4), not in this version.
