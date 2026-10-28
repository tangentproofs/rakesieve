---
id: Rake.term
title: 'Rake.term: read the n-th term round-robin'
summary: Terms are not listed in increasing order in general; they cycle through the teeth. Only the first term
  is guaranteed to be the smallest, and that is all the sieve needs.
review: draft
authors:
- grok-bot
quiz:
- q: For {d = 6, ks = [5, 7]}, what is term 3?
  type: choice
  choices:
  - '13'
  - '11'
  - '17'
  answer: 0
  explain: 3 mod 2 = 1 → constant 7; 3 / 2 = 1 → 7 + 6 = 13.
- q: Are terms always increasing in n?
  type: choice
  choices:
  - No; for example if a constant exceeds d the order can saw-tooth
  - 'Yes'
  answer: 0
  explain: Rake.lean lines 180–184 say so.
- q: Which term is the minimum of a sorted rake?
  type: choice
  choices:
  - term 0
  - the last constant
  answer: 0
  explain: '`sorted_min_term_zero`.'
---
## Plain English

`r.term n = ks[n mod q] + d·(n / q)` where q = ks.length (Rake.lean lines 32–35). So term 0, 1, …, q−1 are the constants themselves, then each constant plus d, and so on.

[Rake.term_iff](#/node/Rake.term_iff) restates it: m is a term exactly when m = k + x·d for some k in ks and some x. For a sorted rake, term 0 is the smallest ([sorted_min_term_zero](#/node/Rake.sorted_min_term_zero)), which is how the RakeSieve picks its candidate.
