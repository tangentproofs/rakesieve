---
id: Rake.term_add_len
title: 'Rake.term_add_len: one full turn adds the period'
summary: Reading a rake round-robin, the input m + len lands on the same sequence as m, one step further along.
  So every term t comes back as t + d, which is how the rake supplies its own survivor.
review: draft
authors:
- grok-bot
quiz:
- q: For the rake {d = 6, ks = [1, 5]}, term 0 = 1. What is term 2?
  type: choice
  choices:
  - '7'
  - '2'
  - '6'
  answer: 0
  explain: len = 2, so term (0 + 2) = term 0 + 6 = 7.
- q: Why does adding len keep the same sequence?
  type: choice
  choices:
  - (m + len) mod len = m mod len
  - because the rake is sorted
  answer: 0
  explain: '`Nat.add_mod_right` (Rake.lean line 51).'
- q: Where is it used?
  type: choice
  choices:
  - in RakeSieve.survivor, to find the term c + d
  - in Rake.sort
  answer: 0
  explain: '`rw [Rake.term_add_len, hm₀]` (RakeSieve.lean line 82).'
---
## Plain English

**Theorem (`Rake.term_add_len`, Rake.lean lines 50–53).** For a [rake](#/node/Rake) r with len = r.ks.length sequences and common step d, and any m:

term (m + len) = term m + d.

[Rake.term](#/node/Rake.term) reads sequence m mod len at position m / len. Adding len leaves m mod len unchanged and adds 1 to m / len, so the same sequence is read one step further, which adds d. The proof is exactly that: two facts about `%` and `/`, then unfolding `term`.

[RakeSieve.survivor](#/node/RakeSieve.survivor) uses it to show that c + d is a term of the rake whenever c is.
