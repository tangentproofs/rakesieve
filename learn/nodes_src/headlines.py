# Explainer nodes for the headline theorems of Results.lean and the instance that carries the
# sieve's correctness. Written as Python data so the YAML is always valid; tools/write_nodes.py
# turns each entry into learn/nodes/<id>.md.
from _terms import PLAIN_R
NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}

node("results_rakeSieve_never_empty", "Headline: the sieve never runs empty",
 "The sieve supplies its own proof that it can always take another step: after the multiples of the candidate c are crossed out, the number c + d is still in the rake, where d is the rake's period. No theorem about infinitely many primes is used.",
 PLAIN_R + r"""**Theorem (`results_rakeSieve_never_empty`, Results.lean lines 20–22).** For every [RakeSieve](#/node/RakeSieve) state s there are numbers n and m with s.c ∤ n and `s.rm.term m = n`. In words: some term of the state's rake is not a multiple of its candidate c.

**Why the sieve needs this.** A sieve step removes the multiples of c with [RakeMap.rem](#/node/RakeMap.rem), and `rem` will not run without a proof that something survives ([HasNonMultiple](#/node/Rake.HasNonMultiple)). This theorem is that proof, for every state. Until PR #5 the step got it by asking Mathlib for a prime above c (`Nat.exists_infinite_primes`). That made the infinitude corollary circular, since it used infinitude of primes to prove infinitude of primes.

**The witness is c + d.** The proof is [RakeSieve.survivor](#/node/RakeSieve.survivor):

1. c is a term of the rake, say term m₀, because c ∈ R p (`hCinR`) and the rake lists exactly R p (`hprop`, `hbij`).
2. One full turn of the rake later, term (m₀ + len) = c + d, where len is the number of sequences and d is their common step ([Rake.term_add_len](#/node/Rake.term_add_len)).
3. Every prime factor of d is ≤ p. This is the invariant `hdfac`, which every [RakeSieve](#/node/RakeSieve) state carries. c is a prime bigger than p ([r_gt_p](#/node/r_gt_p)), so c ∤ d, and therefore c ∤ c + d.

**This is still Euclid's idea.** In Euclid's proof, p# + 1 (one more than the product of the primes up to p) has no prime factor ≤ p. Here the period d plays the part of p#, and c + d is the survivor. What changed is where the argument lives. It is carried by the data structure, as an invariant that every step maintains, instead of being imported as a theorem. So infinitude of primes is now a consequence of the algorithm, not an input to it.

Lean states only that the prime factors of d are all ≤ p (`hdfac`). In fact d is exactly p# = 2·3·5·…·p: the start rake has period 2, and each step multiplies the period by the new prime ([RakeMap.rem_d](#/node/RakeMap.rem_d)). That equality is not stated as a theorem, and the proof does not need it.
""",
 [q("What does the sieve step need this theorem for?",
    ["`RakeMap.rem` needs proof that removing c's multiples leaves something", "to prove c is prime", "to sort the rake", "nothing, it is decorative"], 0,
    "RakeMap.rem's argument `hnmr: ∃n m, ¬j∣n ∧ rm.term m = n` (RakeMap.lean line 48). RakeSieve.next supplies it as `rs₀.survivor hC₀` (RakeSieve.lean line 98)."),
  q("Which number is the witness that survives?",
    ["a prime above c, from Mathlib", "c + d, one period past c", "c + 1", "2"], 1,
    "`refine ⟨s.c + s.rm.rake.d, m₀ + s.rm.rake.ks.length, ?_, ?_⟩` (RakeSieve.lean line 75)."),
  q("Why can't c divide c + d?",
    ["it would then divide d, but every prime factor of d is ≤ p < c", "because c + d is prime", "because d is odd"], 0,
    "If c ∣ c + d then c ∣ d; `hdfac` gives c ≤ p, and `r_gt_p` gives c > p (RakeSieve.lean lines 77–80)."),
  q("Is this a new mathematical proof that there are infinitely many primes?",
    ["Yes, a completely new idea", "No: c + d plays the part of Euclid's p# + 1, but no infinitude theorem is imported"], 1,
    "The idea is Euclid's. The circularity is gone, because the invariant `hdfac` is maintained by the sieve itself.")],
 caveats=[
  "Euclid's argument, carried by the data structure: c + d (d = p#) plays the part of p# + 1. This removes the circularity, not Euclid's idea.",
  "This site did not build the Lean. The claim that no infinitude theorem is used rests on NoEuclidCheck.lean as run for PR #5 (see the Trust page)."],
 widgets=[{"type": "walkthrough", "title": "How RakeSieve.survivor proves it (RakeSieve.lean, lines 72-82)", "config": {"steps": [
   {"text": "c is in R p, so it is a term of the rake, at some index m₀", "lean": "obtain ⟨m₀, hm₀⟩ := (s.rm.hbij s.c).mp ((s.hprop s.c).mpr s.hCinR)", "link": "RakeMap"},
   {"text": "Offer c + d as the survivor, at index m₀ + len (one period on)", "lean": "refine ⟨s.c + s.rm.rake.d, m₀ + s.rm.rake.ks.length, ?_, ?_⟩"},
   {"text": "If c divided c + d, it would divide d", "lean": "have hcd : s.c ∣ s.rm.rake.d := (Nat.dvd_add_iff_right (dvd_refl s.c)).mpr hdvd"},
   {"text": "Then c ≤ p, by the invariant hdfac (every prime factor of d is ≤ p)", "lean": "have hle : s.c ≤ s.p.val := s.hdfac s.c hC hcd", "link": "RakeSieve"},
   {"text": "But c > p, because c is in R p", "lean": "have hgt : s.c > s.p.val := r_gt_p s.p.val s.c s.hCinR", "link": "r_gt_p"},
   {"text": "And c + d really is a term: one period past term m₀", "lean": "rw [Rake.term_add_len, hm₀]", "link": "Rake.term_add_len"}]}}])

node("results_rakeSieve_step", "Headline: each step emits the next prime, none skipped",
 "The sieve's correctness used to be hidden inside an instance. Now it is a theorem anyone can cite: one step turns the candidate into the new prime, the candidate is prime and bigger than the old prime, and no prime was jumped over.",
 PLAIN_R + r"""**Theorem (`results_rakeSieve_step`, Results.lean lines 27–31).** For every [RakeSieve](#/node/RakeSieve) state s, with prime p and candidate c:

1. one step ([nextState](#/node/nextState)) makes c the new prime;
2. c is prime;
3. p < c;
4. no prime q lies strictly between p and c.

Together these say the step moves from p to the very next prime. The proof only assembles results proved once for every sieve. Each state's candidate is the least element of R p, so by [c_prime](#/node/c_prime) it is prime, by [c_gt_p](#/node/c_gt_p) it is above p, and by [no_skipped_prime](#/node/no_skipped_prime) no prime lies in between. The state's `hNext` field ([PrimeSieveState](#/node/PrimeSieveState)) says the step makes c the new prime.

The same facts feed [the sieve driver instance](#/node/instPrimeGenPrimeSieve). This theorem states them directly for the RakeSieve, as the earlier review asked.
""",
 [q("After one step, what is the new prime?",
    ["the old candidate c", "p + 2", "the least term of the old rake times 2"], 0,
    "First conjunct: `((nextState s).p : Nat) = s.c` (Results.lean line 28)."),
  q("Which generic lemma rules out a prime strictly between p and c?",
    ["`no_skipped_prime`", "`c_gt_p`", "`Rake.term_add_len`"], 0,
    "Such a prime would be in R p and below its least element c."),
  q("Does this theorem need Mathlib's infinitude of primes?",
    ["Yes", "No: NoEuclidCheck.lean checks its whole dependency closure"], 1,
    "See the Trust page for the check output.")],
 widgets=[{"type": "walkthrough", "title": "The proof (Results.lean, lines 27-31)", "config": {"steps": [
   {"text": "The state's hNext field: one step turns the candidate into the new prime", "lean": "(PrimeSieveState.hNext s (c_prime RakeSieve s) (no_skipped_prime RakeSieve s) rfl).1", "link": "PrimeSieveState"},
   {"text": "The candidate is prime (it is the least element of R p)", "lean": "c_prime RakeSieve s,", "link": "c_prime"},
   {"text": "The candidate is bigger than p (everything in R p is)", "lean": "c_gt_p RakeSieve s", "link": "c_gt_p"},
   {"text": "No prime lies strictly between p and c", "lean": "no_skipped_prime RakeSieve s⟩", "link": "no_skipped_prime"}]}}])

node("results_rakeSieve_emits_every_prime", "Headline: started at 2, the sieve emits every prime",
 "Not just 'the sieve produces primes' but 'it produces all of them': for every prime q, running the sieve from its start state reaches q after some number of steps.",
 r"""
## Plain English

**Theorem (`results_rakeSieve_emits_every_prime`, Results.lean lines 35–37).** For every prime q there is a number of steps k such that the sieve, started at [RakeSieve.init](#/node/RakeSieve.init) and stepped k times, has current prime q.

With [the step theorem](#/node/results_rakeSieve_step) this says the sieve lists 2, 3, 5, 7, 11, …, every prime in order, with none missed and none repeated.

The proof is one line. The generic lemma [PrimeGen.exists_iterate_P_eq](#/node/PrimeGen.exists_iterate_P_eq) says that any prime generator emits every prime at or above its start prime. The sieve starts at 2, and every prime is ≥ 2. The generator here is [PrimeSieve](#/node/PrimeSieve) RakeSieve, a prime generator by [the sieve driver](#/node/instPrimeGenPrimeSieve).
""",
 [q("What does the theorem promise for q = 7?",
    ["some number of steps after which the sieve's prime is 7", "that 7 is the 7th prime", "nothing; 7 is too small"], 0,
    "For every prime q there is k with P (next^[k] start) = q."),
  q("Why does the proof need `Nat.Prime.two_le hq`?",
    ["the generic lemma only covers primes at or above the start prime, which is 2", "to show q is odd", "it doesn't"], 0,
    "`PrimeGen.exists_iterate_P_eq _ q hq (Nat.Prime.two_le hq)` (Results.lean line 37)."),
  q("Which property of a prime generator makes 'every prime' work?",
    ["`hP'`: no prime is skipped between one step and the next", "only that the primes increase"], 0,
    "Increase alone could skip primes; `hP'` rules that out.")],
 widgets=[{"type": "walkthrough", "title": "The proof (Results.lean, lines 35-37)", "config": {"steps": [
   {"text": "Run the sieve from its start state, prime 2", "lean": "({ state := RakeSieve.init } : PrimeSieve RakeSieve)", "link": "RakeSieve.init"},
   {"text": "Any prime generator emits every prime at or above its start; every prime is ≥ 2", "lean": "PrimeGen.exists_iterate_P_eq _ q hq (Nat.Prime.two_le hq)", "link": "PrimeGen.exists_iterate_P_eq"}]}}])

node("results_exists_prime_gt_of_rakeSieve", "Corollary: infinitely many primes, from the sieve",
 "The statement is Euclid's theorem, but the proof imports no infinitude result: the sieve never runs empty and its primes keep going up, so they pass any n. Infinitude of primes is a corollary of the algorithm, not an input to it.",
 r"""
## Plain English

**Theorem (`results_exists_prime_gt_of_rakeSieve`, Results.lean lines 46–48).** For every natural number n there is a prime p with n < p.

The statement never mentions the sieve. Only the proof does: start the RakeSieve at [RakeSieve.init](#/node/RakeSieve.init), wrap it as a [PrimeSieve](#/node/PrimeSieve), which is a prime generator by [the sieve driver](#/node/instPrimeGenPrimeSieve), and apply [exists_prime_gt_of_primeGen](#/node/exists_prime_gt_of_primeGen): a generator whose primes strictly increase passes any n.

### What this does and does not show

- **As a statement, it is Euclid's theorem.** Mathlib already has it (`Nat.exists_infinite_primes`).
- **As a proof, it does not use Mathlib's Euclid.** Every sieve step must know that crossing out the new prime's multiples leaves something in the rake. The rake now proves that itself, with the survivor c + d ([the never-empty headline](#/node/results_rakeSieve_never_empty)). NoEuclidCheck.lean walks the full dependency closure of this theorem, through Mathlib and core, and finds nothing from `Mathlib.Data.Nat.Prime.Infinite` or a list of known infinitude results. A control check confirms that the same walk does find Euclid in the circular [reference generator](#/node/simpleGen_exists_prime_gt).
- **The idea is still Euclid's.** The survivor c + d works because d, the rake's period, is the product of the primes sifted so far. This is Euclid's p# + 1 carried by the data structure. It is not a new kind of proof, but it is no longer circular.
- **The sieve's correctness has its own headlines:** [each step emits the next prime](#/node/results_rakeSieve_step) and [every prime is emitted](#/node/results_rakeSieve_emits_every_prime).

### The outline

The proof is one line (Results.lean line 48). The outline below follows it, then shows what one sieve step does.
""",
 [q("What does the *statement* of `results_exists_prime_gt_of_rakeSieve` mention?",
    ["The RakeSieve and its initial state", "Only `Nat.Prime`, `<` and the natural numbers", "The list of primes the sieve produces", "The growth rate of the rake"], 1,
    "The statement is `∀ n, ∃ p, Nat.Prime p ∧ n < p` (Results.lean lines 46–47). RakeSieve appears only in the proof term on line 48."),
  q("Does the proof use Mathlib's infinitude of primes anywhere?",
    ["Yes, inside every sieve step", "No: each step's survivor is c + d, built from the rake itself, and NoEuclidCheck.lean confirms that no infinitude theorem is reachable"], 1,
    "RakeSieve.next gets its survivor from `rs₀.survivor hC₀` (RakeSieve.lean line 98)."),
  q("Which classical argument does the survivor c + d echo?",
    ["Euclid's p# + 1", "Eratosthenes' p² bound", "Bertrand's postulate"], 0,
    "d is the product of the primes sifted so far, so c + d plays the part of p# + 1."),
  q("Where is the claim 'each RakeSieve step yields the next prime, none skipped' stated?",
    ["Nowhere", "In `results_rakeSieve_step`, and generically in the `PrimeGen (PrimeSieve α)` instance", "Only in `Main.lean`'s `#eval`"], 1,
    "Results.lean lines 27–31 state it for every RakeSieve state.")],
 caveats=[
  "The statement is Euclid's theorem and says nothing about the sieve. The sieve's correctness is stated by the step and every-prime headlines.",
  "The mathematical idea is Euclid's (c + p# in place of p# + 1). What is new is that the sieve carries it, so the proof is not circular.",
  "This site did not build the Lean. The no-Euclid check and `#print axioms` were run on the tcode server for PR #5; see the Trust page."],
 widgets=[
  {"type": "walkthrough", "title": "How Results.lean proves it (Results.lean, lines 46-48)", "config": {"steps": [
   {"text": "Start the sieve: RakeSieve.init has found the prime 2, and its rake lists exactly the odd numbers ≥ 3", "lean": "{ state := RakeSieve.init }", "link": "RakeSieve.init",
    "note": "The initial state carries proofs that 3 is in R 2 (the residue left after crossing out multiples of 2), that nothing in R 2 is below 3, and that the rake's period, 2, has no prime factor above 2."},
   {"text": "Wrap it as a PrimeSieve. The generic driver makes any PrimeSieve a PrimeGen: each step gives the next prime, strictly larger, none skipped", "lean": "PrimeSieve RakeSieve", "link": "instPrimeGenPrimeSieve",
    "note": "Lean finds this by type-class search: RakeSieve has PrimeSieveState and PrimeSieveDriver instances, so PrimeSieve RakeSieve has a PrimeGen instance."},
   {"text": "Apply the general fact: a prime generator whose primes strictly increase passes any n after n + 1 steps", "lean": "exists_prime_gt_of_primeGen", "link": "exists_prime_gt_of_primeGen",
    "note": "The primes go up by at least 1 per step, and start at 2 or more, so after n + 1 steps the prime is at least n + 3."}]}},
  {"type": "walkthrough", "title": "What one sieve step does (RakeSieve.lean, lines 84-136)", "config": {"steps": [
   {"text": "The candidate c is prime and no prime lies between p and c (supplied by the driver), so c is the least prime above p", "lean": "let c' : MinPrimeGt rs₀.p := { p:=rs₀.c, hpgt:=hpgt, hmin:=hmin}", "link": "MinPrimeGt"},
   {"text": "Show that removing c's multiples leaves something: the rake's own term c + d survives", "lean": "have hsurv : ∃n m, ¬rs₀.c ∣ n ∧ rs₀.rm.term m = n := rs₀.survivor hC₀", "link": "RakeSieve.survivor",
    "note": "This line used to call Mathlib's Nat.exists_infinite_primes. Now the rake supplies the witness itself."},
   {"text": "Remove the multiples of c from the rake (partition each sequence into c sequences, drop those whose constant is a multiple of c, sort)", "lean": "let rs := rs₀.rm.rem c'.p (Nat.Prime.pos hC₀) hsurv", "link": "RakeMap.rem"},
   {"text": "The new candidate is the rake's first term", "lean": "let c₁ := rs.rake.term 0", "link": "Rake.term"},
   {"text": "The new rake lists exactly R c: numbers ≥ 2 with no prime factor up to c", "lean": "intro n; exact r_next_prop (hh₀ n) (hh₁ n)", "link": "r_next_prop"},
   {"text": "Its first term is its least term, because the rake is sorted, so the new candidate is the minimum of R c", "lean": "exact rs.min_term_zero k", "link": "RakeMap.min_term_zero"},
   {"text": "Keep the invariant: the new period is d · c, so its prime factors are those of d (all ≤ p < c) and c itself", "lean": "have hd : rs.rake.d = rs₀.rm.rake.d * rs₀.c := RakeMap.rem_d _ _ _ _", "link": "RakeMap.rem_d"}]}}])

node("instPrimeGenPrimeSieve", "The sieve driver: every PrimeSieve is a prime generator",
 "The sieve's correctness is proved once, for every sieve at the same time: any sieve state whose candidate is the least survivor gives, step by step, the next prime with none skipped. The RakeSieve headlines restate it for the RakeSieve.",
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

For the RakeSieve, α = [RakeSieve](#/node/RakeSieve): its states carry the proofs the driver needs ([the PrimeSieveDriver instance](#/node/RakeSieve.instPrimeSieveDriverRakeSieve)), so `PrimeSieve RakeSieve` is a prime generator. The every-prime headline and the infinitude corollary use it.

### What it adds up to

Starting from [RakeSieve.init](#/node/RakeSieve.init), whose prime is 2, these two facts mean the sieve lists 2, 3, 5, 7, 11, …, *all* the primes, in order. Results.lean now states this directly: [results_rakeSieve_step](#/node/results_rakeSieve_step) for a single step and [results_rakeSieve_emits_every_prime](#/node/results_rakeSieve_emits_every_prime) for "every prime is eventually produced". The second comes from the generic lemma [PrimeGen.exists_iterate_P_eq](#/node/PrimeGen.exists_iterate_P_eq).
""",
 [q("What are the two facts a `PrimeGen` instance must prove?",
    ["the prime is even, and it is less than 100", "no prime lies strictly between the current prime and the next one, and the next prime is bigger", "the state is finite, and it is sorted", "the sieve terminates"], 1,
    "PrimeGen.lean lines 22 and 26: `hP'` (no skipped prime) and `hP_lt` (strict increase)."),
  q("Why can no prime q lie strictly between P and the candidate C?",
    ["because q would be in R P, and C is the least element of R P", "because q would divide C", "because the rake is sorted", "because of `decide`"], 0,
    "`no_skipped_prime` (PrimeSieve.lean lines 133–151): a prime q > P has no prime factor ≤ P (its only prime factor is q), so q ∈ R P, and `hRmin` says C ≤ q."),
  q("Is 'the sieve started at 2 produces every prime' stated as a theorem?",
    ["Yes: `results_rakeSieve_emits_every_prime` in Results.lean", "No, it is only implicit in this instance"], 0,
    "Results.lean lines 35–37, proved from this instance with `PrimeGen.exists_iterate_P_eq`."),
  q("Which sieves does this instance cover?",
    ["only the RakeSieve", "any type with `PrimeSieveState` and `PrimeSieveDriver` instances", "only SimpleGen"], 1,
    "It is stated for an arbitrary α under `variable (α : Type) [PrimeSieveState α] [PrimeSieveDriver α]` (PrimeSieve.lean line 210).")],
 caveats=[
  "This is an `instance`, so it has no name in the source; this site calls it `instPrimeGenPrimeSieve`, the name Lean most likely generates. The exact generated name was not checked (no Lean build).",
  "Completeness ('every prime appears') is stated separately, as `results_rakeSieve_emits_every_prime`."],
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

**Theorem (`results_exists_prime_gt_of_primeGen`, Results.lean lines 40–42). CONDITIONAL.** Let α be any type with a [PrimeGen](#/node/PrimeGen) instance, and g₀ any state. Then for every n there is a prime p > n.

The hypothesis is the `PrimeGen` instance (and a state g₀ to start from). Given those, the proof is elementary and does **not** use Mathlib's infinitude of primes: after k steps the prime has gone up by at least k ([PrimeGen.P_iterate_add_le](#/node/PrimeGen.P_iterate_add_le)), and the first prime is at least 2, so after n + 1 steps it is at least n + 3 > n.

So the honest reading is: *infinitely many primes follows from the existence of a generator whose primes strictly increase*. That moves the work into building a generator. The library has two. [SimpleGen](#/node/SimpleGen) is built with Mathlib's `Nat.exists_infinite_primes`, so using it here would be circular ([simpleGen_exists_prime_gt](#/node/simpleGen_exists_prime_gt)). The RakeSieve is not: each of its steps proves for itself that something survives ([the never-empty headline](#/node/results_rakeSieve_never_empty)). Plugging the RakeSieve in gives the unconditional [corollary](#/node/results_exists_prime_gt_of_rakeSieve).

Only `hP_lt` (strict increase) is used. The docstring of [exists_prime_gt_of_primeGen](#/node/exists_prime_gt_of_primeGen) says why `hP'` alone would not do: a generator stuck on one prime skips nothing.
""",
 [q("What is assumed?",
    ["nothing: it is Euclid's theorem outright", "a `PrimeGen` instance on some type α, and a state g₀", "the Riemann hypothesis", "that the RakeSieve is correct"], 1,
    "The signature is `{α : Type} [PrimeGen α] (g₀ : α) (n : Nat)` (Results.lean line 40)."),
  q("Which field of `PrimeGen` does the proof use?",
    ["`hP'` (no skipped prime)", "`hP_lt` (strict increase)", "both", "neither"], 1,
    "`PrimeGen.P_iterate_add_le` is proved by induction from `hP_lt` (PrimeGen.lean line 62)."),
  q("Why can't `hP'` alone prove infinitude?",
    ["it can", "a generator that stays on the same prime forever satisfies `hP'`", "`hP'` is false for SimpleGen"], 1,
    "If `next g = g`, there is nothing strictly between P g and P g, so `hP'` holds, but only one prime is ever produced. PrimeGen.lean lines 23–24 say this.")],
 caveats=["Conditional on a PrimeGen instance. SimpleGen's instance uses Mathlib's `Nat.exists_infinite_primes`, so it gives only a circular proof. The RakeSieve's instance does not."],
 widgets=[{"type": "walkthrough", "title": "The proof (PrimeGen.lean, lines 68-74)", "config": {"steps": [
   {"text": "Take k = n + 1 steps", "lean": "let k := n + 1"},
   {"text": "After k steps the prime has grown by at least k", "lean": "PrimeGen.P_iterate_add_le g₀ k", "link": "PrimeGen.P_iterate_add_le"},
   {"text": "The starting prime is at least 2 (it is prime)", "lean": "Nat.Prime.two_le (P g₀).prop"},
   {"text": "Offer the prime after k steps as the witness; it is prime because generator values are primes", "lean": "refine ⟨P (next^[k] g₀), (P (next^[k] g₀)).prop, ?_⟩", "link": "NPrime"},
   {"text": "Arithmetic: 2 + (n + 1) > n", "lean": "omega"}]}}])

node("simpleGen_exists_prime_gt", "Reference only: Euclid via the brute-force generator (circular)",
 "Kept as a reference specification, not as evidence. The 'simple' generator finds each next prime by asking Mathlib for a prime above it, so it assumes the very theorem it proves.",
 r"""
## Plain English

**Theorem (`simpleGen_exists_prime_gt`, SimpleGen.lean lines 62–63). CIRCULAR.** For every n there is a prime p > n.

Its statement is the same as the [corollary](#/node/results_exists_prime_gt_of_rakeSieve). The proof runs the general fact [exists_prime_gt_of_primeGen](#/node/exists_prime_gt_of_primeGen) on [SimpleGen.start](#/node/SimpleGen.start), the brute-force generator. Its next prime is `Nat.find` of "a prime greater than p" ([min_prime_gt](#/node/min_prime_gt)), and that prime exists only because Mathlib's `Nat.exists_infinite_primes` says so ([ex_prime_gt](#/node/ex_prime_gt), SimpleGen.lean line 19). So this is Euclid proved from Euclid.

PR #5 moved it out of Results.lean, where it was `results_exists_prime_gt_of_simpleGen`, into SimpleGen.lean, which the RakeSieve does not import. It stays for two reasons:

- **As a reference spec.** It shows that the obvious specification, "the next prime is the least prime above this one", satisfies the [PrimeGen](#/node/PrimeGen) interface. The RakeSieve can be compared against it, and the `#guard` on SimpleGen.lean line 57 checks its first ten primes by evaluation.
- **As the control for the no-Euclid check.** NoEuclidCheck.lean must *find* `Nat.exists_infinite_primes` in this theorem's dependencies. A broken checker that saw nothing would fail here instead of passing the RakeSieve headlines silently.
""",
 [q("How does `SimpleGen` find the next prime?",
    ["by trial division", "as the least prime greater than p, via `Nat.find`", "with the rake"], 1,
    "`min_prime_gt n` uses `Nat.find (ex_prime_gt n)` (SimpleGen.lean lines 24–28)."),
  q("Is this an independent proof that there are infinitely many primes?",
    ["Yes", "No: building SimpleGen uses `Nat.exists_infinite_primes`"], 1,
    "`ex_prime_gt` calls `Nat.exists_infinite_primes` (SimpleGen.lean line 19)."),
  q("Why is it kept at all?",
    ["as a reference spec for PrimeGen, and as the control case that the no-Euclid check must flag", "because the RakeSieve needs it", "by accident"], 0,
    "NoEuclidCheck.lean ends with `#assert_uses_euclid simpleGen_exists_prime_gt`."),
  q("What is SimpleGen's first prime?",
    ["1", "2", "3"], 1, "`SimpleGen.start := { p := ⟨2, Nat.prime_two⟩, … }` (SimpleGen.lean line 39).")],
 caveats=["Circular as a proof of Euclid: it assumes Mathlib's `Nat.exists_infinite_primes`. It checks the interface, not number theory, and is not on the RakeSieve's headline path."],
 widgets=[{"type": "walkthrough", "title": "The proof (SimpleGen.lean, lines 62-63)", "config": {"steps": [
   {"text": "Start the brute-force generator at 2", "lean": "SimpleGen.start", "link": "SimpleGen.start"},
   {"text": "It is a PrimeGen: its next prime is the least prime above the current one, which exists by Mathlib's Euclid", "link": "instPrimeGenSimpleGen"},
   {"text": "Apply the general fact about prime generators", "lean": "exists_prime_gt_of_primeGen", "link": "exists_prime_gt_of_primeGen"}]}}])

node("results_three_mem_R_two", "3 survives sieving by 2",
 "A fact this small is a headline because it is the sieve's base case: after crossing out multiples of 2, the number 3 is still there. Lean checks it by computation (`decide`), not by reasoning.",
 PLAIN_R + r"""**Theorem (`results_three_mem_R_two`, Results.lean lines 11–12).** 3 ∈ R 2: the number 3 is at least 2 and is not divisible by any prime q ≤ 2.

[R](#/node/R) P is the set of numbers that survive a sieve once every prime up to P has crossed out its multiples. So R 2 is the odd numbers from 3 up, and this theorem says 3 is one of them.

Why it matters: the RakeSieve starts with prime p = 2 and candidate c = 3 ([RakeSieve.init](#/node/RakeSieve.init)). Every sieve state must prove that its candidate lies in R p; for the start state that proof is this theorem (RakeSieve.lean line 53). It was moved out of `RakeSieve.init` into PrimeSieve.lean so that any sieve can reuse it (issue #3).
""",
 [q("Which set is R 2?",
    ["all numbers ≥ 2", "the odd numbers ≥ 3", "the primes", "the even numbers"], 1,
    "R 2 = { n | n ≥ 2 ∧ ∀ q ≤ 2, q prime → ¬ q ∣ n }. The only prime ≤ 2 is 2, so these are the n ≥ 2 that are odd."),
  q("How does Lean check `¬ 2 ∣ 3`?",
    ["`native_decide`", "`decide` (evaluated by the kernel)", "an axiom"], 1,
    "PrimeSieve.lean line 27: `decide`. That is ordinary kernel evaluation, with no extra trust."),
  q("Where is this fact used?",
    ["As the base case for RakeSieve.init's proof that its candidate 3 is in R 2", "Nowhere", "In Main.lean only"], 0,
    "RakeSieve.lean line 53: `simpa [p] using three_mem_R_two`.")],
 widgets=[{"type": "walkthrough", "title": "The proof (PrimeSieve.lean, lines 19-27)", "config": {"steps": [
   {"text": "3 ≥ 2, by computation", "lean": "refine ⟨by decide, ?_⟩"},
   {"text": "Any prime q ≤ 2 is at least 2, so q = 2", "lean": "have := Nat.Prime.two_le hq'"},
   {"text": "2 does not divide 3, by computation", "lean": "decide"}]}}])

node("results_three_le_of_mem_R_two", "Nothing in R 2 is smaller than 3",
 "With the previous theorem this pins down the sieve's first candidate: 3 is the *least* survivor after sieving by 2. That is exactly what the sieve needs to know 3 is the next prime.",
 PLAIN_R + r"""**Theorem (`results_three_le_of_mem_R_two`, Results.lean lines 14–15).** Every r ∈ R 2 satisfies 3 ≤ r.

Together with [3 ∈ R 2](#/node/results_three_mem_R_two), this says 3 is the minimum of [R](#/node/R) 2. The sieve's start state needs both: its candidate must be in R p (`hCinR`) and below everything else in R p (`hRmin`). See the [RakeSieve](#/node/RakeSieve) structure and RakeSieve.lean lines 51–56.

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
    "`hRmin : ∀ r ∈ R p, c ≤ r` (RakeSieve.lean line 12); RakeSieve.lean line 56 uses this theorem.")],
 widgets=[{"type": "walkthrough", "title": "The proof (PrimeSieve.lean, lines 30-37)", "config": {"steps": [
   {"text": "Suppose r ∈ R 2 but r < 3", "lean": "by_contra h"},
   {"text": "Since r ≥ 2, r = 2", "lean": "have r2 : r = 2 := by omega"},
   {"text": "But R 2 says the prime 2 does not divide r = 2, which is false", "lean": "have := hrr 2 (by omega) Nat.prime_two"}]}}])
