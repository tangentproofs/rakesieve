---
id: Rake.rem
title: 'Rake.rem: remove all multiples of j'
summary: '**The surprise:** removal never looks at a single number. It partitions by j and drops the sequences whose
  constant is a multiple of j: one test per sequence covers infinitely many numbers.'
review: draft
authors:
- grok-bot
quiz:
- q: After partitioning by j, why does j ∣ k decide a whole sequence?
  type: choice
  choices:
  - the step d·j is a multiple of j, so k + d·j·n ≡ k mod j
  - because k is prime
  answer: 0
  explain: So either every term or no term is a multiple of j.
- q: What happens if every constant is a multiple of j?
  type: choice
  choices:
  - it returns the placeholder rake `zer`
  - it fails to compile
  answer: 0
  explain: Rake.lean line 361.
- q: Why do the theorems assume `HasNonMultiple`?
  type: choice
  choices:
  - to rule out the `zer` case
  - for speed
  answer: 0
  explain: '`rem_def` (Rake.lean lines 370–409) shows the zer case cannot happen under that assumption.'
---
## Plain English

`r.rem hj` (Rake.lean lines 353–362, with r, j and hj from the section `variable` on line 350) partitions r by j ([Rake.partition](#/node/Rake.partition)) and keeps only the constants k with j ∤ k. If nothing is left it returns the dummy rake `zer`.

Three theorems pin down what it does, assuming the rake has at least one term not divisible by j ([HasNonMultiple](#/node/Rake.HasNonMultiple)):
- [rem_drop](#/node/Rake.rem_drop): no multiple of j is a term afterwards;
- [rem_keep](#/node/Rake.rem_keep): every non-multiple term of r is still a term;
- [rem_same](#/node/Rake.rem_same): no new terms appear.

A comment notes that a smarter version would use gcd(d, j), but in the sieve j is always a new prime, so it makes no difference.
