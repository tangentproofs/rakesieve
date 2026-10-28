---
id: main
title: 'main: print the first five primes from the RakeSieve'
summary: The verified sieve is also a runnable program; `#eval main` prints its first five primes when the file
  is compiled. That is a demo, not a proof.
review: draft
authors:
- grok-bot
quiz:
- q: Is `#eval main` a proof of anything?
  type: choice
  choices:
  - No, it prints output; nothing checks it
  - 'Yes'
  answer: 0
  explain: Unlike `#guard`, `#eval` does not fail on a wrong value.
- q: How many primes does it print?
  type: choice
  choices:
  - '5'
  - '10'
  answer: 0
  explain: '`for _ in [0:5]`.'
- q: Which generator does it run?
  type: choice
  choices:
  - PrimeSieve RakeSieve
  - SimpleGen
  answer: 0
  explain: Main.lean line 5.
---
## Plain English

`main` (Main.lean lines 4–10) starts a `PrimeSieve RakeSieve` at [RakeSieve.init](#/node/RakeSieve.init), steps it five times and prints the primes, which should be [2, 3, 5, 7, 11]. Main.lean line 12 runs it with `#eval`. Being the `lean_exe` root, it is built by `lake build`.

The output is not checked by any assertion, and this site did not run it (no Lean build). For a checked computation see the `#guard` on `primes SimpleGen.start 10` (PrimeGen.lean line 97), which is about the simple generator, not the RakeSieve.
