---
id: results_exists_prime_gt_of_rakeSieve
title: 'Corollary: infinitely many primes, from the sieve'
summary: 'The statement is Euclid''s theorem, but the proof imports no infinitude result: the sieve never runs empty
  and its primes keep going up, so they pass any n. Infinitude of primes is a corollary of the algorithm, not an
  input to it.'
review: draft
authors:
- grok-bot
caveats:
- The statement is Euclid's theorem and says nothing about the sieve. The sieve's correctness is stated by the step
  and every-prime headlines.
- The mathematical idea is Euclid's (c + p# in place of p# + 1). What is new is that the sieve carries it, so the
  proof is not circular.
- 'This site did not build the Lean. The no-Euclid check and `#print axioms` were run on the tcode server for PR
  #5; see the Trust page.'
widgets:
- type: walkthrough
  title: How Results.lean proves it (Results.lean, lines 46-48)
  config:
    steps:
    - text: 'Start the sieve: RakeSieve.init has found the prime 2, and its rake lists exactly the odd numbers ≥
        3'
      lean: '{ state := RakeSieve.init }'
      link: RakeSieve.init
      note: The initial state carries proofs that 3 is in R 2 (the residue left after crossing out multiples of
        2), that nothing in R 2 is below 3, and that the rake's period, 2, has no prime factor above 2.
    - text: 'Wrap it as a PrimeSieve. The generic driver makes any PrimeSieve a PrimeGen: each step gives the next
        prime, strictly larger, none skipped'
      lean: PrimeSieve RakeSieve
      link: instPrimeGenPrimeSieve
      note: 'Lean finds this by type-class search: RakeSieve has PrimeSieveState and PrimeSieveDriver instances,
        so PrimeSieve RakeSieve has a PrimeGen instance.'
    - text: 'Apply the general fact: a prime generator whose primes strictly increase passes any n after n + 1 steps'
      lean: exists_prime_gt_of_primeGen
      link: exists_prime_gt_of_primeGen
      note: The primes go up by at least 1 per step, and start at 2 or more, so after n + 1 steps the prime is at
        least n + 3.
- type: walkthrough
  title: What one sieve step does (RakeSieve.lean, lines 84-136)
  config:
    steps:
    - text: The candidate c is prime and no prime lies between p and c (supplied by the driver), so c is the least
        prime above p
      lean: 'let c'' : MinPrimeGt rs₀.p := { p:=rs₀.c, hpgt:=hpgt, hmin:=hmin}'
      link: MinPrimeGt
    - text: 'Show that removing c''s multiples leaves something: the rake''s own term c + d survives'
      lean: 'have hsurv : ∃n m, ¬rs₀.c ∣ n ∧ rs₀.rm.term m = n := rs₀.survivor hC₀'
      link: RakeSieve.survivor
      note: This line used to call Mathlib's Nat.exists_infinite_primes. Now the rake supplies the witness itself.
    - text: Remove the multiples of c from the rake (partition each sequence into c sequences, drop those whose
        constant is a multiple of c, sort)
      lean: let rs := rs₀.rm.rem c'.p (Nat.Prime.pos hC₀) hsurv
      link: RakeMap.rem
    - text: The new candidate is the rake's first term
      lean: let c₁ := rs.rake.term 0
      link: Rake.term
    - text: 'The new rake lists exactly R c: numbers ≥ 2 with no prime factor up to c'
      lean: intro n; exact r_next_prop (hh₀ n) (hh₁ n)
      link: r_next_prop
    - text: Its first term is its least term, because the rake is sorted, so the new candidate is the minimum of
        R c
      lean: exact rs.min_term_zero k
      link: RakeMap.min_term_zero
    - text: 'Keep the invariant: the new period is d · c, so its prime factors are those of d (all ≤ p < c) and
        c itself'
      lean: 'have hd : rs.rake.d = rs₀.rm.rake.d * rs₀.c := RakeMap.rem_d _ _ _ _'
      link: RakeMap.rem_d
quiz:
- q: What does the *statement* of `results_exists_prime_gt_of_rakeSieve` mention?
  type: choice
  choices:
  - The RakeSieve and its initial state
  - Only `Nat.Prime`, `<` and the natural numbers
  - The list of primes the sieve produces
  - The growth rate of the rake
  answer: 1
  explain: The statement is `∀ n, ∃ p, Nat.Prime p ∧ n < p` (Results.lean lines 46–47). RakeSieve appears only in
    the proof term on line 48.
- q: Does the proof use Mathlib's infinitude of primes anywhere?
  type: choice
  choices:
  - Yes, inside every sieve step
  - 'No: each step''s survivor is c + d, built from the rake itself, and NoEuclidCheck.lean confirms that no infinitude
    theorem is reachable'
  answer: 1
  explain: RakeSieve.next gets its survivor from `rs₀.survivor hC₀` (RakeSieve.lean line 98).
- q: Which classical argument does the survivor c + d echo?
  type: choice
  choices:
  - Euclid's p# + 1
  - Eratosthenes' p² bound
  - Bertrand's postulate
  answer: 0
  explain: d is the product of the primes sifted so far, so c + d plays the part of p# + 1.
- q: Where is the claim 'each RakeSieve step yields the next prime, none skipped' stated?
  type: choice
  choices:
  - Nowhere
  - In `results_rakeSieve_step`, and generically in the `PrimeGen (PrimeSieve α)` instance
  - Only in `Main.lean`'s `#eval`
  answer: 1
  explain: Results.lean lines 27–31 state it for every RakeSieve state.
---
## Plain English

**Theorem (`results_exists_prime_gt_of_rakeSieve`, Results.lean lines 46–48).** For every natural number n there is a prime p with n < p.

The statement never mentions the sieve. Only the proof does: start the RakeSieve at [RakeSieve.init](#/node/RakeSieve.init), wrap it as a [PrimeSieve](#/node/PrimeSieve), which is a prime generator by [the sieve driver](#/node/instPrimeGenPrimeSieve), and apply [exists_prime_gt_of_primeGen](#/node/exists_prime_gt_of_primeGen): a generator whose primes strictly increase passes any n.

### What this does and does not show

- **As a statement, it is Euclid's theorem.** Mathlib already has it (`Nat.exists_infinite_primes`).
- **As a proof, it does not use Mathlib's Euclid.** Every sieve step must know that crossing out the new prime's multiples leaves something in the rake. The rake now proves that itself, with the survivor c + d ([the never-empty headline](#/node/results_rakeSieve_never_empty)). NoEuclidCheck.lean walks the full dependency closure of this theorem, through Mathlib and core, and finds nothing from `Mathlib.Data.Nat.Prime.Infinite` or a list of known infinitude results. A control check confirms that the same walk does find Euclid in the circular [reference generator](#/node/simpleGen_exists_prime_gt).
- **The idea is still Euclid's.** The survivor c + d works because d, the rake's period, is the product of the primes sifted so far. This is Euclid's p# + 1 carried by the data structure. It is not a new kind of proof, but it is no longer circular.
- **The sieve's correctness has its own headlines:** [each step emits the next prime](#/node/results_rakeSieve_step) and [every prime is emitted](#/node/results_rakeSieve_emits_every_prime).

### The outline

The proof is one line (Results.lean line 48). The outline below follows it, then shows what one sieve step does.
