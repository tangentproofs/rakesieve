---
id: instPrimeGenPrimeSieve
title: 'The sieve driver: every PrimeSieve is a prime generator'
summary: 'The sieve''s correctness is proved once, for every sieve at the same time: any sieve state whose candidate
  is the least survivor gives, step by step, the next prime with none skipped. The RakeSieve headlines restate it
  for the RakeSieve.'
review: draft
authors:
- grok-bot
caveats:
- This is an `instance`, so it has no name in the source; this site calls it `instPrimeGenPrimeSieve`, the name
  Lean most likely generates. The exact generated name was not checked (no Lean build).
- Completeness ('every prime appears') is stated separately, as `results_rakeSieve_emits_every_prime`.
widgets:
- type: walkthrough
  title: How the instance is proved (PrimeSieve.lean, lines 218-242)
  config:
    steps:
    - text: The generator's prime is the state's prime; a step runs the sieve once
      lean: next := PrimeSieve.next (α := α)
      link: PrimeSieve.next
    - text: 'From the driver: the candidate C is prime, and no prime lies strictly between P and C'
      lean: have hc' := c_prime α s.state
      uses:
      - c_prime
      - no_skipped_prime
    - text: 'The state''s hNext field: after one step, the new prime P is the old candidate C'
      lean: (PrimeSieveState.hNext (α := α) s.state hc' hns rfl).left
      link: PrimeSieveState
    - text: 'No skipped prime: a prime between P and the new P would lie between P and C, which no_skipped_prime
        rules out'
      lean: exact hns ⟨q, hq, hgt', hlt'⟩
      link: no_skipped_prime
    - text: 'Strict increase: the new P is C, and C > P'
      lean: have hgt := c_gt_p α s.state
      link: c_gt_p
quiz:
- q: What are the two facts a `PrimeGen` instance must prove?
  type: choice
  choices:
  - the prime is even, and it is less than 100
  - no prime lies strictly between the current prime and the next one, and the next prime is bigger
  - the state is finite, and it is sorted
  - the sieve terminates
  answer: 1
  explain: 'PrimeGen.lean lines 22 and 26: `hP''` (no skipped prime) and `hP_lt` (strict increase).'
- q: Why can no prime q lie strictly between P and the candidate C?
  type: choice
  choices:
  - because q would be in R P, and C is the least element of R P
  - because q would divide C
  - because the rake is sorted
  - because of `decide`
  answer: 0
  explain: '`no_skipped_prime` (PrimeSieve.lean lines 133–151): a prime q > P has no prime factor ≤ P (its only
    prime factor is q), so q ∈ R P, and `hRmin` says C ≤ q.'
- q: Is 'the sieve started at 2 produces every prime' stated as a theorem?
  type: choice
  choices:
  - 'Yes: `results_rakeSieve_emits_every_prime` in Results.lean'
  - No, it is only implicit in this instance
  answer: 0
  explain: Results.lean lines 35–37, proved from this instance with `PrimeGen.exists_iterate_P_eq`.
- q: Which sieves does this instance cover?
  type: choice
  choices:
  - only the RakeSieve
  - any type with `PrimeSieveState` and `PrimeSieveDriver` instances
  - only SimpleGen
  answer: 1
  explain: 'It is stated for an arbitrary α under `variable (α : Type) [PrimeSieveState α] [PrimeSieveDriver α]`
    (PrimeSieve.lean line 210).'
---
## Plain English

**R stands for *residue*.** R p is the set of numbers ≥ 2 that no prime ≤ p divides: what is left after crossing out the multiples of every prime up to p ([R](#/node/R)). For example, R 2 is the odd numbers from 3 up.

**Instance (`instance : PrimeGen (PrimeSieve α)`, PrimeSieve.lean lines 218–242).** For any type α of sieve states that has a [PrimeSieveState](#/node/PrimeSieveState) and a [PrimeSieveDriver](#/node/PrimeSieveDriver) instance, the wrapper [PrimeSieve](#/node/PrimeSieve) α is a [PrimeGen](#/node/PrimeGen): a prime generator. Concretely:

- its current prime is the state's prime P;
- one step runs the sieve once ([PrimeSieve.next](#/node/PrimeSieve.next));
- **no prime is skipped**: there is no prime strictly between the current prime and the next one (`hP'`);
- **the prime goes up**: the next prime is strictly bigger (`hP_lt`).

Both facts come from three generic lemmas about any driven sieve state, where C is its candidate and R P is the set of numbers ≥ 2 with no prime factor up to P ([R](#/node/R)):

1. [c_prime](#/node/c_prime): C is prime, since its prime factors would be ≤ P (impossible, C is in R P) or between P and C (impossible, see 2);
2. [no_skipped_prime](#/node/no_skipped_prime): no prime lies strictly between P and C, since such a prime would be in R P and smaller than its minimum C;
3. [c_gt_p](#/node/c_gt_p): C > P, since everything in R P is bigger than P ([r_gt_p](#/node/r_gt_p)).

And the state's own `hNext` field says that one step turns C into the new P.

For the RakeSieve, α = [RakeSieve](#/node/RakeSieve): its states carry the proofs the driver needs ([the PrimeSieveDriver instance](#/node/RakeSieve.instPrimeSieveDriverRakeSieve)), so `PrimeSieve RakeSieve` is a prime generator. The every-prime headline and the infinitude corollary use it.

### What it adds up to

Starting from [RakeSieve.init](#/node/RakeSieve.init), whose prime is 2, these two facts mean the sieve lists 2, 3, 5, 7, 11, …, *all* the primes, in order. Results.lean now states this directly: [results_rakeSieve_step](#/node/results_rakeSieve_step) for a single step and [results_rakeSieve_emits_every_prime](#/node/results_rakeSieve_emits_every_prime) for "every prime is eventually produced". The second comes from the generic lemma [PrimeGen.exists_iterate_P_eq](#/node/PrimeGen.exists_iterate_P_eq).
