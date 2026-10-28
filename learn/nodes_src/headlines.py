# Explainer nodes for the headline theorems of Results.lean and the instance that carries the
# sieve's correctness. Written as Python data so the YAML is always valid; tools/write_nodes.py
# turns each entry into learn/nodes/<id>.md.
from _terms import PLAIN_R
NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}

node("results_exists_prime_gt_of_rakeSieve", "Main theorem: the RakeSieve never runs out of primes",
 "The statement never mentions the sieve. It is word for word Euclid's theorem, ∀ n, ∃ prime p > n, and the proof calls Mathlib's own proof of Euclid inside each sieve step. The sieve only appears in the proof.",
 r"""
## Plain English

**Theorem (`results_exists_prime_gt_of_rakeSieve`, Results.lean lines 19–21).** For every natural number n there is a prime p with n < p.

That is the whole statement. Nothing in it says "RakeSieve". The name says *how* it was proved: by starting the RakeSieve at [RakeSieve.init](#/node/RakeSieve.init), wrapping it as a [PrimeSieve](#/node/PrimeSieve), which is a prime generator by [the sieve driver](#/node/instPrimeGenPrimeSieve), and applying the general fact [exists_prime_gt_of_primeGen](#/node/exists_prime_gt_of_primeGen): a generator whose primes strictly increase must eventually pass any n.

### What this does and does not show

- **As a statement, it is Euclid's theorem.** Mathlib already has it (`Nat.exists_infinite_primes`). Two of the five theorems in Results.lean have exactly this statement; only the proofs differ.
- **As a proof, it is not independent of Euclid.** One sieve step, [RakeSieve.next](#/node/RakeSieve.next), must show that removing the multiples of the new prime c leaves *something* in the rake, so that the rake is never empty. It does this by asking Mathlib for a prime above c (`Nat.exists_infinite_primes`, RakeSieve.lean line 71). So the proof uses the theorem it states. This is not a flaw in the Lean (nothing is assumed that isn't proved), but the theorem should not be read as "a new proof that there are infinitely many primes".
- **What the proof does exercise** is the sieve's correctness: to build the generator, Lean has to accept that every RakeSieve step yields the next prime with none skipped. That guarantee is the real content, and it lives in an instance rather than a named theorem; see [instPrimeGenPrimeSieve](#/node/instPrimeGenPrimeSieve) and [the review](#/review).

### The outline

The proof is one line (Results.lean line 21). The outline below follows it, then shows what one sieve step does.
""",
 [q("What does the *statement* of `results_exists_prime_gt_of_rakeSieve` mention?",
    ["The RakeSieve and its initial state", "Only `Nat.Prime`, `<` and the natural numbers", "The list of primes the sieve produces", "The growth rate of the rake"], 1,
    "The statement is `∀ n, ∃ p, Nat.Prime p ∧ n < p` (Results.lean lines 19–20). RakeSieve appears only in the proof term on line 21."),
  q("Which other theorem in Results.lean has exactly the same statement?",
    ["`results_three_mem_R_two`", "`results_exists_prime_gt_of_simpleGen`", "`results_three_le_of_mem_R_two`", "none"], 1,
    "`results_exists_prime_gt_of_simpleGen (n : Nat) : ∃ p, Nat.Prime p ∧ n < p` has the same type; it runs the brute-force `SimpleGen` instead of the RakeSieve."),
  q("Does the proof use Mathlib's infinitude of primes anywhere?",
    ["No, it is a self-contained proof of Euclid", "Yes: `RakeSieve.next` calls `Nat.exists_infinite_primes` to show the rake never becomes empty", "Only through `decide`"], 1,
    "RakeSieve.lean line 71: `Nat.exists_infinite_primes rs₀.c.succ` gives a prime q > c, which survives the removal of c's multiples."),
  q("Where is the claim 'each RakeSieve step yields the next prime, none skipped' checked?",
    ["In the statement of this theorem", "In the `PrimeGen (PrimeSieve α)` instance and the generic driver lemmas it uses", "Only in `Main.lean`'s `#eval`", "It is not checked"], 1,
    "The `PrimeGen` class (PrimeGen.lean lines 19–26) demands `hP'` (no skipped prime) and `hP_lt` (strict increase). The instance for `PrimeSieve α` proves both from `c_prime`, `no_skipped_prime` and `c_gt_p`.")],
 caveats=[
  "The statement is Euclid's theorem and says nothing about the sieve. Read it as 'the sieve, run forever, keeps producing primes', not as 'the sieve is correct'.",
  "The proof is not independent of Mathlib's infinitude of primes: RakeSieve.next uses `Nat.exists_infinite_primes` (RakeSieve.lean line 71).",
  "This site did not build the Lean. The statement and proof are read from the source text at commit 36e7360; see the Trust page."],
 widgets=[
  {"type": "walkthrough", "title": "How Results.lean proves it (Results.lean, lines 19-21)", "config": {"steps": [
   {"text": "Start the sieve: RakeSieve.init has found the prime 2, and its rake lists exactly the odd numbers ≥ 3", "lean": "{ state := RakeSieve.init }", "link": "RakeSieve.init",
    "note": "The initial state carries proofs that 3 is in R 2 and that nothing in R 2 is below 3 (the two other headline theorems)."},
   {"text": "Wrap it as a PrimeSieve. The generic driver makes any PrimeSieve a PrimeGen: each step gives the next prime, strictly larger, none skipped", "lean": "PrimeSieve RakeSieve", "link": "instPrimeGenPrimeSieve",
    "note": "Lean finds this by type-class search: RakeSieve has PrimeSieveState and PrimeSieveDriver instances, so PrimeSieve RakeSieve has a PrimeGen instance."},
   {"text": "Apply the general fact: a prime generator whose primes strictly increase passes any n after n + 1 steps", "lean": "exists_prime_gt_of_primeGen", "link": "exists_prime_gt_of_primeGen",
    "note": "The primes go up by at least 1 per step, and start at 2 or more, so after n + 1 steps the prime is at least n + 3."}]}},
  {"type": "walkthrough", "title": "What one sieve step does (RakeSieve.lean, lines 55-111)", "config": {"steps": [
   {"text": "The candidate c is prime and no prime lies between p and c (supplied by the driver), so c is the least prime above p", "lean": "let c' : MinPrimeGt rs₀.p := { p:=rs₀.c, hpgt:=hpgt, hmin:=hmin}", "link": "MinPrimeGt"},
   {"text": "Show that removing c's multiples leaves something: Mathlib gives a prime q > c, and q is in R p but is not a multiple of c", "lean": "Nat.exists_infinite_primes rs₀.c.succ",
    "note": "This is the step that uses Mathlib's Euclid. Without it, the rake operation `rem` would have no guarantee of a non-empty result."},
   {"text": "Remove the multiples of c from the rake (partition each sequence into c sequences, drop those whose constant is a multiple of c, sort)", "lean": "let rs := rs₀.rm.rem c'.p (Nat.Prime.pos hC₀) this", "link": "RakeMap.rem"},
   {"text": "The new candidate is the rake's first term", "lean": "let c₁ := rs.rake.term 0", "link": "Rake.term"},
   {"text": "The new rake lists exactly R c: numbers ≥ 2 with no prime factor up to c", "lean": "intro n; exact r_next_prop (hh₀ n) (hh₁ n)", "link": "r_next_prop"},
   {"text": "Its first term is its least term, because the rake is sorted, so the new candidate is the minimum of R c", "lean": "exact rs.min_term_zero k }", "link": "RakeMap.min_term_zero"}]}}])

node("instPrimeGenPrimeSieve", "The sieve driver: every PrimeSieve is a prime generator",
 "The sieve's correctness theorem is not a named theorem at all. It is this instance: any sieve state whose candidate is the least survivor gives, step by step, the next prime with none skipped. It is proved once, for every such sieve.",
 PLAIN_R + r"""**Instance (`instance : PrimeGen (PrimeSieve α)`, PrimeSieve.lean lines 218–242).** For any type α of sieve states that has a [PrimeSieveState](#/node/PrimeSieveState) and a [PrimeSieveDriver](#/node/PrimeSieveDriver) instance, the wrapper [PrimeSieve](#/node/PrimeSieve) α is a [PrimeGen](#/node/PrimeGen): a prime generator. Concretely:

- its current prime is the state's prime P;
- one step runs the sieve once ([PrimeSieve.next](#/node/PrimeSieve.next));
- **no prime is skipped**: there is no prime strictly between the current prime and the next one (`hP'`);
- **the prime goes up**: the next prime is strictly bigger (`hP_lt`).

Both facts come from three generic lemmas about any driven sieve state, where C is its candidate and R P is the set of numbers ≥ 2 with no prime factor up to P ([R](#/node/R)):

1. [c_prime](#/node/c_prime): C is prime, since its prime factors would be ≤ P (impossible, C is in R P) or between P and C (impossible, see 2);
2. [no_skipped_prime](#/node/no_skipped_prime): no prime lies strictly between P and C, since such a prime would be in R P and smaller than its minimum C;
3. [c_gt_p](#/node/c_gt_p): C > P, since everything in R P is bigger than P ([r_gt_p](#/node/r_gt_p)).

And the state's own `hNext` field says that one step turns C into the new P.

For the RakeSieve, α = [RakeSieve](#/node/RakeSieve): its states carry the proofs the driver needs ([the PrimeSieveDriver instance](#/node/RakeSieve.instPrimeSieveDriverRakeSieve)), so `PrimeSieve RakeSieve` is a prime generator. That is what the main theorem uses.

### What it adds up to (not stated in Lean)

Starting from [RakeSieve.init](#/node/RakeSieve.init), whose prime is 2, these two facts mean the sieve lists 2, 3, 5, 7, 11, … *all* the primes, in order. That conclusion is one short induction away, but Results.lean does not state it. There is no theorem saying "the n-th prime the sieve produces is the n-th prime" or "every prime is eventually produced". See [the review](#/review).
""",
 [q("What are the two facts a `PrimeGen` instance must prove?",
    ["the prime is even, and it is less than 100", "no prime lies strictly between the current prime and the next one, and the next prime is bigger", "the state is finite, and it is sorted", "the sieve terminates"], 1,
    "PrimeGen.lean lines 23 and 26: `hP'` (no skipped prime) and `hP_lt` (strict increase)."),
  q("Why can no prime q lie strictly between P and the candidate C?",
    ["because q would be in R P, and C is the least element of R P", "because q would divide C", "because the rake is sorted", "because of `decide`"], 0,
    "`no_skipped_prime` (PrimeSieve.lean lines 133–151): a prime q > P has no prime factor ≤ P (its only prime factor is q), so q ∈ R P, and `hRmin` says C ≤ q."),
  q("Is 'the sieve started at 2 produces every prime' stated as a theorem?",
    ["Yes, in Results.lean", "No: it follows from this instance plus the start state, but no theorem states it"], 1,
    "Results.lean exports only Euclid-type statements and two facts about R 2. The enumeration property is implicit in the `PrimeGen` instance."),
  q("Which sieves does this instance cover?",
    ["only the RakeSieve", "any type with `PrimeSieveState` and `PrimeSieveDriver` instances", "only SimpleGen"], 1,
    "It is stated for an arbitrary α under `variable (α : Type) [PrimeSieveState α] [PrimeSieveDriver α]` (PrimeSieve.lean line 210).")],
 caveats=[
  "This is an `instance`, so it has no name in the source; this site calls it `instPrimeGenPrimeSieve`, the name Lean most likely generates. The exact generated name was not checked (no Lean build).",
  "Completeness ('every prime appears') follows easily but is not stated in Lean."],
 widgets=[{"type": "walkthrough", "title": "How the instance is proved (PrimeSieve.lean, lines 218-242)", "config": {"steps": [
   {"text": "The generator's prime is the state's prime; a step runs the sieve once", "lean": "next := PrimeSieve.next (α := α)", "link": "PrimeSieve.next"},
   {"text": "From the driver: the candidate C is prime, and no prime lies strictly between P and C", "lean": "have hc' := c_prime α s.state", "uses": ["c_prime", "no_skipped_prime"]},
   {"text": "The state's hNext field: after one step, the new prime P is the old candidate C", "lean": "(PrimeSieveState.hNext (α := α) s.state hc' hns rfl).left", "link": "PrimeSieveState"},
   {"text": "No skipped prime: a prime between P and the new P would lie between P and C, which no_skipped_prime rules out", "lean": "exact hns ⟨q, hq, hgt', hlt'⟩", "link": "no_skipped_prime"},
   {"text": "Strict increase: the new P is C, and C > P", "lean": "have hgt := c_gt_p α s.state", "link": "c_gt_p"}]}}])

node("results_exists_prime_gt_of_primeGen", "Any prime generator proves Euclid (CONDITIONAL)",
 "This one *is* a genuine proof of infinitude, but conditional: if you hand it any prime generator at all, primes go on forever. Only strict increase is used; the 'no skipped prime' half is not needed.",
 r"""
## Plain English

**Theorem (`results_exists_prime_gt_of_primeGen`, Results.lean lines 11–13). CONDITIONAL.** Let α be any type with a [PrimeGen](#/node/PrimeGen) instance, and g₀ any state. Then for every n there is a prime p > n.

The hypothesis is the `PrimeGen` instance (and a state g₀ to start from). Given those, the proof is elementary and does **not** use Mathlib's infinitude of primes: after k steps the prime has gone up by at least k ([PrimeGen.P_iterate_add_le](#/node/PrimeGen.P_iterate_add_le)), and the first prime is at least 2, so after n + 1 steps it is at least n + 3 > n.

So the honest reading is: *infinitely many primes follows from the existence of a generator whose primes strictly increase*. That moves the work into building a generator. The two concrete generators in this library ([SimpleGen](#/node/SimpleGen) and the RakeSieve) both use Mathlib's `Nat.exists_infinite_primes` to get built, so neither gives an independent proof of Euclid. See the [main theorem](#/node/results_exists_prime_gt_of_rakeSieve).

Only `hP_lt` (strict increase) is used. The docstring of [exists_prime_gt_of_primeGen](#/node/exists_prime_gt_of_primeGen) says why `hP'` alone would not do: a generator stuck on one prime skips nothing.
""",
 [q("What is assumed?",
    ["nothing: it is Euclid's theorem outright", "a `PrimeGen` instance on some type α, and a state g₀", "the Riemann hypothesis", "that the RakeSieve is correct"], 1,
    "The signature is `{α : Type} [PrimeGen α] (g₀ : α) (n : Nat)` (Results.lean line 11)."),
  q("Which field of `PrimeGen` does the proof use?",
    ["`hP'` (no skipped prime)", "`hP_lt` (strict increase)", "both", "neither"], 1,
    "`PrimeGen.P_iterate_add_le` is proved by induction from `hP_lt` (PrimeGen.lean line 106)."),
  q("Why can't `hP'` alone prove infinitude?",
    ["it can", "a generator that stays on the same prime forever satisfies `hP'`", "`hP'` is false for SimpleGen"], 1,
    "If `next g = g`, there is nothing strictly between P g and P g, so `hP'` holds, but only one prime is ever produced. PrimeGen.lean lines 24–25 say this.")],
 caveats=["Conditional on a PrimeGen instance. Every concrete instance in this repository is built with the help of Mathlib's `Nat.exists_infinite_primes`."],
 widgets=[{"type": "walkthrough", "title": "The proof (PrimeGen.lean, lines 112-118)", "config": {"steps": [
   {"text": "Take k = n + 1 steps", "lean": "let k := n + 1"},
   {"text": "After k steps the prime has grown by at least k", "lean": "PrimeGen.P_iterate_add_le g₀ k", "link": "PrimeGen.P_iterate_add_le"},
   {"text": "The starting prime is at least 2 (it is prime)", "lean": "Nat.Prime.two_le (P g₀).prop"},
   {"text": "Offer the prime after k steps as the witness; it is prime because generator values are primes", "lean": "refine ⟨P (next^[k] g₀), (P (next^[k] g₀)).prop, ?_⟩", "link": "NPrime"},
   {"text": "Arithmetic: 2 + (n + 1) > n", "lean": "omega"}]}}])

node("results_exists_prime_gt_of_simpleGen", "Euclid via the brute-force generator",
 "The 'simple' generator finds the next prime by asking Mathlib for the least prime above p, which already presupposes there is one. So this is Euclid proved from Euclid, a sanity check of the PrimeGen interface.",
 r"""
## Plain English

**Theorem (`results_exists_prime_gt_of_simpleGen`, Results.lean lines 15–17).** For every n there is a prime p > n.

Same statement as the [main theorem](#/node/results_exists_prime_gt_of_rakeSieve). The proof runs the general fact [exists_prime_gt_of_primeGen](#/node/exists_prime_gt_of_primeGen) on [SimpleGen.start](#/node/SimpleGen.start), the brute-force generator: its next prime is `Nat.find` of "a prime greater than p" ([min_prime_gt](#/node/min_prime_gt)), whose existence comes from Mathlib's `Nat.exists_infinite_primes` ([ex_prime_gt](#/node/ex_prime_gt), PrimeGen.lean line 42).

Its value is as a reference point: it shows the [PrimeGen](#/node/PrimeGen) interface is satisfiable by the obvious specification ("the least prime above p"), against which the RakeSieve can be compared.
""",
 [q("How does `SimpleGen` find the next prime?",
    ["by trial division", "as the least prime greater than p, via `Nat.find`", "with the rake"], 1,
    "`min_prime_gt n` uses `Nat.find (ex_prime_gt n)` (PrimeGen.lean lines 47–51)."),
  q("Is this an independent proof that there are infinitely many primes?",
    ["Yes", "No: building SimpleGen uses `Nat.exists_infinite_primes`"], 1,
    "`ex_prime_gt` calls `Nat.exists_infinite_primes` (PrimeGen.lean line 42)."),
  q("What is SimpleGen's first prime?",
    ["1", "2", "3"], 1, "`SimpleGen.start := { p := ⟨2, Nat.prime_two⟩, … }` (PrimeGen.lean line 62).")],
 caveats=["Circular as a proof of Euclid; it checks the interface, not number theory."],
 widgets=[{"type": "walkthrough", "title": "The proof (Results.lean, lines 15-17)", "config": {"steps": [
   {"text": "Start the brute-force generator at 2", "lean": "SimpleGen.start", "link": "SimpleGen.start"},
   {"text": "It is a PrimeGen: its next prime is the least prime above the current one", "link": "instPrimeGenSimpleGen"},
   {"text": "Apply the general fact about prime generators", "lean": "exists_prime_gt_of_primeGen", "link": "exists_prime_gt_of_primeGen"}]}}])

node("results_three_mem_R_two", "3 survives sieving by 2",
 "A fact this small is a headline because it is the sieve's base case: after crossing out multiples of 2, the number 3 is still there. Lean checks it by computation (`decide`), not by reasoning.",
 PLAIN_R + r"""**Theorem (`results_three_mem_R_two`, Results.lean lines 5–6).** 3 ∈ R 2: the number 3 is at least 2 and is not divisible by any prime q ≤ 2.

[R](#/node/R) P is the set of numbers that survive a sieve once every prime up to P has crossed out its multiples. So R 2 is the odd numbers from 3 up, and this theorem says 3 is one of them.

Why it matters: the RakeSieve starts with prime p = 2 and candidate c = 3 ([RakeSieve.init](#/node/RakeSieve.init)). Every sieve state must prove that its candidate lies in R p; for the start state that proof is this theorem (RakeSieve.lean line 50). It was moved out of `RakeSieve.init` into PrimeSieve.lean so that any sieve can reuse it (issue #3).
""",
 [q("Which set is R 2?",
    ["all numbers ≥ 2", "the odd numbers ≥ 3", "the primes", "the even numbers"], 1,
    "R 2 = { n | n ≥ 2 ∧ ∀ q ≤ 2, q prime → ¬ q ∣ n }. The only prime ≤ 2 is 2, so these are the n ≥ 2 that are odd."),
  q("How does Lean check `¬ 2 ∣ 3`?",
    ["`native_decide`", "`decide` (evaluated by the kernel)", "an axiom"], 1,
    "PrimeSieve.lean line 27: `decide`. That is ordinary kernel evaluation, with no extra trust."),
  q("Where is this fact used?",
    ["As the base case for RakeSieve.init's proof that its candidate 3 is in R 2", "Nowhere", "In Main.lean only"], 0,
    "RakeSieve.lean line 50: `simpa [p] using three_mem_R_two`.")],
 widgets=[{"type": "walkthrough", "title": "The proof (PrimeSieve.lean, lines 19-27)", "config": {"steps": [
   {"text": "3 ≥ 2, by computation", "lean": "refine ⟨by decide, ?_⟩"},
   {"text": "Any prime q ≤ 2 is at least 2, so q = 2", "lean": "have := Nat.Prime.two_le hq'"},
   {"text": "2 does not divide 3, by computation", "lean": "decide"}]}}])

node("results_three_le_of_mem_R_two", "Nothing in R 2 is smaller than 3",
 "With the previous theorem this pins down the sieve's first candidate: 3 is the *least* survivor after sieving by 2. That is exactly what the sieve needs to know 3 is the next prime.",
 PLAIN_R + r"""**Theorem (`results_three_le_of_mem_R_two`, Results.lean lines 8–9).** Every r ∈ R 2 satisfies 3 ≤ r.

Together with [3 ∈ R 2](#/node/results_three_mem_R_two), this says 3 is the minimum of [R](#/node/R) 2. The sieve's start state needs both: its candidate must be in R p (`hCinR`) and below everything else in R p (`hRmin`). See the [RakeSieve](#/node/RakeSieve) structure and RakeSieve.lean lines 48–53.

The proof: anything in R 2 is ≥ 2; if it were below 3 it would be 2, but 2 divides 2, so 2 is not in R 2.
""",
 [q("Why is 2 not in R 2?",
    ["2 is not prime", "the prime 2 ≤ 2 divides 2", "R 2 starts at 4"], 1,
    "R 2 requires that no prime q ≤ 2 divides n. For n = 2, q = 2 divides it."),
  q("Combined with `results_three_mem_R_two`, what do we learn?",
    ["3 is the least element of R 2", "R 2 is finite", "3 is the only element of R 2"], 0,
    "3 is in R 2 and is ≤ every element of R 2."),
  q("Which field of the RakeSieve structure does this discharge for the start state?",
    ["`hCinR`", "`hRmin`", "`hprop`"], 1,
    "`hRmin : ∀ r ∈ R p, c ≤ r` (RakeSieve.lean line 12); RakeSieve.lean line 53 uses this theorem.")],
 widgets=[{"type": "walkthrough", "title": "The proof (PrimeSieve.lean, lines 30-37)", "config": {"steps": [
   {"text": "Suppose r ∈ R 2 but r < 3", "lean": "by_contra h"},
   {"text": "Since r ≥ 2, r = 2", "lean": "have r2 : r = 2 := by omega"},
   {"text": "But R 2 says the prime 2 does not divide r = 2, which is false", "lean": "have := hrr 2 (by omega) Nat.prime_two"}]}}])
