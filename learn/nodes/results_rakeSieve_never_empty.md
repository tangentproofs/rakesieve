---
id: results_rakeSieve_never_empty
title: 'Headline: the sieve never runs empty'
summary: 'The sieve supplies its own proof that it can always take another step: after the multiples of the candidate
  c are crossed out, the number c + d is still in the rake, where d is the rake''s period. No theorem about infinitely
  many primes is used.'
review: draft
authors:
- grok-bot
caveats:
- 'Euclid''s argument, carried by the data structure: c + d (d = p#) plays the part of p# + 1. This removes the
  circularity, not Euclid''s idea.'
- 'This site did not build the Lean. The claim that no infinitude theorem is used rests on NoEuclidCheck.lean as
  run for PR #5 (see the Trust page).'
widgets:
- type: walkthrough
  title: How RakeSieve.survivor proves it (RakeSieve.lean, lines 72-82)
  config:
    steps:
    - text: c is in R p, so it is a term of the rake, at some index m₀
      lean: obtain ⟨m₀, hm₀⟩ := (s.rm.hbij s.c).mp ((s.hprop s.c).mpr s.hCinR)
      link: RakeMap
    - text: Offer c + d as the survivor, at index m₀ + len (one period on)
      lean: refine ⟨s.c + s.rm.rake.d, m₀ + s.rm.rake.ks.length, ?_, ?_⟩
    - text: If c divided c + d, it would divide d
      lean: 'have hcd : s.c ∣ s.rm.rake.d := (Nat.dvd_add_iff_right (dvd_refl s.c)).mpr hdvd'
    - text: Then c ≤ p, by the invariant hdfac (every prime factor of d is ≤ p)
      lean: 'have hle : s.c ≤ s.p.val := s.hdfac s.c hC hcd'
      link: RakeSieve
    - text: But c > p, because c is in R p
      lean: 'have hgt : s.c > s.p.val := r_gt_p s.p.val s.c s.hCinR'
      link: r_gt_p
    - text: 'And c + d really is a term: one period past term m₀'
      lean: rw [Rake.term_add_len, hm₀]
      link: Rake.term_add_len
quiz:
- q: What does the sieve step need this theorem for?
  type: choice
  choices:
  - '`RakeMap.rem` needs proof that removing c''s multiples leaves something'
  - to prove c is prime
  - to sort the rake
  - nothing, it is decorative
  answer: 0
  explain: 'RakeMap.rem''s argument `hnmr: ∃n m, ¬j∣n ∧ rm.term m = n` (RakeMap.lean line 48). RakeSieve.next supplies
    it as `rs₀.survivor hC₀` (RakeSieve.lean line 98).'
- q: Which number is the witness that survives?
  type: choice
  choices:
  - a prime above c, from Mathlib
  - c + d, one period past c
  - c + 1
  - '2'
  answer: 1
  explain: '`refine ⟨s.c + s.rm.rake.d, m₀ + s.rm.rake.ks.length, ?_, ?_⟩` (RakeSieve.lean line 75).'
- q: Why can't c divide c + d?
  type: choice
  choices:
  - it would then divide d, but every prime factor of d is ≤ p < c
  - because c + d is prime
  - because d is odd
  answer: 0
  explain: If c ∣ c + d then c ∣ d; `hdfac` gives c ≤ p, and `r_gt_p` gives c > p (RakeSieve.lean lines 77–80).
- q: Is this a new mathematical proof that there are infinitely many primes?
  type: choice
  choices:
  - Yes, a completely new idea
  - 'No: c + d plays the part of Euclid''s p# + 1, but no infinitude theorem is imported'
  answer: 1
  explain: The idea is Euclid's. The circularity is gone, because the invariant `hdfac` is maintained by the sieve
    itself.
---
## Plain English

**R stands for *residue*.** R p is the set of numbers ≥ 2 that no prime ≤ p divides: what is left after crossing out the multiples of every prime up to p ([R](#/node/R)). For example, R 2 is the odd numbers from 3 up.

**Theorem (`results_rakeSieve_never_empty`, Results.lean lines 20–22).** For every [RakeSieve](#/node/RakeSieve) state s there are numbers n and m with s.c ∤ n and `s.rm.term m = n`. In words: some term of the state's rake is not a multiple of its candidate c.

**Why the sieve needs this.** A sieve step removes the multiples of c with [RakeMap.rem](#/node/RakeMap.rem), and `rem` will not run without a proof that something survives ([HasNonMultiple](#/node/Rake.HasNonMultiple)). This theorem is that proof, for every state. Until PR #5 the step got it by asking Mathlib for a prime above c (`Nat.exists_infinite_primes`). That made the infinitude corollary circular, since it used infinitude of primes to prove infinitude of primes.

**The witness is c + d.** The proof is [RakeSieve.survivor](#/node/RakeSieve.survivor):

1. c is a term of the rake, say term m₀, because c ∈ R p (`hCinR`) and the rake lists exactly R p (`hprop`, `hbij`).
2. One full turn of the rake later, term (m₀ + len) = c + d, where len is the number of sequences and d is their common step ([Rake.term_add_len](#/node/Rake.term_add_len)).
3. Every prime factor of d is ≤ p. This is the invariant `hdfac`, which every [RakeSieve](#/node/RakeSieve) state carries. c is a prime bigger than p ([r_gt_p](#/node/r_gt_p)), so c ∤ d, and therefore c ∤ c + d.

**This is still Euclid's idea.** In Euclid's proof, p# + 1 (one more than the product of the primes up to p) has no prime factor ≤ p. Here the period d plays the part of p#, and c + d is the survivor. What changed is where the argument lives. It is carried by the data structure, as an invariant that every step maintains, instead of being imported as a theorem. So infinitude of primes is now a consequence of the algorithm, not an input to it.

Lean states only that the prime factors of d are all ≤ p (`hdfac`). In fact d is exactly p# = 2·3·5·…·p: the start rake has period 2, and each step multiplies the period by the new prime ([RakeMap.rem_d](#/node/RakeMap.rem_d)). That equality is not stated as a theorem, and the proof does not need it.
