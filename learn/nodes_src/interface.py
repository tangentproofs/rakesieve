# Nodes for the generic interface: primes as a type, prime generators, the residue set R, and the
# generic sieve driver (PrimeGen.lean, PrimeSieve.lean).
from _terms import PLAIN_R
NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}

node("NPrime", "NPrime: a natural number packaged with a proof that it is prime",
 "A value of this type cannot be a non-prime. Every prime a generator hands out carries its own certificate, so 'the output is prime' never has to be proved again.",
 r"""
## Plain English

`NPrime` is the type `{ n : Nat // Nat.Prime n }` (PrimeGen.lean line 7): a pair of a natural number and a proof that it is prime. Lean can only build one by supplying the proof, for example `⟨2, Nat.prime_two⟩`.

The library adds conveniences: two `NPrime`s are equal when their numbers are ([NPrime.eq_iff](#/node/NPrime.eq_iff)), they print as their number, and they coerce to `Nat` (PrimeGen.lean lines 9–12).

Because [PrimeGen](#/node/PrimeGen)'s `P` returns an `NPrime`, every generator's output is prime *by its type*.
""",
 [q("Can you build an `NPrime` holding 4?", ["Yes", "No: you would need a proof of `Nat.Prime 4`, which is false"], 1,
    "An `NPrime` is a subtype value: the number together with a proof that it is prime."),
  q("How is the number 2 packaged as an `NPrime` in this library?", ["`⟨2, Nat.prime_two⟩`", "`NPrime.mk 2`", "`2 : NPrime` with no proof"], 0,
    "See `SimpleGen.start` (PrimeGen.lean line 62) and `RakeSieve.init` (RakeSieve.lean line 22)."),
  q("What does `(P g).prop` give you, for a generator state g?", ["the number", "a proof that the number is prime", "the next state"], 1,
    "`.prop` is the proof component of a subtype value; `exists_prime_gt_of_primeGen` uses it (PrimeGen.lean line 117).")])

node("PrimeGen", "PrimeGen: what it means to generate primes in order",
 "The spec of a prime generator is only two lines, 'no prime is skipped' and 'the prime goes up', and the second line was added only in September 2026 because the first alone allows a generator stuck on one prime.",
 r"""
## Plain English

A `PrimeGen` on a type α of states (PrimeGen.lean lines 19–26) provides:

- `P : α → NPrime`, the prime at the current state ([NPrime](#/node/NPrime));
- `next : α → α`, the step to the next state;
- `hP'`: for every state g, **no prime q satisfies P g < q < P (next g)**;
- `hP_lt`: for every state g, **P g < P (next g)**.

So, run from a state whose prime is p, a generator lists the primes from p upward, in order, with none skipped. The two conditions are independent: `hP'` alone allows `next g = g`, and `hP_lt` alone allows skipping.

The start state is deliberately not part of the class (the docstring explains: use `primes g₀ n` with an explicit start such as [SimpleGen.start](#/node/SimpleGen.start)). Consequently a `PrimeGen` does not promise to start at 2; that is a property of the particular start state.
""",
 [q("Which two properties does `PrimeGen` require?",
    ["output is prime; output is odd", "no prime strictly between consecutive outputs; outputs strictly increase", "the state is finite; next terminates"], 1,
    "`hP'` and `hP_lt` (PrimeGen.lean lines 23 and 26). Primality of the output is built into the type `NPrime`."),
  q("Does `PrimeGen` say the generator starts at 2?", ["Yes", "No, the start state is chosen separately"], 1,
    "There is no `init` field; the docstring says it was intentionally left out (PrimeGen.lean lines 16–18)."),
  q("A 'generator' with `next g = g` satisfies which condition?", ["`hP'` only", "`hP_lt` only", "both", "neither"], 0,
    "There is no prime strictly between p and p, so `hP'` holds, but `p < p` fails, so `hP_lt` does not.")])

node("nosk'", "nosk': no prime strictly between P and C",
 "The apostrophe-named one-liner is the heart of 'next prime': it is the claim that nothing was skipped, and a sieve step is only allowed to run once it has been proved.",
 r"""
## Plain English

`nosk' P C` (PrimeSieve.lean line 5) abbreviates **¬ ∃ q, q is prime ∧ P < q ∧ q < C**: there is no prime strictly between P and C. "nosk" is short for "no skip".

[PrimeSieveState](#/node/PrimeSieveState)'s `next` takes a proof of `nosk' (P s) (C s)` as an argument. In other words a sieve step may only be taken once someone has proved that the candidate C is the very next prime after P. The generic driver supplies that proof ([no_skipped_prime](#/node/no_skipped_prime)).
""",
 [q("Is `nosk' 3 5` true?", ["Yes: 4 is the only number strictly between, and it is not prime", "No"], 0, "The only q with 3 < q < 5 is 4, which is not prime."),
  q("Is `nosk' 7 13` true?", ["Yes", "No: 11 is a prime strictly between"], 1, "11 is prime and 7 < 11 < 13."),
  q("Does `nosk' P C` say C is prime?", ["Yes", "No, it only says no prime lies strictly between"], 1, "Primality of C is a separate argument `hC` of `PrimeSieveState.next`.")])

node("R", "R P, the residue: the numbers that survive sieving by every prime up to P",
 "R stands for residue: what is left after sieving. The whole sieve is driven by this one set. Its least element is always the next prime, and sieving by a new prime p is exactly the step from R (previous prime) to R p.",
 r"""
## Plain English

**R stands for *residue*.** `R P = { n | n ≥ 2 ∧ ∀ q ≤ P, q prime → ¬ q ∣ n }` (PrimeSieve.lean line 16); the comment there reads "the residue, or remaining nats". In words: the numbers from 2 up that no prime ≤ P divides. These are what is left after the sieve of Eratosthenes has crossed out the multiples of every prime up to P.

Examples: R 2 = {3, 5, 7, 9, 11, …} (odd numbers ≥ 3); R 3 = {5, 7, 11, 13, 17, 19, 23, 25, …}.

Three facts make it useful:
- everything in R P is bigger than P ([r_gt_p](#/node/r_gt_p));
- the least element of R P is the next prime after P ([c_prime](#/node/c_prime), [no_skipped_prime](#/node/no_skipped_prime));
- if p₁ is the next prime after p₀, then R p₁ = R p₀ minus the multiples of p₁ ([r_next](#/node/r_next)).

Note that R P is defined for any number P, prime or not, and contains composites (25 ∈ R 3).
""",
 [q("Is 9 in R 2?", ["Yes", "No"], 0, "9 ≥ 2 and the only prime ≤ 2 is 2, which does not divide 9."),
  q("Is 9 in R 3?", ["Yes", "No"], 1, "3 ≤ 3 is prime and divides 9."),
  q("What is the least element of R 5?", ["6", "7", "25"], 1, "R 5 drops multiples of 2, 3 and 5; 6 is a multiple of 2, so the least survivor is 7, the next prime."),
  q("Does R P contain only primes?", ["Yes", "No, e.g. 25 ∈ R 3"], 1, "25 = 5·5 has no prime factor ≤ 3.")])

node("PrimeSieveState", "PrimeSieveState: a sieve's state, its prime, its candidate, its step",
 "The step function demands proofs as inputs: you may only advance a sieve after proving the candidate is prime and nothing was skipped. The interface makes an unjustified step impossible to write.",
 PLAIN_R + r"""A `PrimeSieveState` on a type α (PrimeSieve.lean lines 6–11) provides, for each state s:

- `P s : NPrime`, the latest prime found ([NPrime](#/node/NPrime));
- `C s : Nat`, the candidate for the next prime;
- `next s hC hN : α`, one sieve step, which needs a proof `hC` that C s is prime and a proof `hN : nosk' (P s) (C s)` that no prime lies strictly between ([nosk'](#/node/nosk'));
- `hNext`: after the step, the new prime is the old candidate (P s' = C s) and the candidate grew (C s' > C s).

On its own this says nothing about whether C really is the next prime. That job belongs to [PrimeSieveDriver](#/node/PrimeSieveDriver), which ties C to the set [R](#/node/R).
""",
 [q("What does `next` require besides the state?", ["nothing", "proofs that C is prime and that no prime lies strictly between P and C", "the list of all primes so far"], 1,
    "`next (s:α) (hC: Nat.Prime (C s)) (hN: nosk' (P s) (C s)): α` (PrimeSieve.lean line 9)."),
  q("After one step, what is the new prime P?", ["the old P + 1", "the old candidate C", "the new candidate"], 1, "`hNext` gives `P s' = C s`."),
  q("Does `PrimeSieveState` alone guarantee C is the least survivor?", ["Yes", "No, that is `PrimeSieveDriver`'s `hRmin`"], 1,
    "`PrimeSieveDriver` adds `hCinR` and `hRmin` (PrimeSieve.lean lines 124–126).")])

node("PrimeSieveDriver", "PrimeSieveDriver: the candidate is the least survivor",
 "Two lines, 'C is in the residue R P' (what survives sieving up to P) and 'C is below everything in R P', are all a sieve needs to promise. From them alone the library proves C is prime and nothing was skipped, for every sieve.",
 PLAIN_R + r"""A `PrimeSieveDriver` for a sieve state type α (PrimeSieve.lean lines 124–126) adds two facts to [PrimeSieveState](#/node/PrimeSieveState), for every state g:

- `hCinR`: the candidate C g is in [R](#/node/R) (P g), i.e. it survived sieving by every prime up to P g;
- `hRmin`: C g ≤ n for every n in R (P g), i.e. it is the *least* survivor.

The docstring describes a prime sieve as something that models the numbers > 1 coprime to the known primes, repeatedly takes the minimum as the next prime, and then eliminates its multiples. These two fields are the formal version of "takes the minimum".

From them the library derives [c_prime](#/node/c_prime) (C is prime), [no_skipped_prime](#/node/no_skipped_prime) and [c_gt_p](#/node/c_gt_p), which is all that [nextState](#/node/nextState) needs.
""",
 [q("Which two facts does a `PrimeSieveDriver` supply?", ["C is prime; C is odd", "C ∈ R P; C ≤ every element of R P", "P is prime; P < C"], 1, "`hCinR` and `hRmin`."),
  q("Does a driver have to prove that C is prime?", ["Yes", "No, `c_prime` derives it from `hCinR` and `hRmin`"], 1, "PrimeSieve.lean lines 173–193."),
  q("For the RakeSieve, where do `hCinR` and `hRmin` come from?", ["They are fields of the `RakeSieve` structure itself", "From Mathlib", "From `decide`"], 0,
    "The `RakeSieve` structure carries `hCinR` and `hRmin` (RakeSieve.lean lines 11–12); the driver instance just reads them (lines 130–132).")])

node("PrimeSieve", "PrimeSieve: a wrapper that turns a sieve state into a generator",
 "It holds nothing but the state. The wrapper exists only so Lean's instance search can attach one generic proof, 'this is a prime generator', to every sieve at once.",
 r"""
## Plain English

`PrimeSieve α` is a structure with one field, `state : α` (PrimeSieve.lean lines 211–212), for a type α that has [PrimeSieveState](#/node/PrimeSieveState) and [PrimeSieveDriver](#/node/PrimeSieveDriver) instances (the section `variable` line, PrimeSieve.lean line 210).

Its step is [PrimeSieve.next](#/node/PrimeSieve.next), which runs the sieve once with the proofs supplied automatically, and the [driver instance](#/node/instPrimeGenPrimeSieve) makes it a [PrimeGen](#/node/PrimeGen). The main theorem uses `PrimeSieve RakeSieve` with state `RakeSieve.init`.
""",
 [q("How many fields does `PrimeSieve α` have?", ["one, `state`", "two", "four"], 0, "PrimeSieve.lean line 212."),
  q("Why wrap the state instead of making α itself a `PrimeGen`?", ["so a single generic instance can cover every sieve type without overlapping other instances", "for speed", "because Lean forbids it"], 0,
    "`instance : PrimeGen (PrimeSieve α)` is proved once for all α with the two sieve classes."),
  q("Which classes must α have?", ["`PrimeSieveState` and `PrimeSieveDriver`", "`PrimeGen`", "`Ord`"], 0, "PrimeSieve.lean line 210.")],
 caveats=["The site's scanner reads section `variable`s by hand for this declaration (PrimeSieve.lean line 210); it does not run Lean."])
