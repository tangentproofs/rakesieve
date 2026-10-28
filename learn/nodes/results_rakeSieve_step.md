---
id: results_rakeSieve_step
title: 'Headline: each step emits the next prime, none skipped'
summary: 'The sieve''s correctness used to be hidden inside an instance. Now it is a theorem anyone can cite: one
  step turns the candidate into the new prime, the candidate is prime and bigger than the old prime, and no prime
  was jumped over.'
review: draft
authors:
- grok-bot
widgets:
- type: walkthrough
  title: The proof (Results.lean, lines 27-31)
  config:
    steps:
    - text: 'The state''s hNext field: one step turns the candidate into the new prime'
      lean: (PrimeSieveState.hNext s (c_prime RakeSieve s) (no_skipped_prime RakeSieve s) rfl).1
      link: PrimeSieveState
    - text: The candidate is prime (it is the least element of R p)
      lean: c_prime RakeSieve s,
      link: c_prime
    - text: The candidate is bigger than p (everything in R p is)
      lean: c_gt_p RakeSieve s
      link: c_gt_p
    - text: No prime lies strictly between p and c
      lean: no_skipped_prime RakeSieve s⟩
      link: no_skipped_prime
quiz:
- q: After one step, what is the new prime?
  type: choice
  choices:
  - the old candidate c
  - p + 2
  - the least term of the old rake times 2
  answer: 0
  explain: 'First conjunct: `((nextState s).p : Nat) = s.c` (Results.lean line 28).'
- q: Which generic lemma rules out a prime strictly between p and c?
  type: choice
  choices:
  - '`no_skipped_prime`'
  - '`c_gt_p`'
  - '`Rake.term_add_len`'
  answer: 0
  explain: Such a prime would be in R p and below its least element c.
- q: Does this theorem need Mathlib's infinitude of primes?
  type: choice
  choices:
  - 'Yes'
  - 'No: NoEuclidCheck.lean checks its whole dependency closure'
  answer: 1
  explain: See the Trust page for the check output.
---
## Plain English

**R stands for *residue*.** R p is the set of numbers ≥ 2 that no prime ≤ p divides: what is left after crossing out the multiples of every prime up to p ([R](#/node/R)). For example, R 2 is the odd numbers from 3 up.

**Theorem (`results_rakeSieve_step`, Results.lean lines 27–31).** For every [RakeSieve](#/node/RakeSieve) state s, with prime p and candidate c:

1. one step ([nextState](#/node/nextState)) makes c the new prime;
2. c is prime;
3. p < c;
4. no prime q lies strictly between p and c.

Together these say the step moves from p to the very next prime. The proof only assembles results proved once for every sieve. Each state's candidate is the least element of R p, so by [c_prime](#/node/c_prime) it is prime, by [c_gt_p](#/node/c_gt_p) it is above p, and by [no_skipped_prime](#/node/no_skipped_prime) no prime lies in between. The state's `hNext` field ([PrimeSieveState](#/node/PrimeSieveState)) says the step makes c the new prime.

The same facts feed [the sieve driver instance](#/node/instPrimeGenPrimeSieve). This theorem states them directly for the RakeSieve, as the earlier review asked.
