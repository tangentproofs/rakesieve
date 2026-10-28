---
id: results_exists_prime_gt_of_rakeSieve
title: 'Main theorem: the RakeSieve never runs out of primes'
summary: '**The surprise:** the statement never mentions the sieve. It is word for word Euclid''s theorem, ∀ n,
  ∃ prime p > n, and the proof calls Mathlib''s own proof of Euclid inside each sieve step. The sieve only appears
  in the proof.'
review: draft
authors:
- grok-bot
caveats:
- The statement is Euclid's theorem and says nothing about the sieve. Read it as 'the sieve, run forever, keeps
  producing primes', not as 'the sieve is correct'.
- 'The proof is not independent of Mathlib''s infinitude of primes: RakeSieve.next uses `Nat.exists_infinite_primes`
  (RakeSieve.lean line 71).'
- This site did not build the Lean. The statement and proof are read from the source text at commit 36e7360; see
  the Trust page.
widgets:
- type: walkthrough
  title: How Results.lean proves it (Results.lean, lines 19-21)
  config:
    steps:
    - text: 'Start the sieve: RakeSieve.init has found the prime 2, and its rake lists exactly the odd numbers ≥
        3'
      lean: '{ state := RakeSieve.init }'
      link: RakeSieve.init
      note: The initial state carries proofs that 3 is in R 2 and that nothing in R 2 is below 3 (the two other
        headline theorems).
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
  title: What one sieve step does (RakeSieve.lean, lines 55-111)
  config:
    steps:
    - text: The candidate c is prime and no prime lies between p and c (supplied by the driver), so c is the least
        prime above p
      lean: 'let c'' : MinPrimeGt rs₀.p := { p:=rs₀.c, hpgt:=hpgt, hmin:=hmin}'
      link: MinPrimeGt
    - text: 'Show that removing c''s multiples leaves something: Mathlib gives a prime q > c, and q is in R p but
        is not a multiple of c'
      lean: Nat.exists_infinite_primes rs₀.c.succ
      note: This is the step that uses Mathlib's Euclid. Without it, the rake operation `rem` would have no guarantee
        of a non-empty result.
    - text: Remove the multiples of c from the rake (partition each sequence into c sequences, drop those whose
        constant is a multiple of c, sort)
      lean: let rs := rs₀.rm.rem c'.p (Nat.Prime.pos hC₀) this
      link: RakeMap.rem
    - text: The new candidate is the rake's first term
      lean: let c₁ := rs.rake.term 0
      link: Rake.term
    - text: 'The new rake lists exactly R c: numbers ≥ 2 with no prime factor up to c'
      lean: intro n; exact r_next_prop (hh₀ n) (hh₁ n)
      link: r_next_prop
    - text: Its first term is its least term, because the rake is sorted, so the new candidate is the minimum of
        R c
      lean: exact rs.min_term_zero k }
      link: RakeMap.min_term_zero
quiz:
- q: What does the *statement* of `results_exists_prime_gt_of_rakeSieve` mention?
  type: choice
  choices:
  - The RakeSieve and its initial state
  - Only `Nat.Prime`, `<` and the natural numbers
  - The list of primes the sieve produces
  - The growth rate of the rake
  answer: 1
  explain: The statement is `∀ n, ∃ p, Nat.Prime p ∧ n < p` (Results.lean lines 19–20). RakeSieve appears only in
    the proof term on line 21.
- q: Which other theorem in Results.lean has exactly the same statement?
  type: choice
  choices:
  - '`results_three_mem_R_two`'
  - '`results_exists_prime_gt_of_simpleGen`'
  - '`results_three_le_of_mem_R_two`'
  - none
  answer: 1
  explain: '`results_exists_prime_gt_of_simpleGen (n : Nat) : ∃ p, Nat.Prime p ∧ n < p` has the same type; it runs
    the brute-force `SimpleGen` instead of the RakeSieve.'
- q: Does the proof use Mathlib's infinitude of primes anywhere?
  type: choice
  choices:
  - No, it is a self-contained proof of Euclid
  - 'Yes: `RakeSieve.next` calls `Nat.exists_infinite_primes` to show the rake never becomes empty'
  - Only through `decide`
  answer: 1
  explain: 'RakeSieve.lean line 71: `Nat.exists_infinite_primes rs₀.c.succ` gives a prime q > c, which survives
    the removal of c''s multiples.'
- q: Where is the claim 'each RakeSieve step yields the next prime, none skipped' checked?
  type: choice
  choices:
  - In the statement of this theorem
  - In the `PrimeGen (PrimeSieve α)` instance and the generic driver lemmas it uses
  - Only in `Main.lean`'s `#eval`
  - It is not checked
  answer: 1
  explain: The `PrimeGen` class (PrimeGen.lean lines 19–26) demands `hP'` (no skipped prime) and `hP_lt` (strict
    increase). The instance for `PrimeSieve α` proves both from `c_prime`, `no_skipped_prime` and `c_gt_p`.
---
## Plain English

**Theorem (`results_exists_prime_gt_of_rakeSieve`, Results.lean lines 19–21).** For every natural number n there is a prime p with n < p.

That is the whole statement. Nothing in it says "RakeSieve". The name says *how* it was proved: by starting the RakeSieve at [RakeSieve.init](#/node/RakeSieve.init), wrapping it as a [PrimeSieve](#/node/PrimeSieve), which is a prime generator by [the sieve driver](#/node/instPrimeGenPrimeSieve), and applying the general fact [exists_prime_gt_of_primeGen](#/node/exists_prime_gt_of_primeGen): a generator whose primes strictly increase must eventually pass any n.

### What this does and does not show

- **As a statement, it is Euclid's theorem.** Mathlib already has it (`Nat.exists_infinite_primes`). Two of the five theorems in Results.lean have exactly this statement; only the proofs differ.
- **As a proof, it is not independent of Euclid.** One sieve step, [RakeSieve.next](#/node/RakeSieve.next), must show that removing the multiples of the new prime c leaves *something* in the rake, so that the rake is never empty. It does this by asking Mathlib for a prime above c (`Nat.exists_infinite_primes`, RakeSieve.lean line 71). So the proof uses the theorem it states. This is not a flaw in the Lean (nothing is assumed that isn't proved), but the theorem should not be read as "a new proof that there are infinitely many primes".
- **What the proof does exercise** is the sieve's correctness: to build the generator, Lean has to accept that every RakeSieve step yields the next prime with none skipped. That guarantee is the real content, and it lives in an instance rather than a named theorem; see [instPrimeGenPrimeSieve](#/node/instPrimeGenPrimeSieve) and [the review](#/review).

### The outline

The proof is one line (Results.lean line 21). The outline below follows it, then shows what one sieve step does.
