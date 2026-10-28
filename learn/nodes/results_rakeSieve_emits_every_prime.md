---
id: results_rakeSieve_emits_every_prime
title: 'Headline: started at 2, the sieve emits every prime'
summary: 'Not just ''the sieve produces primes'' but ''it produces all of them'': for every prime q, running the
  sieve from its start state reaches q after some number of steps.'
review: draft
authors:
- grok-bot
widgets:
- type: walkthrough
  title: The proof (Results.lean, lines 35-37)
  config:
    steps:
    - text: Run the sieve from its start state, prime 2
      lean: '({ state := RakeSieve.init } : PrimeSieve RakeSieve)'
      link: RakeSieve.init
    - text: Any prime generator emits every prime at or above its start; every prime is ≥ 2
      lean: PrimeGen.exists_iterate_P_eq _ q hq (Nat.Prime.two_le hq)
      link: PrimeGen.exists_iterate_P_eq
quiz:
- q: What does the theorem promise for q = 7?
  type: choice
  choices:
  - some number of steps after which the sieve's prime is 7
  - that 7 is the 7th prime
  - nothing; 7 is too small
  answer: 0
  explain: For every prime q there is k with P (next^[k] start) = q.
- q: Why does the proof need `Nat.Prime.two_le hq`?
  type: choice
  choices:
  - the generic lemma only covers primes at or above the start prime, which is 2
  - to show q is odd
  - it doesn't
  answer: 0
  explain: '`PrimeGen.exists_iterate_P_eq _ q hq (Nat.Prime.two_le hq)` (Results.lean line 37).'
- q: Which property of a prime generator makes 'every prime' work?
  type: choice
  choices:
  - '`hP''`: no prime is skipped between one step and the next'
  - only that the primes increase
  answer: 0
  explain: Increase alone could skip primes; `hP'` rules that out.
---
## Plain English

**Theorem (`results_rakeSieve_emits_every_prime`, Results.lean lines 35–37).** For every prime q there is a number of steps k such that the sieve, started at [RakeSieve.init](#/node/RakeSieve.init) and stepped k times, has current prime q.

With [the step theorem](#/node/results_rakeSieve_step) this says the sieve lists 2, 3, 5, 7, 11, …, every prime in order, with none missed and none repeated.

The proof is one line. The generic lemma [PrimeGen.exists_iterate_P_eq](#/node/PrimeGen.exists_iterate_P_eq) says that any prime generator emits every prime at or above its start prime. The sieve starts at 2, and every prime is ≥ 2. The generator here is [PrimeSieve](#/node/PrimeSieve) RakeSieve, a prime generator by [the sieve driver](#/node/instPrimeGenPrimeSieve).
