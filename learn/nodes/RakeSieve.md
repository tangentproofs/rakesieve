---
id: RakeSieve
title: 'RakeSieve: a sieve state that carries its own correctness proof'
summary: '**The surprise:** each state is data plus three proofs: its rake lists exactly R p, its candidate is in
  R p, and its candidate is below everything in R p. A wrong state cannot even be constructed.'
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
  explain: '`let c₁ := rs.rake.term 0` (RakeSieve.lean line 88).'
---
## Plain English

A `RakeSieve` (RakeSieve.lean lines 5–12) has:

- `prop : Nat → Prop` and `rm : RakeMap prop`: a [RakeMap](#/node/RakeMap), i.e. a rake (a sorted list of arithmetic sequences with a common step) whose terms are exactly the numbers satisfying `prop`;
- `p : NPrime`, the current prime, and `c : Nat`, the candidate;
- `hprop`: **prop n ↔ n ∈ [R](#/node/R) p**, so the rake's terms are exactly the survivors of sieving up to p;
- `hCinR`: c ∈ R p; `hRmin`: c ≤ r for every r ∈ R p.

So c is the least survivor, and by the generic lemmas it is the next prime. In the actual sieve, c is the rake's first term (RakeSieve.lean line 88).

The commented-out field `Q : Array RakeMap` is the planned queue of primes below p² (issue #2, open pull request #4), not in this version.
