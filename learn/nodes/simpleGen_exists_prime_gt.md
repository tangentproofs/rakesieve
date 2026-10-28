---
id: simpleGen_exists_prime_gt
title: 'Reference only: Euclid via the brute-force generator (circular)'
summary: Kept as a reference specification, not as evidence. The 'simple' generator finds each next prime by asking
  Mathlib for a prime above it, so it assumes the very theorem it proves.
review: draft
authors:
- grok-bot
caveats:
- 'Circular as a proof of Euclid: it assumes Mathlib''s `Nat.exists_infinite_primes`. It checks the interface, not
  number theory, and is not on the RakeSieve''s headline path.'
widgets:
- type: walkthrough
  title: The proof (SimpleGen.lean, lines 62-63)
  config:
    steps:
    - text: Start the brute-force generator at 2
      lean: SimpleGen.start
      link: SimpleGen.start
    - text: 'It is a PrimeGen: its next prime is the least prime above the current one, which exists by Mathlib''s
        Euclid'
      link: instPrimeGenSimpleGen
    - text: Apply the general fact about prime generators
      lean: exists_prime_gt_of_primeGen
      link: exists_prime_gt_of_primeGen
quiz:
- q: How does `SimpleGen` find the next prime?
  type: choice
  choices:
  - by trial division
  - as the least prime greater than p, via `Nat.find`
  - with the rake
  answer: 1
  explain: '`min_prime_gt n` uses `Nat.find (ex_prime_gt n)` (SimpleGen.lean lines 24–28).'
- q: Is this an independent proof that there are infinitely many primes?
  type: choice
  choices:
  - 'Yes'
  - 'No: building SimpleGen uses `Nat.exists_infinite_primes`'
  answer: 1
  explain: '`ex_prime_gt` calls `Nat.exists_infinite_primes` (SimpleGen.lean line 19).'
- q: Why is it kept at all?
  type: choice
  choices:
  - as a reference spec for PrimeGen, and as the control case that the no-Euclid check must flag
  - because the RakeSieve needs it
  - by accident
  answer: 0
  explain: NoEuclidCheck.lean ends with `#assert_uses_euclid simpleGen_exists_prime_gt`.
- q: What is SimpleGen's first prime?
  type: choice
  choices:
  - '1'
  - '2'
  - '3'
  answer: 1
  explain: '`SimpleGen.start := { p := ⟨2, Nat.prime_two⟩, … }` (SimpleGen.lean line 39).'
---
## Plain English

**Theorem (`simpleGen_exists_prime_gt`, SimpleGen.lean lines 62–63). CIRCULAR.** For every n there is a prime p > n.

Its statement is the same as the [corollary](#/node/results_exists_prime_gt_of_rakeSieve). The proof runs the general fact [exists_prime_gt_of_primeGen](#/node/exists_prime_gt_of_primeGen) on [SimpleGen.start](#/node/SimpleGen.start), the brute-force generator. Its next prime is `Nat.find` of "a prime greater than p" ([min_prime_gt](#/node/min_prime_gt)), and that prime exists only because Mathlib's `Nat.exists_infinite_primes` says so ([ex_prime_gt](#/node/ex_prime_gt), SimpleGen.lean line 19). So this is Euclid proved from Euclid.

PR #5 moved it out of Results.lean, where it was `results_exists_prime_gt_of_simpleGen`, into SimpleGen.lean, which the RakeSieve does not import. It stays for two reasons:

- **As a reference spec.** It shows that the obvious specification, "the next prime is the least prime above this one", satisfies the [PrimeGen](#/node/PrimeGen) interface. The RakeSieve can be compared against it, and the `#guard` on SimpleGen.lean line 57 checks its first ten primes by evaluation.
- **As the control for the no-Euclid check.** NoEuclidCheck.lean must *find* `Nat.exists_infinite_primes` in this theorem's dependencies. A broken checker that saw nothing would fail here instead of passing the RakeSieve headlines silently.
