---
id: instPrimeGenSimpleGen
title: SimpleGen is a prime generator
summary: 'Both obligations fall straight out of the MinPrimeGt fields: ''nothing smaller'' is `hmin`, ''bigger''
  is `hpgt`.'
review: draft
authors:
- grok-bot
caveats:
- An anonymous instance; the site's name for it is an approximation.
quiz:
- q: Which field gives 'no skipped prime'?
  type: choice
  choices:
  - '`hmin`'
  - '`hpgt`'
  answer: 0
  explain: SimpleGen.lean lines 44–48.
- q: Which field gives strict increase?
  type: choice
  choices:
  - '`hpgt`'
  - '`hmin`'
  answer: 0
  explain: SimpleGen.lean lines 49–51.
- q: Is this instance anonymous in the source?
  type: choice
  choices:
  - Yes; the site's name for it is approximate
  - 'No'
  answer: 0
  explain: '`instance : PrimeGen SimpleGen where`.'
---
## Plain English

`instance : PrimeGen SimpleGen` (SimpleGen.lean lines 41–53): `P g := g.p`, `next := SimpleGen.next`. `hP'`: a prime between p and the next would contradict `hmin`. `hP_lt`: `hpgt` says the next prime is above p. See [PrimeGen](#/node/PrimeGen), [SimpleGen](#/node/SimpleGen).
