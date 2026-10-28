---
id: Rake.rem_keep
title: After rem, every non-multiple survives
summary: 'This is the half that makes the sieve *complete*: nothing that should survive is lost, which is what keeps
  every prime in play.'
review: draft
authors:
- grok-bot
quiz:
- q: What does it preserve?
  type: choice
  choices:
  - every term not divisible by j
  - every term
  answer: 0
  explain: '`¬j∣n → (∃m, r.term m = n) → (∃m'', r''.term m'' = n)`.'
- q: Does it need HasNonMultiple?
  type: choice
  choices:
  - No (it builds one from n itself)
  - 'Yes'
  answer: 0
  explain: 'Rake.lean line 442: `have hnm: HasNonMultiple r j := by use n`.'
- q: Why is it important for the sieve?
  type: choice
  choices:
  - no prime is lost
  - it speeds things up
  answer: 0
  explain: Primes above the current one are never multiples of it.
---
## Plain English

**Theorem (`Rake.rem_keep`, Rake.lean lines 433–457).** If n is a term of r and j ∤ n, then n is a term of r.rem. It uses [partition_term_iff](#/node/Rake.partition_term_iff) to find n in the partitioned rake and checks that its constant passes the filter. See [Rake.rem](#/node/Rake.rem).
