---
id: RakeMap
title: 'RakeMap: a rake together with the property its terms have'
summary: The docstring calls it a '1-to-1 mapping', but the Lean only says the rake's terms are exactly the numbers
  with the property; one-to-one is never stated or needed.
review: draft
authors:
- grok-bot
caveats:
- The docstring's '1-to-1 mapping' and the field name `hbij` suggest a bijection; the field states only that the
  set of terms equals { n | pred n }. Nothing in the sieve needs injectivity.
quiz:
- q: What does `hbij` state?
  type: choice
  choices:
  - pred n holds iff n is some term of the rake
  - the term function is injective
  - pred is decidable
  answer: 0
  explain: RakeMap.lean line 8.
- q: Does the Lean state that the term function is one-to-one?
  type: choice
  choices:
  - 'No'
  - 'Yes'
  answer: 0
  explain: Despite the name `hbij` and the docstring, only the iff with pred is stated.
- q: Why require sortedness?
  type: choice
  choices:
  - so term 0 is the minimum
  - for printing
  answer: 0
  explain: '`min_term_zero`.'
---
## Plain English

A `RakeMap pred` (RakeMap.lean lines 6–9) is a [Rake](#/node/Rake) with two proofs:

- `hbij`: **pred n ↔ n is a term of the rake**, for every n;
- `hord`: the rake is sorted.

So the rake is an exact, sorted description of the set { n | pred n }. Operations: [RakeMap.rem](#/node/RakeMap.rem) removes multiples of j and updates pred to `pred n ∧ ¬ j ∣ n`; [min_term_zero](#/node/RakeMap.min_term_zero) says term 0 is the minimum; [RakeMap.pred](#/node/RakeMap.pred) reads the predicate back.
