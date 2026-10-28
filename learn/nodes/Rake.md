---
id: Rake
title: 'Rake: several arithmetic sequences sharing one step'
summary: 'A rake is a picture of a residue system: the constants are the ''teeth'' and the shared step d is the
  spacing, so {3, 5} with d = 6 lists everything coprime to 6 that is ≥ 3.'
review: draft
authors:
- grok-bot
caveats:
- The README's growth figures and efficiency remarks are not formalized.
quiz:
- q: Which numbers does the rake {d = 6, ks = [5, 7]} produce?
  type: choice
  choices:
  - 5, 7, 11, 13, 17, 19, …
  - 5, 6, 7, 8, …
  - 6, 12, 18, …
  answer: 0
  explain: 5 + 6n and 7 + 6n.
- q: What does `hsize` guarantee?
  type: choice
  choices:
  - at least one constant
  - the rake is sorted
  - d > 0
  answer: 0
  explain: '`hsize : 0 < ks.length`.'
- q: Is the README's growth table (1, 2, 8, 48, …) proved in Lean?
  type: choice
  choices:
  - No, it is documentation
  - 'Yes'
  answer: 0
  explain: No theorem counts the constants after k steps.
---
## Plain English

A `Rake` (Rake.lean lines 15–22) has a step d and a non-empty list ks of constants. It stands for the union of the sequences k + d·n for k in ks. Its terms are listed round-robin by [Rake.term](#/node/Rake.term).

Fields `sorted`, `hsort`, `huniq` record whether ks is known to be strictly increasing and duplicate-free (a Bool flag with proofs), and `hsize` says ks is non-empty.

Examples: [Rake.ge2](#/node/Rake.ge2) = {d = 1, ks = [2]} is every number ≥ 2. After removing multiples of 2 and 3 the README shows the rake {5, 7} with step 6, and after 5 the rake with step 30 and eight constants 7, 11, 13, 17, 19, 23, 29, 31.

Why "rake": each sieve step multiplies the step d by the new prime p and the number of teeth by p − 1, which is why the README calls it laughably inefficient: 1, 2, 8, 48, 480, 5760, … sequences.
