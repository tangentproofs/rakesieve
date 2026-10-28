# Nodes for the generic sieve lemmas (PrimeSieve.lean), the RakeSieve itself (RakeSieve.lean)
# and the simple reference generator (SimpleGen.lean, circular; kept as a reference spec).
from _terms import PLAIN_R
NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}

node("r_gt_p", "Everything in R P is bigger than P",
 "This is why sieving works at all: a number ≤ P that is at least 2 has a prime factor ≤ P, so it cannot survive. Every survivor, including the next candidate, is beyond P.",
 PLAIN_R + r"""**Lemma (`r_gt_p`, PrimeSieve.lean lines 40–53).** For every r ∈ [R](#/node/R) p, r > p.

Proof: suppose r ≤ p. Since r ≥ 2, r has some prime factor f (Mathlib's `Nat.exists_prime_and_dvd`), and f ≤ r ≤ p. But membership in R p says no prime ≤ p divides r. Contradiction.

It gives [c_gt_p](#/node/c_gt_p) (the candidate is beyond the current prime) and is used in the RakeSieve's step to show the candidate grows.
""",
 [q("Why can't 4 be in R 5?", ["4 is even, and 2 ≤ 5 is a prime dividing it", "4 < 5 is not allowed by definition", "4 is in R 5"], 0, "R 5 requires that no prime ≤ 5 divide n; 2 divides 4. In general any 2 ≤ r ≤ p has a prime factor ≤ p."),
  q("Which Mathlib fact does the proof use?", ["every n ≠ 1 has a prime factor", "infinitely many primes", "unique factorization"], 0, "`Nat.exists_prime_and_dvd` (PrimeSieve.lean line 48)."),
  q("Does the lemma need p to be prime?", ["Yes", "No, it holds for every natural number p"], 1, "The statement is `∀ p : Nat, ∀ r ∈ R p, r > p`.")])

node("r_next", "Sieving by the next prime: R p₁ = R p₀ minus multiples of p₁",
 "This is the sieve of Eratosthenes as one equation. Crossing out the multiples of the next prime is exactly the move from 'no prime factor ≤ p₀' to 'no prime factor ≤ p₁', because no prime lies in between.",
 PLAIN_R + r"""**Theorem (`r_next`, PrimeSieve.lean lines 60–96).** Let p₁ be the least prime greater than p₀ (a [MinPrimeGt](#/node/MinPrimeGt) p₀). Then for every n:

n ∈ [R](#/node/R) p₀ and p₁ ∤ n **if and only if** n ∈ R p₁.

Left to right is the interesting part: a prime q ≤ p₁ dividing n is either ≤ p₀ (excluded by n ∈ R p₀), equal to p₁ (excluded by p₁ ∤ n), or strictly between p₀ and p₁, which cannot happen because p₁ is the *least* prime above p₀. (The Lean argues through a prime factor f of q, which makes the case split work for any q.)

Its companion [r_next_prop](#/node/r_next_prop) restates it for predicates, which is how the RakeSieve uses it.
""",
 [q("Why must p₁ be the *least* prime above p₀?", ["otherwise a prime between them would not be sieved out", "for speed", "it need not be"], 0,
    "If a prime q with p₀ < q < p₁ existed, R p₀ minus multiples of p₁ would still contain q, but q ∉ R p₁."),
  q("Which numbers are in R 3 but not R 5?", ["multiples of 5 that have no factor 2 or 3, like 5, 25, 35", "all multiples of 5", "primes"], 0, "R 5 = R 3 minus multiples of 5 (5 is the least prime above 3)."),
  q("Where is this used?", ["in the RakeSieve step, via `r_next_prop`", "nowhere", "in SimpleGen"], 0, "RakeSieve.lean line 110.")])

node("r_next_prop", "r_next for predicates: how a sieve tracks R step by step",
 "The RakeSieve never computes the residue R (what survives sieving) directly. It carries a predicate, adds '∧ not a multiple of c' at each step, and this lemma certifies that the predicate still means exactly R.",
 PLAIN_R + r"""**Theorem (`r_next_prop`, PrimeSieve.lean lines 110–114).** Suppose h₀ n ↔ n ∈ [R](#/node/R) p₀, and h₁ n ↔ h₀ n ∧ ¬ (m.p ∣ n), where m.p is the least prime above p₀. Then h₁ n ↔ n ∈ R m.p.

It is [r_next](#/node/r_next) with names for the two predicates. The comment above it (PrimeSieve.lean lines 98–109) explains the design: a sieve models R p by a bijection with its data structure, and whatever it does to sift out the next prime corresponds to adding `∧ ¬(p₁∣n)` to the predicate. The RakeSieve uses it once per step (RakeSieve.lean line 110).
""",
 [q("What is h₁ in the RakeSieve step?", ["the predicate of the rake after removing multiples of the new prime", "the list of primes", "the candidate"], 0, "`h₁ := rs.pred`, with `rs = rs₀.rm.rem c'.p …` (RakeSieve.lean lines 101–108)."),
  q("What does the lemma conclude?", ["h₁ describes R of the new prime", "h₁ is decidable", "h₀ = h₁"], 0, "`h₁ n ↔ n ∈ R m.p`."),
  q("Which lemma does it rest on?", ["`r_next`", "`c_prime`", "`r_gt_p`"], 0, "The proof is `simp[hh₁, hh₀]; exact r_next p₀ m`.")])

node("c_gt_p", "The candidate is beyond the current prime",
 "A one-line consequence, but it is the whole reason the generated primes strictly increase, the property that turned out to be needed for infinitude.",
 PLAIN_R + r"""**Theorem (`c_gt_p`, PrimeSieve.lean lines 129–131).** For any driven sieve state g, C g > P g.

Because C g ∈ [R](#/node/R) (P g) (the driver's `hCinR`) and everything in R P exceeds P ([r_gt_p](#/node/r_gt_p)). The [driver instance](#/node/instPrimeGenPrimeSieve) uses it for `hP_lt`.
""",
 [q("Which driver field does it use?", ["`hCinR`", "`hRmin`"], 0, "C ∈ R P, then `r_gt_p`."),
  q("Which `PrimeGen` field does it supply?", ["`hP'`", "`hP_lt`"], 1, "Strict increase."),
  q("Does it need C to be the *least* survivor?", ["Yes", "No, only that C survives"], 1, "Any survivor exceeds P.")])

node("no_skipped_prime", "No prime lies between P and the candidate",
 "The proof is three lines of idea: a prime above P has no small prime factor, so it survives the sieve, so it is at least the least survivor C.",
 PLAIN_R + r"""**Theorem (`no_skipped_prime`, PrimeSieve.lean lines 133–151).** For any driven sieve state g there is no prime q with P g < q < C g.

Proof: such a q is ≥ 2, and any prime p ≤ P dividing q would equal q (both prime), but q > P. So q ∈ [R](#/node/R) (P g). The driver's `hRmin` then gives C g ≤ q, contradicting q < C g.

This is the proof of [nosk'](#/node/nosk') that a sieve step needs, and gives `hP'` in the [driver instance](#/node/instPrimeGenPrimeSieve).
""",
 [q("Why is a prime q > P in R P?", ["its only prime factor is q itself, which is > P", "because q is odd", "by definition of prime"], 0, "`Nat.prime_dvd_prime_iff_eq` turns p ∣ q into p = q."),
  q("Which driver field closes the argument?", ["`hCinR`", "`hRmin`"], 1, "C is ≤ everything in R P."),
  q("Is this the same as `nosk' (P g) (C g)`?", ["Yes", "No"], 0, "The statement is `¬ ∃ q, Nat.Prime q ∧ P g < q ∧ q < C g`.")])

node("no_prime_factors_im_no_factors", "No prime factor below c means c is prime",
 "The library proves this small classical fact by hand rather than finding it in Mathlib: a number ≥ 2 with no prime factor below it has no factor at all but 1 and itself.",
 r"""
## Plain English

**Lemma (`no_prime_factors_im_no_factors`, PrimeSieve.lean lines 153–170).** If c ≥ 2 and no prime p < c divides c, then c is prime.

Proof: a divisor m < c with m ≠ 1 would have a prime factor p, which divides c and is ≤ m < c, contradiction. So the only divisors below c are 1, which is Mathlib's `Nat.prime_def_lt`.

Used by [c_prime](#/node/c_prime).
""",
 [q("Is the hypothesis 'no prime p < c divides c' enough without c ≥ 2?", ["Yes", "No: c = 1 has no prime factors and is not prime"], 1, "Hence `h2lc : 2 ≤ c`."),
  q("Which characterization of primes closes the proof?", ["`Nat.prime_def_lt`", "Wilson's theorem", "`Nat.Prime.two_le`"], 0, "PrimeSieve.lean line 170."),
  q("Does 25 satisfy the hypothesis?", ["Yes", "No: 5 < 25 is prime and divides 25"], 1, "So the lemma says nothing about 25.")])

node("c_prime", "The candidate is prime",
 "No sieve ever tests the candidate for primality. Its primality is a theorem: a prime factor would be either ≤ P (sieved out) or between P and C (impossible).",
 PLAIN_R + r"""**Theorem (`c_prime`, PrimeSieve.lean lines 173–193).** For any driven sieve state g, C g is prime.

Proof by [no_prime_factors_im_no_factors](#/node/no_prime_factors_im_no_factors): C ≥ 2 because C > P ≥ 2 ([c_gt_p](#/node/c_gt_p)). A prime q < C dividing C would be ≤ P, impossible since C ∈ [R](#/node/R) P, or > P, impossible by [no_skipped_prime](#/node/no_skipped_prime).

It supplies the `hC` argument of every sieve step ([nextState](#/node/nextState)).
""",
 [q("Does any sieve in this library run a primality test on C?", ["Yes", "No, C's primality is proved from the driver facts"], 1, "`c_prime` is a theorem about every driven state."),
  q("Which two lemmas cover the two cases of a prime factor q?", ["`hCinR` (q ≤ P) and `no_skipped_prime` (q > P)", "`r_next` and `r_gt_p`"], 0, "PrimeSieve.lean lines 180–187."),
  q("Why is C ≥ 2?", ["C > P and P is prime, so P ≥ 2", "by definition"], 0, "PrimeSieve.lean lines 188–192.")])

node("nextState", "nextState: one sieve step, with the proofs filled in",
 "The step a user calls takes no proofs, because the library proves the step's preconditions itself, for every driven sieve, every time.",
 r"""
## Plain English

`nextState s` (PrimeSieve.lean lines 205–208) is `PrimeSieveState.next s (c_prime …) (no_skipped_prime …)`: it runs the sieve's own step, passing in the two proofs that step demands, [c_prime](#/node/c_prime) and [no_skipped_prime](#/node/no_skipped_prime). [PrimeSieve.next](#/node/PrimeSieve.next) applies it to the wrapped state.
""",
 [q("Which two proofs does `nextState` pass to the sieve's `next`?", ["`c_prime` and `no_skipped_prime`", "`r_gt_p` and `r_next`"], 0, "PrimeSieve.lean lines 206–208."),
  q("Does a caller of `nextState` need to prove anything?", ["Yes", "No"], 1, "The proofs come from the driver."),
  q("For the RakeSieve, which function does `nextState` end up calling?", ["`RakeSieve.next`", "`SimpleGen.next`"], 0, "The RakeSieve's `PrimeSieveState` instance sets `next := .next` (RakeSieve.lean line 141).")])

node("PrimeSieve.next", "PrimeSieve.next: step the wrapped sieve",
 "It is nothing more than `nextState` applied inside the wrapper; all the mathematics is in the proofs it carries along.",
 r"""
## Plain English

`PrimeSieve.next x = { state := nextState x.state }` (PrimeSieve.lean lines 214–215). It is the `next` of the [driver instance](#/node/instPrimeGenPrimeSieve). See [nextState](#/node/nextState).
""",
 [q("What does `PrimeSieve.next` change?", ["only the wrapped state, by one sieve step", "the type α"], 0, "PrimeSieve.lean line 215."),
  q("Which `PrimeGen` field is it?", ["`P`", "`next`"], 1, "PrimeSieve.lean line 220."),
  q("Does it need proofs from the caller?", ["No", "Yes"], 0, "`nextState` supplies them.")])

node("RakeSieve", "RakeSieve: a sieve state that carries its own correctness proof",
 "Each state is data plus four proofs: its rake lists exactly the residue R p (the survivors of sieving up to p), its candidate is the least element of R p, and the rake's period has no prime factor above p. That last proof keeps the sieve from ever running empty.",
 PLAIN_R + r"""A `RakeSieve` (RakeSieve.lean lines 5–15) has:

- `prop : Nat → Prop` and `rm : RakeMap prop`: a [RakeMap](#/node/RakeMap), i.e. a rake (a sorted list of arithmetic sequences with a common step) whose terms are exactly the numbers satisfying `prop`;
- `p : NPrime`, the current prime, and `c : Nat`, the candidate;
- `hprop`: **prop n ↔ n ∈ [R](#/node/R) p**, so the rake's terms are exactly the survivors of sieving up to p;
- `hCinR`: c ∈ R p; `hRmin`: c ≤ r for every r ∈ R p;
- `hdfac` (RakeSieve.lean line 15): **every prime factor of the rake's period d is ≤ p**. The period is the common step of the rake's sequences. It starts at 2 and is multiplied by each new prime, so it is in fact p# = 2·3·5·…·p, though Lean only states the factor bound.

So c is the least survivor, and by the generic lemmas it is the next prime. `hdfac` is what lets the sieve prove it never runs empty: c is a prime above p, so it does not divide d, and so the term c + d survives when c's multiples are removed ([RakeSieve.survivor](#/node/RakeSieve.survivor)). In the actual sieve, c is the rake's first term (RakeSieve.lean line 102).

The commented-out field `Q : Array RakeMap` is the planned queue of primes below p² (issue #2, open pull request #4), not in this version.
""",
 [q("What does `hprop` say?", ["the rake's predicate holds exactly on R p", "p is prime", "the rake is sorted"], 0, "`hprop : ∀ n:Nat, prop n ↔ n ∈ R p` (RakeSieve.lean line 10)."),
  q("Can you build a `RakeSieve` whose candidate is not the least element of R p?", ["Yes", "No, `hRmin` must be proved"], 1, "Every value of the structure includes the proof `hRmin`."),
  q("Where does the candidate come from in `RakeSieve.next`?", ["the rake's first term", "`Nat.find`", "a primality test"], 0, "`let c₁ := rs.rake.term 0` (RakeSieve.lean line 102)."),
  q("What does `hdfac` say?", ["every prime factor of the rake's period is ≤ p", "the rake has at most p sequences", "c divides the period"], 0, "`hdfac : ∀ q, Nat.Prime q → q ∣ rm.rake.d → q ≤ p.val` (RakeSieve.lean line 15)."),
  q("Is `hdfac` an assumption that smuggles in infinitude of primes?", ["No: like `hCinR`, it is a field proved at `init` and re-proved by every step", "Yes"], 0, "RakeSieve.lean lines 57–62 prove it for `init` and lines 126–136 for `next`.")],
 caveats=["The queue of primes below p² described in the README and issue #2 is on the unmerged branch `feature/rakesieve-queue-below-psq` (PR #4), not in main."])

node("RakeSieve.init", "RakeSieve.init: prime 2, odd numbers ≥ 3, candidate 3",
 "The starting rake is built by the same operation as every later step: begin with 2 + n (all numbers ≥ 2) and remove the multiples of 2, leaving the single sequence 3 + 2n.",
 PLAIN_R + r"""`RakeSieve.init` (RakeSieve.lean lines 22–62) is the start state:

- the rake map is [rm_ge2](#/node/RakeMap.rm_ge2) (the rake {2 + n}, i.e. every number ≥ 2) with the multiples of 2 removed by [RakeMap.rem](#/node/RakeMap.rem); its predicate is n ≥ 2 ∧ ¬ 2 ∣ n;
- p = 2, c = 3;
- `hprop`: n ≥ 2 ∧ ¬ 2 ∣ n ↔ n ∈ [R](#/node/R) 2 (proved inline, RakeSieve.lean lines 27–50);
- `hCinR` and `hRmin`: the two headline facts [3 ∈ R 2](#/node/results_three_mem_R_two) and [nothing in R 2 is below 3](#/node/results_three_le_of_mem_R_two);
- `hdfac`: the start rake's period is 1 · 2 = 2 ([RakeMap.rem_d](#/node/RakeMap.rem_d)), and its only prime factor, 2, is ≤ p (RakeSieve.lean lines 57–62).

To call `rem`, the code must show some term of {2 + n} is odd; it uses 3 = 2 + 1 (RakeSieve.lean line 24).
""",
 [q("What is the rake after `init`?", ["2 + n", "3 + 2n (the odd numbers ≥ 3)", "1 + 2n"], 1, "Removing multiples of 2 from 2 + n leaves 3 + 2n; the README walks through this."),
  q("Which two Results.lean facts does `init` use?", ["3 ∈ R 2 and 3 ≤ everything in R 2", "Euclid's theorem twice"], 0, "RakeSieve.lean lines 51–56."),
  q("What witness shows `rem 2` leaves something?", ["3, the term at m = 1", "2", "Mathlib's infinitude of primes"], 0, "`use 3; use 1` (RakeSieve.lean line 24). Later steps use the survivor c + d instead.")])

node("RakeSieve.next", "RakeSieve.next: remove the multiples of c, take the first term",
 "To cross out c's multiples, the step must first prove that something will survive, and the rake supplies the survivor itself: the term c + d, one period past c. No theorem about infinitely many primes is used.",
 PLAIN_R + r"""`RakeSieve.next rs₀ hC₀ hNS` (RakeSieve.lean lines 84–136) takes a state, a proof that its candidate c is prime, and a proof that no prime lies between p and c ([nosk'](#/node/nosk')). It returns the state with prime c:

1. Package c as the least prime above p (a [MinPrimeGt](#/node/MinPrimeGt)), using [r_gt_p](#/node/r_gt_p) for c > p.
2. Prove that removing c's multiples leaves at least one term: [RakeSieve.survivor](#/node/RakeSieve.survivor) gives the term c + d, which c does not divide (RakeSieve.lean line 98).
3. Remove the multiples of c with [RakeMap.rem](#/node/RakeMap.rem) (RakeSieve.lean line 101).
4. The new candidate c₁ is the new rake's first term (RakeSieve.lean line 102).
5. The new predicate means R c, by [r_next_prop](#/node/r_next_prop) (RakeSieve.lean line 110); c₁ is in it, and is ≤ every term because the rake is sorted ([RakeMap.min_term_zero](#/node/RakeMap.min_term_zero), RakeSieve.lean line 125).

6. Re-prove the invariant `hdfac` for the new state. The new period is d · c ([RakeMap.rem_d](#/node/RakeMap.rem_d)), so its prime factors are those of d, all ≤ p < c, together with c itself (RakeSieve.lean lines 126–136).

Step 2 used to ask Mathlib for a prime above c (`Nat.exists_infinite_primes`). That made the sieve's infinitude corollary circular. The survivor c + d is the same idea as Euclid's p# + 1, but it is now built from the rake's own data.
""",
 [q("Why does the step need a non-multiple of c among the rake's terms?", ["`rem` requires a proof it won't remove everything", "for speed", "to sort the rake"], 0,
    "RakeMap.rem's argument `hnmr: ∃n m, ¬j∣n ∧ rm.term m = n` (RakeMap.lean line 48)."),
  q("Where does that non-multiple come from?", ["the rake's own term c + d, via `RakeSieve.survivor`", "a prime q > c from `Nat.exists_infinite_primes`", "`decide`"], 0, "`have hsurv … := rs₀.survivor hC₀` (RakeSieve.lean line 98)."),
  q("Why is the first term the least survivor?", ["the rake is sorted, so term 0 is its minimum", "by luck", "it is proved by `decide`"], 0, "`rs.min_term_zero k` (RakeSieve.lean line 125)."),
  q("What is the new prime of the returned state?", ["the old candidate c", "the old prime + 2"], 0, "`p := ⟨c'.p, hC₀⟩` where `c'.p = rs₀.c` (RakeSieve.lean line 111).")],
 caveats=["No infinitude theorem is used. The survivor is Euclid's idea (c + p# for p# + 1), carried by the invariant `hdfac`."])

node("RakeSieve.survivor", "RakeSieve.survivor: the rake proves it never runs empty",
 "The sieve finds its own survivor without asking anyone for a bigger prime. The candidate c sits somewhere in the rake, one full turn later the rake produces c + d, and c cannot divide c + d.",
 PLAIN_R + r"""**Theorem (`RakeSieve.survivor`, RakeSieve.lean lines 72–82).** For every [RakeSieve](#/node/RakeSieve) state s whose candidate c is prime, some term of the rake is not a multiple of c. Exported as [results_rakeSieve_never_empty](#/node/results_rakeSieve_never_empty), which has the proof outline. [RakeSieve.next](#/node/RakeSieve.next) uses it to call [RakeMap.rem](#/node/RakeMap.rem).

The witness is c + d, where d is the rake's period (the common step of its sequences):

- c is in R p, so it is a term of the rake, say term m₀;
- [Rake.term_add_len](#/node/Rake.term_add_len): term (m₀ + len) = c + d;
- if c divided c + d, it would divide d, so c ≤ p by the invariant `hdfac`. But c > p ([r_gt_p](#/node/r_gt_p)).

The docstring (RakeSieve.lean lines 64–71) says plainly that this is Euclid's argument, with c + p# in the part of p# + 1. The difference is that it is carried by the data structure, and no infinitude theorem is imported.
""",
 [q("Why is c + d a term of the rake?", ["one period past term m₀ = c, by `Rake.term_add_len`", "because c + d is prime", "by `decide`"], 0, "`rw [Rake.term_add_len, hm₀]` (RakeSieve.lean line 82)."),
  q("Which invariant rules out c ∣ d?", ["`hdfac`: every prime factor of d is ≤ p", "`hRmin`", "`hprop`"], 0, "`s.hdfac s.c hC hcd` (RakeSieve.lean line 78)."),
  q("Does it need c to be prime?", ["Yes: `hdfac` speaks about prime factors, so it is applied to c as a prime", "No"], 0, "The hypothesis `hC : Nat.Prime s.c`.")],
 caveats=["Euclid's argument in the sieve's own terms. It removes the circularity, not Euclid's idea."])

node("RakeSieve.instPrimeSieveStateRakeSieve", "The RakeSieve is a sieve state",
 "The proof that the candidate grows reuses the generic r_gt_p: the new candidate is in the residue R (the survivors of sieving) of the new prime, so it exceeds the new prime, which is the old candidate.",
 PLAIN_R + r"""`instance : PrimeSieveState RakeSieve` (RakeSieve.lean lines 138–151): P is the state's prime p, C its candidate c, the step is [RakeSieve.next](#/node/RakeSieve.next). The `hNext` proof shows the new p is the old c (by unfolding `next`) and the new c exceeds the old c (the new c is in R (new p), so [r_gt_p](#/node/r_gt_p) applies).
""",
 [q("What is `C` for a RakeSieve state?", ["its field `c`", "its rake's last term"], 0, "`C x := x.c` (RakeSieve.lean line 140)."),
  q("Why is the new candidate bigger than the old one?", ["it lies in R (new p), so it exceeds new p = old c", "the rake grows"], 0, "RakeSieve.lean lines 148–151."),
  q("Which step function does it use?", ["`RakeSieve.next`", "`PrimeSieve.next`"], 0, "`next := .next` (RakeSieve.lean line 141).")],
 caveats=["An anonymous instance; this site names it `RakeSieve.instPrimeSieveStateRakeSieve`, which may differ from the name Lean generates."])

node("RakeSieve.instPrimeSieveDriverRakeSieve", "The RakeSieve satisfies the driver",
 "There is nothing to prove here. Every RakeSieve state already carries `hCinR` and `hRmin` as fields, so the driver instance just reads them off.",
 r"""
## Plain English

`instance : PrimeSieveDriver RakeSieve` (RakeSieve.lean lines 155–157) sets `hCinR x := x.hCinR` and `hRmin x := x.hRmin`, after unfolding C and P. The work was done when each state was built: in [RakeSieve.init](#/node/RakeSieve.init) and in [RakeSieve.next](#/node/RakeSieve.next). See [PrimeSieveDriver](#/node/PrimeSieveDriver).
""",
 [q("Where are the driver facts proved for the RakeSieve?", ["inside `init` and `next`, when each state is built", "in this instance", "nowhere"], 0, "The structure's fields are proofs."),
  q("How long is the instance?", ["three lines", "a hundred lines"], 0, "RakeSieve.lean lines 155–157."),
  q("Which two fields does it supply?", ["`hCinR` and `hRmin`", "`hP'` and `hP_lt`"], 0, "Those are the fields of `PrimeSieveDriver`.")],
 caveats=["An anonymous instance; the site's name for it is an approximation."])

node("exists_prime_gt_of_primeGen", "A generator whose primes strictly increase passes every n",
 "It needs no number theory at all, just counting: the prime goes up by at least one per step and starts at 2 or more, so after n + 1 steps it exceeds n.",
 r"""
## Plain English

**Theorem (`exists_prime_gt_of_primeGen`, PrimeGen.lean lines 68–74).** For any [PrimeGen](#/node/PrimeGen) α, any state g₀ and any n, some prime p satisfies n < p.

The witness is the generator's prime after n + 1 steps. By [PrimeGen.P_iterate_add_le](#/node/PrimeGen.P_iterate_add_le) it is at least P g₀ + n + 1 ≥ n + 3. It is prime because generator values are [NPrime](#/node/NPrime)s. This is what [results_exists_prime_gt_of_primeGen](#/node/results_exists_prime_gt_of_primeGen) exports.
""",
 [q("Which witness does the proof offer?", ["the prime after n + 1 steps", "n + 1", "the least prime above n"], 0, "`P (next^[k] g₀)` with k = n + 1."),
  q("Is it ever tight, i.e. is the witness the *least* prime above n?", ["not necessarily; the proof only needs some prime above n", "always"], 0, "The witness can be far above n."),
  q("Which field of PrimeGen is used?", ["`hP_lt`", "`hP'`"], 0, "Via `P_iterate_add_le`.")])

node("PrimeGen.exists_iterate_P_eq", "A prime generator skips nothing: every prime is reached",
 "Two small properties add up to completeness: the primes go up, so some step passes q; nothing is skipped, so the step just before that lands exactly on q.",
 r"""
## Plain English

**Theorem (`PrimeGen.exists_iterate_P_eq`, PrimeGen.lean lines 79–97).** For any [prime generator](#/node/PrimeGen) started at g₀ and any prime q at or above the start prime, some number of steps k gives P (next^k g₀) = q.

The proof:

1. The primes go up by at least one per step ([PrimeGen.P_iterate_add_le](#/node/PrimeGen.P_iterate_add_le)), so after q + 1 steps the prime is above q. Let k be the *first* step where the prime is above q (`Nat.find`).
2. k is not 0, because the start prime is ≤ q. So k = j + 1, and at step j the prime is ≤ q (k was the first above).
3. If the prime at step j were not q, then q would lie strictly between the primes at steps j and j + 1, which `hP'` forbids.

It is generic and makes no use of Mathlib's infinitude of primes. [results_rakeSieve_emits_every_prime](#/node/results_rakeSieve_emits_every_prime) applies it to the RakeSieve, whose start prime is 2.
""",
 [q("Which field of PrimeGen gives 'nothing skipped'?", ["`hP'`", "`hP_lt`"], 0, "Used on the last line, PrimeGen.lean line 97."),
  q("Why can the first step above q not be step 0?", ["the start prime is ≤ q by hypothesis", "step 0 does not exist"], 0, "`hle : (P g₀ : Nat) ≤ q`."),
  q("What does `Nat.find` pick here?", ["the first step whose prime is above q", "the largest prime below q"], 0, "`set k := Nat.find hex` (PrimeGen.lean line 84).")],
 widgets=[{"type": "walkthrough", "title": "The proof (PrimeGen.lean, lines 79-97)", "config": {"steps": [
   {"text": "Some step's prime is above q: after q + 1 steps the prime has grown by at least q + 1", "lean": "⟨q + 1, by have := PrimeGen.P_iterate_add_le g₀ (q + 1); omega⟩", "link": "PrimeGen.P_iterate_add_le"},
   {"text": "Take the first such step k", "lean": "set k := Nat.find hex with hkdef"},
   {"text": "k is a successor j + 1, since the start prime is ≤ q", "lean": "obtain ⟨j, hj⟩ : ∃ j, k = j + 1 := Nat.exists_eq_succ_of_ne_zero hk0"},
   {"text": "At step j the prime is ≤ q, because k was the first step above q", "lean": "have := Nat.find_min hex (show j < k by omega)"},
   {"text": "If it were not q, q would be a prime strictly between steps j and j + 1, which hP' rules out", "lean": "exact hP' (next^[j] g₀) ⟨q, hq, by omega, hk⟩", "link": "PrimeGen"}]}}])

node("PrimeGen.P_iterate_add_le", "After k steps the prime has grown by at least k",
 "Strict increase on natural numbers is already a growth guarantee: each step adds at least 1, so k steps add at least k.",
 r"""
## Plain English

**Theorem (`PrimeGen.P_iterate_add_le`, PrimeGen.lean lines 56–64).** For any state g and k, P g + k ≤ P (next^[k] g), where next^[k] is next applied k times.

Induction on k, using `hP_lt` at each step. Used by [exists_prime_gt_of_primeGen](#/node/exists_prime_gt_of_primeGen).
""",
 [q("What does `next^[k] g` mean?", ["next applied k times to g", "the k-th power of next's value"], 0, "Mathlib's function iteration notation."),
  q("What proof technique?", ["induction on k", "contradiction", "`decide`"], 0, "PrimeGen.lean lines 58–64."),
  q("Does it need `hP'`?", ["No", "Yes"], 0, "Only strict increase.")])

node("MinPrimeGt", "MinPrimeGt n: the least prime above n, with proof",
 "'The next prime' is a structure, not a number: the number, a proof it is a prime above n, and a proof nothing smaller is.",
 r"""
## Plain English

A `MinPrimeGt n` (PrimeGen.lean lines 30–33) has a number p, a proof `hpgt` that p is prime and n < p ([PrimeGt](#/node/PrimeGt)), and a proof `hmin` that no q < p is a prime above n. So p is *the* next prime after n. [min_prime_gt](#/node/min_prime_gt) builds one with `Nat.find`; [RakeSieve.next](#/node/RakeSieve.next) builds one from the sieve's candidate.
""",
 [q("What does `hmin` say?", ["no q < p is a prime greater than n", "p is minimal among all primes"], 0, "`∀q:Nat, q < p → (¬ PrimeGt n q)`."),
  q("Is MinPrimeGt 7 unique?", ["its number p must be 11", "p could be 11 or 13"], 0, "11 is the least prime above 7, and `hmin` rules out anything else."),
  q("Which lemma about R needs a MinPrimeGt?", ["`r_next`", "`r_gt_p`"], 0, "Sieving by the *next* prime.")])

node("PrimeGt", "PrimeGt n p: p is a prime above n",
 "It is a two-word abbreviation that the whole library leans on: 'prime and bigger than n'.",
 r"""
## Plain English

`PrimeGt n p := Nat.Prime p ∧ n < p` (PrimeGen.lean line 28). Used in [MinPrimeGt](#/node/MinPrimeGt) and [ex_prime_gt](#/node/ex_prime_gt).
""",
 [q("Is `PrimeGt 5 7` true?", ["Yes", "No"], 0, "7 is prime and 5 < 7."),
  q("Is `PrimeGt 5 5` true?", ["Yes", "No"], 1, "5 < 5 is false."),
  q("Is `PrimeGt 5 9` true?", ["Yes", "No"], 1, "9 is not prime.")])

node("ex_prime_gt", "There is a prime above c (from Mathlib)",
 "This is where the reference generator borrows Euclid outright, with a direct call to Mathlib's `Nat.exists_infinite_primes`. That is why it lives in SimpleGen.lean, off the RakeSieve's path.",
 r"""
## Plain English

**Theorem (`ex_prime_gt`, SimpleGen.lean lines 16–22).** For every c there is p with [PrimeGt](#/node/PrimeGt) c p. It applies Mathlib's `Nat.exists_infinite_primes (c + 1)` (SimpleGen.lean line 19). Used by [min_prime_gt](#/node/min_prime_gt), hence by [SimpleGen](#/node/SimpleGen). The RakeSieve does not use it: SimpleGen.lean is not imported by Results.lean.
""",
 [q("Which Mathlib theorem does it call?", ["`Nat.exists_infinite_primes`", "`Nat.find`"], 0, "SimpleGen.lean line 19."),
  q("Is its statement Euclid's theorem?", ["Yes, in the form ∀ c, ∃ prime p > c", "No"], 0, "Same content as the infinitude corollary."),
  q("Why is c + 1 passed instead of c?", ["Mathlib's version gives c ≤ p; we need c < p", "no reason"], 0, "The comment on SimpleGen.lean line 17 says so.")])

node("min_prime_gt", "min_prime_gt n: the least prime above n, found by Nat.find",
 "It is computable in principle, since Nat.find just counts upward, but only because Euclid guarantees the search stops.",
 r"""
## Plain English

`min_prime_gt n` (SimpleGen.lean lines 24–28) is the [MinPrimeGt](#/node/MinPrimeGt) n whose number is `Nat.find (ex_prime_gt n)`: the least p satisfying [PrimeGt](#/node/PrimeGt) n p. `Nat.find_spec` and `Nat.find_min` give the two proofs. It is [SimpleGen](#/node/SimpleGen)'s step.
""",
 [q("What does `Nat.find` need?", ["a proof that some number satisfies the property", "an upper bound only"], 0, "Here `ex_prime_gt n`."),
  q("What is `(min_prime_gt 13).p`?", ["13", "17", "15"], 1, "17 is the least prime above 13."),
  q("Who uses it?", ["SimpleGen", "RakeSieve"], 0, "`SimpleGen.next` and `SimpleGen.start`.")])

node("SimpleGen", "SimpleGen: the obvious prime generator (reference spec, circular)",
 "It is the specification as a program, 'the next prime is the least prime above this one'. It exists so the RakeSieve has something to be compared with. It assumes Euclid, so it proves nothing about infinitude.",
 r"""
## Plain English

A `SimpleGen` (SimpleGen.lean lines 30–32) holds a prime p and the [least prime above it](#/node/MinPrimeGt). Its step moves to that prime ([SimpleGen.next](#/node/SimpleGen.next)), and [its PrimeGen instance](#/node/instPrimeGenSimpleGen) is proved directly from `hmin` and `hpgt`. SimpleGen.lean opens by saying it is a reference spec that assumes Euclid's theorem and is not on the RakeSieve's headline path. The `#guard` on SimpleGen.lean line 57 checks by evaluation that its first ten primes from [SimpleGen.start](#/node/SimpleGen.start) are 2, 3, 5, …, 29.
""",
 [q("What does a SimpleGen hold?", ["a prime and the least prime above it", "a rake"], 0, "Fields `p` and `c`."),
  q("Is the `#guard` on its first ten primes a proof?", ["it is a compile-time check by evaluation, not a theorem in Results.lean", "it is an axiom"], 0, "`#guard` fails compilation if the equation evaluates to false."),
  q("How does it find each prime?", ["Nat.find", "sieving"], 0, "via `min_prime_gt`.")])

node("SimpleGen.start", "SimpleGen.start: begin at 2",
 "This is the one place the simple generator says where primes begin; the PrimeGen class itself does not.",
 r"""
## Plain English

`SimpleGen.start := { p := ⟨2, Nat.prime_two⟩, c := min_prime_gt 2 }` (SimpleGen.lean lines 38–39): prime 2, next prime 3. Used by [simpleGen_exists_prime_gt](#/node/simpleGen_exists_prime_gt), the circular reference theorem. See [SimpleGen](#/node/SimpleGen) and [min_prime_gt](#/node/min_prime_gt).
""",
 [q("What is the start prime?", ["2", "3", "1"], 0, "SimpleGen.lean line 39."),
  q("What is its `c` field's number?", ["3", "5"], 0, "The least prime above 2."),
  q("Why is the start not part of PrimeGen?", ["by design; see the class docstring", "an oversight"], 0, "PrimeGen.lean lines 15–17.")])

node("instPrimeGenSimpleGen", "SimpleGen is a prime generator",
 "Both obligations fall straight out of the MinPrimeGt fields: 'nothing smaller' is `hmin`, 'bigger' is `hpgt`.",
 r"""
## Plain English

`instance : PrimeGen SimpleGen` (SimpleGen.lean lines 41–53): `P g := g.p`, `next := SimpleGen.next`. `hP'`: a prime between p and the next would contradict `hmin`. `hP_lt`: `hpgt` says the next prime is above p. See [PrimeGen](#/node/PrimeGen), [SimpleGen](#/node/SimpleGen).
""",
 [q("Which field gives 'no skipped prime'?", ["`hmin`", "`hpgt`"], 0, "SimpleGen.lean lines 44–48."),
  q("Which field gives strict increase?", ["`hpgt`", "`hmin`"], 0, "SimpleGen.lean lines 49–51."),
  q("Is this instance anonymous in the source?", ["Yes; the site's name for it is approximate", "No"], 0, "`instance : PrimeGen SimpleGen where`.")],
 caveats=["An anonymous instance; the site's name for it is an approximation."])

node("three_mem_R_two", "3 ∈ R 2 (the lemma behind the headline)",
 "Shared by every sieve, it lives in PrimeSieve.lean, not in the RakeSieve, so any future sieve can start from it.",
 PLAIN_R + r"""**Theorem (`three_mem_R_two`, PrimeSieve.lean lines 19–27).** 3 ∈ [R](#/node/R) 2. Exported as [results_three_mem_R_two](#/node/results_three_mem_R_two), which has the proof outline. Used by [RakeSieve.init](#/node/RakeSieve.init).
""",
 [q("Which file holds it?", ["PrimeSieve.lean", "RakeSieve.lean"], 0, "Moved there in 37c37c7 so every sieve can use it."),
  q("How is ¬ 2 ∣ 3 checked?", ["`decide`", "`native_decide`"], 0, "By `decide`, PrimeSieve.lean line 27."),
  q("Which Results.lean theorem re-exports it?", ["`results_three_mem_R_two`", "`results_exists_prime_gt_of_rakeSieve`"], 0, "See Results.lean lines 11–12.")])

node("three_le_of_mem_R_two", "Nothing in R 2 is below 3 (the lemma behind the headline)",
 "R 2, the residue after sieving by 2, is the odd numbers from 3 up. With 3 ∈ R 2 this makes 3 its minimum, which is exactly what the start state must prove about its candidate.",
 PLAIN_R + r"""**Theorem (`three_le_of_mem_R_two`, PrimeSieve.lean lines 30–37).** Every r ∈ [R](#/node/R) 2 has 3 ≤ r. Exported as [results_three_le_of_mem_R_two](#/node/results_three_le_of_mem_R_two), which has the proof outline. Used by [RakeSieve.init](#/node/RakeSieve.init).
""",
 [q("Why is 2 excluded from R 2?", ["2 divides 2", "2 is not prime"], 0, "The prime 2 ≤ 2 divides it."),
  q("Which structure field does it provide for the start state?", ["`hRmin`", "`hprop`"], 0, "See RakeSieve.lean line 56."),
  q("Is it proved by contradiction?", ["Yes", "No"], 0, "`by_contra h` on PrimeSieve.lean line 32.")])

node("MinPrimeGt.p'", "MinPrimeGt.p': the next prime is prime",
 "It is a one-line projection, handy enough to get its own name.",
 r"""
## Plain English

`MinPrimeGt.p' m : Nat.Prime m.p` (PrimeGen.lean line 34): the first half of `hpgt`. See [MinPrimeGt](#/node/MinPrimeGt).
""",
 [q("What does it return?", ["a proof that m.p is prime", "the number m.p"], 0, "It is `m.hpgt.left`."),
  q("Which field does it read?", ["`hpgt`", "`hmin`"], 0, "`hpgt : PrimeGt n p`, whose left part is primality."),
  q("Is it a theorem or a definition?", ["theorem", "def"], 0, "Declared with `theorem` on PrimeGen.lean line 34.")])
