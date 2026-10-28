---
id: Rake.rem_drop
title: After rem, no multiple of j remains
summary: 'The proof is pure divisibility: a surviving constant k has j ∤ k, and j divides d·j·x, so j cannot divide
  k + d·j·x.'
review: draft
authors:
- grok-bot
quiz:
- q: Which terms does it rule out?
  type: choice
  choices:
  - multiples of j
  - primes
  - terms below j
  answer: 0
  explain: '`∀n, j∣n → ¬(∃m, r''.term m = n)`.'
- q: Why is the HasNonMultiple hypothesis needed?
  type: choice
  choices:
  - otherwise rem returns `zer`, whose only term 0 is a multiple of j
  - it is not needed
  answer: 0
  explain: '`zer = {d := 0, ks := [0]}`.'
- q: Is it the 'drop' or 'keep' half?
  type: choice
  choices:
  - drop
  - keep
  answer: 0
  explain: 'As the name says: it drops the multiples.'
---
## Plain English

**Theorem (`Rake.rem_drop`, Rake.lean lines 411–431).** If r has a non-multiple of j, then no multiple of j is a term of r.rem. See [Rake.rem](#/node/Rake.rem).
