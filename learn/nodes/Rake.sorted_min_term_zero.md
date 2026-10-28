---
id: Rake.sorted_min_term_zero
title: In a sorted rake, the first term is the smallest
summary: '**The surprise:** even though a rake''s terms can come out of order, this one fact survives every case,
  and it is the only ordering fact the sieve needs.'
review: draft
authors:
- grok-bot
quiz:
- q: Why is the first constant the smallest constant?
  type: choice
  choices:
  - the list is strictly increasing
  - it is 2
  answer: 0
  explain: That is the field `hsort`.
- q: Does the theorem need d > 0?
  type: choice
  choices:
  - 'No'
  - 'Yes'
  answer: 0
  explain: Adding d·x ≥ 0 never decreases.
- q: Where is it used in the sieve?
  type: choice
  choices:
  - to show the candidate is ≤ every survivor
  - to show it is prime
  answer: 0
  explain: RakeSieve.lean line 111.
---
## Plain English

**Theorem (`Rake.sorted_min_term_zero`, Rake.lean lines 185–196).** If the rake is sorted, r.term 0 ≤ r.term n for every n.

term 0 is the first constant plus 0; any other term is some constant (≥ the first, by sortedness) plus a multiple of d. [RakeMap.min_term_zero](#/node/RakeMap.min_term_zero) restates it for rake maps, and [RakeSieve.next](#/node/RakeSieve.next) uses it to prove the new candidate is the least survivor.
