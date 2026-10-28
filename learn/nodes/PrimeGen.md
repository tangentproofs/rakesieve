---
id: PrimeGen
title: 'PrimeGen: what it means to generate primes in order'
summary: The spec of a prime generator is only two lines, 'no prime is skipped' and 'the prime goes up', and the
  second line was added only in September 2026 because the first alone allows a generator stuck on one prime.
review: draft
authors:
- grok-bot
quiz:
- q: Which two properties does `PrimeGen` require?
  type: choice
  choices:
  - output is prime; output is odd
  - no prime strictly between consecutive outputs; outputs strictly increase
  - the state is finite; next terminates
  answer: 1
  explain: '`hP''` and `hP_lt` (PrimeGen.lean lines 22 and 25). Primality of the output is built into the type `NPrime`.'
- q: Does `PrimeGen` say the generator starts at 2?
  type: choice
  choices:
  - 'Yes'
  - No, the start state is chosen separately
  answer: 1
  explain: There is no `init` field; the docstring says it was intentionally left out (PrimeGen.lean lines 15–17).
- q: A 'generator' with `next g = g` satisfies which condition?
  type: choice
  choices:
  - '`hP''` only'
  - '`hP_lt` only'
  - both
  - neither
  answer: 0
  explain: There is no prime strictly between p and p, so `hP'` holds, but `p < p` fails, so `hP_lt` does not.
---
## Plain English

A `PrimeGen` on a type α of states (PrimeGen.lean lines 18–25) provides:

- `P : α → NPrime`, the prime at the current state ([NPrime](#/node/NPrime));
- `next : α → α`, the step to the next state;
- `hP'`: for every state g, **no prime q satisfies P g < q < P (next g)**;
- `hP_lt`: for every state g, **P g < P (next g)**.

So, run from a state whose prime is p, a generator lists the primes from p upward, in order, with none skipped. The two conditions are independent: `hP'` alone allows `next g = g`, and `hP_lt` alone allows skipping.

The start state is deliberately not part of the class (the docstring explains: use `primes g₀ n` with an explicit start such as [SimpleGen.start](#/node/SimpleGen.start)). Consequently a `PrimeGen` does not promise to start at 2; that is a property of the particular start state.
