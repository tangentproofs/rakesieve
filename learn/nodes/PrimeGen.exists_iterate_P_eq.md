---
id: PrimeGen.exists_iterate_P_eq
title: 'A prime generator skips nothing: every prime is reached'
summary: 'Two small properties add up to completeness: the primes go up, so some step passes q; nothing is skipped,
  so the step just before that lands exactly on q.'
review: draft
authors:
- grok-bot
widgets:
- type: walkthrough
  title: The proof (PrimeGen.lean, lines 79-97)
  config:
    steps:
    - text: 'Some step''s prime is above q: after q + 1 steps the prime has grown by at least q + 1'
      lean: ⟨q + 1, by have := PrimeGen.P_iterate_add_le g₀ (q + 1); omega⟩
      link: PrimeGen.P_iterate_add_le
    - text: Take the first such step k
      lean: set k := Nat.find hex with hkdef
    - text: k is a successor j + 1, since the start prime is ≤ q
      lean: 'obtain ⟨j, hj⟩ : ∃ j, k = j + 1 := Nat.exists_eq_succ_of_ne_zero hk0'
    - text: At step j the prime is ≤ q, because k was the first step above q
      lean: have := Nat.find_min hex (show j < k by omega)
    - text: If it were not q, q would be a prime strictly between steps j and j + 1, which hP' rules out
      lean: exact hP' (next^[j] g₀) ⟨q, hq, by omega, hk⟩
      link: PrimeGen
quiz:
- q: Which field of PrimeGen gives 'nothing skipped'?
  type: choice
  choices:
  - '`hP''`'
  - '`hP_lt`'
  answer: 0
  explain: Used on the last line, PrimeGen.lean line 97.
- q: Why can the first step above q not be step 0?
  type: choice
  choices:
  - the start prime is ≤ q by hypothesis
  - step 0 does not exist
  answer: 0
  explain: '`hle : (P g₀ : Nat) ≤ q`.'
- q: What does `Nat.find` pick here?
  type: choice
  choices:
  - the first step whose prime is above q
  - the largest prime below q
  answer: 0
  explain: '`set k := Nat.find hex` (PrimeGen.lean line 84).'
---
## Plain English

**Theorem (`PrimeGen.exists_iterate_P_eq`, PrimeGen.lean lines 79–97).** For any [prime generator](#/node/PrimeGen) started at g₀ and any prime q at or above the start prime, some number of steps k gives P (next^k g₀) = q.

The proof:

1. The primes go up by at least one per step ([PrimeGen.P_iterate_add_le](#/node/PrimeGen.P_iterate_add_le)), so after q + 1 steps the prime is above q. Let k be the *first* step where the prime is above q (`Nat.find`).
2. k is not 0, because the start prime is ≤ q. So k = j + 1, and at step j the prime is ≤ q (k was the first above).
3. If the prime at step j were not q, then q would lie strictly between the primes at steps j and j + 1, which `hP'` forbids.

It is generic and makes no use of Mathlib's infinitude of primes. [results_rakeSieve_emits_every_prime](#/node/results_rakeSieve_emits_every_prime) applies it to the RakeSieve, whose start prime is 2.
