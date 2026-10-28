---
id: results_exists_prime_gt_of_simpleGen
title: Euclid via the brute-force generator
summary: '**The surprise:** the ''simple'' generator finds the next prime by asking Mathlib for the least prime
  above p, which already presupposes there is one. So this is Euclid proved from Euclid, a sanity check of the PrimeGen
  interface.'
review: draft
authors:
- grok-bot
caveats:
- Circular as a proof of Euclid; it checks the interface, not number theory.
widgets:
- type: walkthrough
  title: The proof (Results.lean, lines 15-17)
  config:
    steps:
    - text: Start the brute-force generator at 2
      lean: SimpleGen.start
      link: SimpleGen.start
    - text: 'It is a PrimeGen: its next prime is the least prime above the current one'
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
  explain: '`min_prime_gt n` uses `Nat.find (ex_prime_gt n)` (PrimeGen.lean lines 47–51).'
- q: Is this an independent proof that there are infinitely many primes?
  type: choice
  choices:
  - 'Yes'
  - 'No: building SimpleGen uses `Nat.exists_infinite_primes`'
  answer: 1
  explain: '`ex_prime_gt` calls `Nat.exists_infinite_primes` (PrimeGen.lean line 42).'
- q: What is SimpleGen's first prime?
  type: choice
  choices:
  - '1'
  - '2'
  - '3'
  answer: 1
  explain: '`SimpleGen.start := { p := ⟨2, Nat.prime_two⟩, … }` (PrimeGen.lean line 62).'
---
## Plain English

**Theorem (`results_exists_prime_gt_of_simpleGen`, Results.lean lines 15–17).** For every n there is a prime p > n.

Same statement as the [main theorem](#/node/results_exists_prime_gt_of_rakeSieve). The proof runs the general fact [exists_prime_gt_of_primeGen](#/node/exists_prime_gt_of_primeGen) on [SimpleGen.start](#/node/SimpleGen.start), the brute-force generator: its next prime is `Nat.find` of "a prime greater than p" ([min_prime_gt](#/node/min_prime_gt)), whose existence comes from Mathlib's `Nat.exists_infinite_primes` ([ex_prime_gt](#/node/ex_prime_gt), PrimeGen.lean line 42).

Its value is as a reference point: it shows the [PrimeGen](#/node/PrimeGen) interface is satisfiable by the obvious specification ("the least prime above p"), against which the RakeSieve can be compared.
