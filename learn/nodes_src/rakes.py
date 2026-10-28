# Nodes for the data structures: arithmetic sequences, rakes and rake maps (ASeq.lean, Rake.lean, RakeMap.lean),
# plus the executable demo.
NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}

node("ASeq", "ASeq: an arithmetic sequence k + d·n",
 "**The surprise:** the basic object is just two numbers. The odd numbers are (1, 2), all numbers ≥ 2 are (2, 1), and the whole sieve is built by composing such pairs.",
 r"""
## Plain English

An `ASeq` (ASeq.lean lines 6–9) is a pair: a constant k and a step d. It stands for the sequence k, k + d, k + 2d, … ; its n-th term is [ASeq.term](#/node/ASeq.term) s n = k + d·n. [aseq](#/node/aseq) k d builds one.

Examples from the file: `nats = aseq 0 1`, `evens = aseq 0 2`, `odds = aseq 1 2` (ASeq.lean lines 40–42), checked with `#guard` on their first ten terms.

ASeq.lean also proves that composing sequences composes their terms (`ASeq.compose_def`), but the rake code works with constants and a shared step directly.
""",
 [q("Which ASeq lists 3, 5, 7, 9, …?", ["k = 3, d = 2", "k = 2, d = 3", "k = 1, d = 2"], 0, "The sequence 3 + 2n."),
  q("What is the 4th term (n = 4) of k = 5, d = 6?", ["29", "24", "35"], 0, "5 + 6·4 = 29."),
  q("Can d be 0?", ["Yes: then every term equals k", "No, the type forbids it"], 0, "`d : Nat` allows 0; `Rake.partition` comments on why d = 0 is awkward.")])

node("aseq", "aseq k d: build the sequence k + d·n",
 "**The surprise:** a one-line constructor, marked @[simp] so Lean unfolds it automatically in proofs.",
 r"""
## Plain English

`aseq k d := ASeq.mk k d` (ASeq.lean line 35): the [ASeq](#/node/ASeq) with constant k and step d. [Rake.term](#/node/Rake.term) uses it to read a term out of a rake.
""",
 [q("`aseq 1 2` is…", ["the odd numbers", "the even numbers"], 0, "The sequence 1 + 2n."),
  q("Why mark it @[simp]?", ["so `simp` unfolds it automatically", "for speed at runtime"], 0, "A simp lemma rewrites `aseq k d` to `ASeq.mk k d`."),
  q("Its arguments are…", ["constant, then step", "step, then constant"], 0, "`aseq (k:Nat) (d:Nat)`.")])

node("ASeq.term", "ASeq.term: the n-th term, k + d·n",
 "**The surprise:** an ASeq can be used as a function (s n) because of a coercion that points at this one line.",
 r"""
## Plain English

`term s n = s.k + s.d * n` (ASeq.lean line 45). A `CoeFun` instance (line 48) lets you write `s n` for it. See [ASeq](#/node/ASeq).
""",
 [q("`(aseq 0 2).term 10` is", ["20", "12", "10"], 0, "0 + 2·10, checked by the `#guard` on ASeq.lean line 50."),
  q("Is term 0 always k?", ["Yes", "No"], 0, "k + d·0 = k."),
  q("Do terms ever decrease?", ["No, d·n grows with n (or stays fixed if d = 0)", "Yes"], 0, "d is a natural number.")])

node("List.Sorted", "List.Sorted: a local stand-in for 'sorted by r'",
 "**The surprise:** the library defines its own `List.Sorted` as `List.Pairwise`, a small shim kept so the code survives Mathlib renaming its sorted-list API.",
 r"""
## Plain English

`List.Sorted r l := l.Pairwise r` (Rake.lean line 11): every earlier element is related to every later one. With r = (<), it means strictly increasing. [Rake](#/node/Rake) uses it for its constant list.
""",
 [q("Is [2, 5, 9] `Sorted (· < ·)`?", ["Yes", "No"], 0, "Each pair in order satisfies <."),
  q("Is [2, 2, 3] `Sorted (· < ·)`?", ["Yes", "No"], 1, "2 < 2 fails."),
  q("Why define it locally?", ["it is an abbreviation for `List.Pairwise`, kept stable across Mathlib versions", "Mathlib has no lists"], 0, "Rake.lean lines 9–13.")])

node("Rake", "Rake: several arithmetic sequences sharing one step",
 "**The surprise:** a rake is a picture of a residue system: the constants are the 'teeth' and the shared step d is the spacing, so {3, 5} with d = 6 lists everything coprime to 6 that is ≥ 3.",
 r"""
## Plain English

A `Rake` (Rake.lean lines 15–22) has a step d and a non-empty list ks of constants. It stands for the union of the sequences k + d·n for k in ks. Its terms are listed round-robin by [Rake.term](#/node/Rake.term).

Fields `sorted`, `hsort`, `huniq` record whether ks is known to be strictly increasing and duplicate-free (a Bool flag with proofs), and `hsize` says ks is non-empty.

Examples: [Rake.ge2](#/node/Rake.ge2) = {d = 1, ks = [2]} is every number ≥ 2. After removing multiples of 2 and 3 the README shows the rake {5, 7} with step 6, and after 5 the rake with step 30 and eight constants 7, 11, 13, 17, 19, 23, 29, 31.

Why "rake": each sieve step multiplies the step d by the new prime p and the number of teeth by p − 1, which is why the README calls it laughably inefficient: 1, 2, 8, 48, 480, 5760, … sequences.
""",
 [q("Which numbers does the rake {d = 6, ks = [5, 7]} produce?", ["5, 7, 11, 13, 17, 19, …", "5, 6, 7, 8, …", "6, 12, 18, …"], 0, "5 + 6n and 7 + 6n."),
  q("What does `hsize` guarantee?", ["at least one constant", "the rake is sorted", "d > 0"], 0, "`hsize : 0 < ks.length`."),
  q("Is the README's growth table (1, 2, 8, 48, …) proved in Lean?", ["No, it is documentation", "Yes"], 0, "No theorem counts the constants after k steps.")],
 caveats=["The README's growth figures and efficiency remarks are not formalized."])

node("Rake.ge2", "Rake.ge2: every number from 2 up",
 "**The surprise:** the sieve's raw material is one sequence, 2 + 1·n.",
 r"""
## Plain English

`ge2 := { d := 1, ks := [2] }` (Rake.lean line 28): the [Rake](#/node/Rake) whose only sequence is 2 + n. [RakeMap.rm_ge2](#/node/RakeMap.rm_ge2) proves its terms are exactly the numbers ≥ 2.
""",
 [q("What are its first terms?", ["2, 3, 4, 5, …", "2, 4, 6, …"], 0, "The sequence 2 + n."),
  q("Its step d is", ["1", "2"], 0, "See Rake.lean line 28."),
  q("Is it sorted?", ["Yes, by default", "No"], 0, "`sorted` defaults to true with automatic proofs for a one-element list.")])

node("Rake.term", "Rake.term: read the n-th term round-robin",
 "**The surprise:** terms are not listed in increasing order in general; they cycle through the teeth. Only the first term is guaranteed to be the smallest, and that is all the sieve needs.",
 r"""
## Plain English

`r.term n = ks[n mod q] + d·(n / q)` where q = ks.length (Rake.lean lines 32–35). So term 0, 1, …, q−1 are the constants themselves, then each constant plus d, and so on.

[Rake.term_iff](#/node/Rake.term_iff) restates it: m is a term exactly when m = k + x·d for some k in ks and some x. For a sorted rake, term 0 is the smallest ([sorted_min_term_zero](#/node/Rake.sorted_min_term_zero)), which is how the RakeSieve picks its candidate.
""",
 [q("For {d = 6, ks = [5, 7]}, what is term 3?", ["13", "11", "17"], 0, "3 mod 2 = 1 → constant 7; 3 / 2 = 1 → 7 + 6 = 13."),
  q("Are terms always increasing in n?", ["No; for example if a constant exceeds d the order can saw-tooth", "Yes"], 0, "Rake.lean lines 180–184 say so."),
  q("Which term is the minimum of a sorted rake?", ["term 0", "the last constant"], 0, "`sorted_min_term_zero`.")])

node("Rake.term_iff", "Which numbers a rake produces",
 "**The surprise:** most of the proof is index arithmetic with mod and div, to show the round-robin order hits every k + x·d exactly where expected.",
 r"""
## Plain English

**Theorem (`Rake.term_iff`, Rake.lean lines 48–99).** m = r.term n for some n **iff** m = k + x·d for some k ∈ ks and some x. This turns questions about the term function into questions about the constants list, and every later rake proof uses it. See [Rake.term](#/node/Rake.term).
""",
 [q("Given k = ks[i] and x, which n gives term n = k + x·d?", ["n = i + x·q", "n = x", "n = i·x"], 0, "Rake.lean line 78 builds n := (i mod q) + x·q."),
  q("Does the theorem depend on sortedness?", ["No", "Yes"], 0, "It holds for any rake, sorted or not."),
  q("Why is it useful?", ["it reduces term questions to questions about ks", "it computes primes"], 0, "Used in the partition and rem proofs.")])

node("Rake.sorted_min_term_zero", "In a sorted rake, the first term is the smallest",
 "**The surprise:** even though a rake's terms can come out of order, this one fact survives every case, and it is the only ordering fact the sieve needs.",
 r"""
## Plain English

**Theorem (`Rake.sorted_min_term_zero`, Rake.lean lines 185–196).** If the rake is sorted, r.term 0 ≤ r.term n for every n.

term 0 is the first constant plus 0; any other term is some constant (≥ the first, by sortedness) plus a multiple of d. [RakeMap.min_term_zero](#/node/RakeMap.min_term_zero) restates it for rake maps, and [RakeSieve.next](#/node/RakeSieve.next) uses it to prove the new candidate is the least survivor.
""",
 [q("Why is the first constant the smallest constant?", ["the list is strictly increasing", "it is 2"], 0, "That is the field `hsort`."),
  q("Does the theorem need d > 0?", ["No", "Yes"], 0, "Adding d·x ≥ 0 never decreases."),
  q("Where is it used in the sieve?", ["to show the candidate is ≤ every survivor", "to show it is prime"], 0, "RakeSieve.lean line 111.")])

node("Rake.partition", "Rake.partition: split each sequence into j sequences",
 "**The surprise:** the rake grows j-fold but produces exactly the same numbers; it only changes how they are grouped, so that divisibility by j can be read off the constants.",
 r"""
## Plain English

`r.partition j` (Rake.lean lines 232–239) replaces step d by d·j and the constants by k + i·d for every constant k and i = 0, …, j−1. Each old sequence k + d·n splits into j sequences by n mod j.

[partition_term_iff](#/node/Rake.partition_term_iff) proves the terms are unchanged. After partitioning by j, the step d·j is a multiple of j, so a sequence k + d·j·n is all multiples of j if j ∣ k, and none otherwise. That is what makes [Rake.rem](#/node/Rake.rem) work.

The result is marked `sorted := false`.
""",
 [q("Partition {d = 2, ks = [3]} by 3. What do you get?", ["d = 6, ks = [3, 5, 7]", "d = 3, ks = [3]", "d = 6, ks = [3]"], 0, "3 + 0·2, 3 + 1·2, 3 + 2·2 with step 6 (the README's example)."),
  q("How many constants after partitioning q constants by j?", ["j·q", "q + j", "q"], 0, "`length_partition`."),
  q("Why must j be positive?", ["j = 0 would leave no sequences", "for speed"], 0, "The docstring, Rake.lean lines 227–231.")])

node("Rake.partition_term_iff", "Partitioning keeps exactly the same terms",
 "**The surprise:** the 'easy' direction, that old terms survive the split, is the long one, a calc chain of mod and div rewrites over nearly 60 lines.",
 r"""
## Plain English

**Theorem (`Rake.partition_term_iff`, Rake.lean lines 340–344).** n is a term of r.partition j iff n is a term of r. It combines `partition_term_same` (Rake.lean lines 248–278) and `partition_term_keep` (Rake.lean lines 280–338). See [Rake.partition](#/node/Rake.partition).
""",
 [q("Does partition add or remove numbers?", ["neither", "adds", "removes"], 0, "Same set of terms."),
  q("Which half is longer in the source?", ["`partition_term_keep`", "`partition_term_same`"], 0, "Rake.lean lines 280–338."),
  q("Is it an iff for every n?", ["Yes", "Only for primes"], 0, "`∀n, … ↔ …`.")])

node("Rake.rem", "Rake.rem: remove all multiples of j",
 "**The surprise:** removal never looks at a single number. It partitions by j and drops the sequences whose constant is a multiple of j: one test per sequence covers infinitely many numbers.",
 r"""
## Plain English

`r.rem hj` (Rake.lean lines 353–362, with r, j and hj from the section `variable` on line 350) partitions r by j ([Rake.partition](#/node/Rake.partition)) and keeps only the constants k with j ∤ k. If nothing is left it returns the dummy rake `zer`.

Three theorems pin down what it does, assuming the rake has at least one term not divisible by j ([HasNonMultiple](#/node/Rake.HasNonMultiple)):
- [rem_drop](#/node/Rake.rem_drop): no multiple of j is a term afterwards;
- [rem_keep](#/node/Rake.rem_keep): every non-multiple term of r is still a term;
- [rem_same](#/node/Rake.rem_same): no new terms appear.

A comment notes that a smarter version would use gcd(d, j), but in the sieve j is always a new prime, so it makes no difference.
""",
 [q("After partitioning by j, why does j ∣ k decide a whole sequence?", ["the step d·j is a multiple of j, so k + d·j·n ≡ k mod j", "because k is prime"], 0, "So either every term or no term is a multiple of j."),
  q("What happens if every constant is a multiple of j?", ["it returns the placeholder rake `zer`", "it fails to compile"], 0, "Rake.lean line 361."),
  q("Why do the theorems assume `HasNonMultiple`?", ["to rule out the `zer` case", "for speed"], 0, "`rem_def` (Rake.lean lines 370–409) shows the zer case cannot happen under that assumption.")])

node("Rake.HasNonMultiple", "HasNonMultiple: some term is not a multiple of j",
 "**The surprise:** this innocent hypothesis is where Euclid enters the sieve: proving it at each step is what needs Mathlib's infinitude of primes.",
 r"""
## Plain English

`HasNonMultiple r j := ∃ n, ¬ j ∣ n ∧ ∃ m, r.term m = n` (Rake.lean line 364): the rake r has a term not divisible by j. [Rake.rem](#/node/Rake.rem)'s theorems need it; [RakeMap.rem](#/node/RakeMap.rem) asks for it as an argument; [RakeSieve.next](#/node/RakeSieve.next) proves it with a prime from `Nat.exists_infinite_primes`.
""",
 [q("Does {d = 2, ks = [4]} have a non-multiple of 2?", ["No", "Yes"], 0, "4 + 2n is always even."),
  q("Does {d = 2, ks = [3]} have a non-multiple of 3?", ["Yes, e.g. 5", "No"], 0, "5 = 3 + 2·1."),
  q("How does the RakeSieve prove it?", ["with a prime above c from Mathlib", "by `decide`"], 0, "RakeSieve.lean line 71.")])

node("Rake.rem_drop", "After rem, no multiple of j remains",
 "**The surprise:** the proof is pure divisibility: a surviving constant k has j ∤ k, and j divides d·j·x, so j cannot divide k + d·j·x.",
 r"""
## Plain English

**Theorem (`Rake.rem_drop`, Rake.lean lines 411–431).** If r has a non-multiple of j, then no multiple of j is a term of r.rem. See [Rake.rem](#/node/Rake.rem).
""",
 [q("Which terms does it rule out?", ["multiples of j", "primes", "terms below j"], 0, "`∀n, j∣n → ¬(∃m, r'.term m = n)`."),
  q("Why is the HasNonMultiple hypothesis needed?", ["otherwise rem returns `zer`, whose only term 0 is a multiple of j", "it is not needed"], 0, "`zer = {d := 0, ks := [0]}`."),
  q("Is it the 'drop' or 'keep' half?", ["drop", "keep"], 0, "As the name says: it drops the multiples.")])

node("Rake.rem_keep", "After rem, every non-multiple survives",
 "**The surprise:** this is the half that makes the sieve *complete*: nothing that should survive is lost, which is what keeps every prime in play.",
 r"""
## Plain English

**Theorem (`Rake.rem_keep`, Rake.lean lines 433–457).** If n is a term of r and j ∤ n, then n is a term of r.rem. It uses [partition_term_iff](#/node/Rake.partition_term_iff) to find n in the partitioned rake and checks that its constant passes the filter. See [Rake.rem](#/node/Rake.rem).
""",
 [q("What does it preserve?", ["every term not divisible by j", "every term"], 0, "`¬j∣n → (∃m, r.term m = n) → (∃m', r'.term m' = n)`."),
  q("Does it need HasNonMultiple?", ["No (it builds one from n itself)", "Yes"], 0, "Rake.lean line 442: `have hnm: HasNonMultiple r j := by use n`."),
  q("Why is it important for the sieve?", ["no prime is lost", "it speeds things up"], 0, "Primes above the current one are never multiples of it.")])

node("Rake.rem_same", "rem adds no new terms",
 "**The surprise:** the soundness half: whatever the reshuffling, rem only ever removes.",
 r"""
## Plain English

**Theorem (`Rake.rem_same`, Rake.lean lines 459–467).** Assuming HasNonMultiple, every term of r.rem is a term of r. See [Rake.rem](#/node/Rake.rem).
""",
 [q("Direction?", ["terms of r.rem ⊆ terms of r", "terms of r ⊆ terms of r.rem"], 0, "`(∃m', r'.term m' = n) → (∃m, r.term m = n)`."),
  q("Together with drop and keep, terms of r.rem are exactly…", ["the terms of r not divisible by j", "the primes"], 0, "That is what `RakeMap.rem` records."),
  q("Is HasNonMultiple assumed?", ["Yes", "No"], 0, "Otherwise `zer` produces 0, which need not be a term of r.")])

node("RakeMap", "RakeMap: a rake together with the property its terms have",
 "**The surprise:** the docstring calls it a '1-to-1 mapping', but the Lean only says the rake's terms are exactly the numbers with the property; one-to-one is never stated or needed.",
 r"""
## Plain English

A `RakeMap pred` (RakeMap.lean lines 6–9) is a [Rake](#/node/Rake) with two proofs:

- `hbij`: **pred n ↔ n is a term of the rake**, for every n;
- `hord`: the rake is sorted.

So the rake is an exact, sorted description of the set { n | pred n }. Operations: [RakeMap.rem](#/node/RakeMap.rem) removes multiples of j and updates pred to `pred n ∧ ¬ j ∣ n`; [min_term_zero](#/node/RakeMap.min_term_zero) says term 0 is the minimum; [RakeMap.pred](#/node/RakeMap.pred) reads the predicate back.
""",
 [q("What does `hbij` state?", ["pred n holds iff n is some term of the rake", "the term function is injective", "pred is decidable"], 0, "RakeMap.lean line 8."),
  q("Does the Lean state that the term function is one-to-one?", ["No", "Yes"], 0, "Despite the name `hbij` and the docstring, only the iff with pred is stated."),
  q("Why require sortedness?", ["so term 0 is the minimum", "for printing"], 0, "`min_term_zero`.")],
 caveats=["The docstring's '1-to-1 mapping' and the field name `hbij` suggest a bijection; the field states only that the set of terms equals { n | pred n }. Nothing in the sieve needs injectivity."])

node("RakeMap.pred", "RakeMap.pred: the property a rake map describes",
 "**The surprise:** it ignores its argument's contents entirely; the predicate lives in the type, and this just reads it back.",
 r"""
## Plain English

`pred (_ : RakeMap p) := p` (RakeMap.lean line 15). Used to name a [RakeMap](#/node/RakeMap)'s predicate, e.g. `prop := rm.pred` in [RakeSieve.init](#/node/RakeSieve.init).
""",
 [q("What does `rm.pred` return for `rm : RakeMap p`?", ["p", "the rake"], 0, "Definition."),
  q("Does it inspect the rake?", ["No", "Yes"], 0, "The argument is unused (`_`)."),
  q("Where is it used?", ["RakeSieve.init and next set `prop := rm.pred`", "nowhere"], 0, "RakeSieve.lean lines 23 and 97.")])

node("RakeMap.rm_ge2", "rm_ge2: the rake 2 + n describes the numbers ≥ 2",
 "**The surprise:** the first certified fact in the sieve's chain: the single sequence 2 + n lists exactly the numbers from 2 up.",
 r"""
## Plain English

`rm_ge2 : RakeMap (λ n => 2 ≤ n)` (RakeMap.lean lines 27–34): the rake [Rake.ge2](#/node/Rake.ge2), with the proof that n ≥ 2 iff n = 2 + m for some m. [RakeSieve.init](#/node/RakeSieve.init) removes the multiples of 2 from it.
""",
 [q("Which m gives term m = n for n ≥ 2?", ["n − 2", "n", "n/2"], 0, "`use n-2` (RakeMap.lean line 32)."),
  q("What is its predicate?", ["2 ≤ n", "n prime"], 0, "It is part of the type `RakeMap (λ n => 2 ≤ n)`."),
  q("What comes next in the sieve?", ["removing multiples of 2", "removing multiples of 3"], 0, "`rm_ge2 |>.rem 2` (RakeSieve.lean line 20).")])

node("RakeMap.rem", "RakeMap.rem: remove multiples of j, keeping the certificate",
 "**The surprise:** it cannot be called without proof that something will survive, which is why the RakeSieve needs Euclid at every step.",
 r"""
## Plain English

`rm.rem j hj hnmr` (RakeMap.lean lines 48–68): given a [RakeMap](#/node/RakeMap) for prop, a positive j and a proof that some term is not a multiple of j, it returns a RakeMap for **prop n ∧ ¬ j ∣ n**. Inside, it applies [Rake.rem](#/node/Rake.rem), uses rem_drop/rem_keep/rem_same to update the iff, then sorts the constants (`Rake.sort`, which removes duplicates and merge-sorts) so the result is sorted again.

The comment above it suggests a future version returning `Option Rake` instead of requiring the proof.
""",
 [q("What predicate does the result describe?", ["prop n ∧ ¬ j ∣ n", "prop n ∨ j ∣ n"], 0, "The return type."),
  q("Why must j be positive?", ["partitioning by 0 would leave no sequences", "for printing"], 0, "Comment, RakeMap.lean lines 39–41."),
  q("Why sort at the end?", ["partition and filter make the constants unsorted, and RakeMap requires sorted", "for speed"], 0, "`hord` must hold.")])

node("RakeMap.min_term_zero", "A rake map's first term is its smallest",
 "**The surprise:** a one-line wrapper, but it is the step that turns 'sorted list' into 'this is the next prime'.",
 r"""
## Plain English

**Theorem (`RakeMap.min_term_zero`, RakeMap.lean lines 18–19).** rm.term 0 ≤ rm.term n for every n. It is [Rake.sorted_min_term_zero](#/node/Rake.sorted_min_term_zero) applied with the map's sortedness proof. [RakeSieve.next](#/node/RakeSieve.next) uses it on its last line.
""",
 [q("Which proof does it reuse?", ["`Rake.sorted_min_term_zero`", "`c_prime`"], 0, "RakeMap.lean line 19."),
  q("Why is the rake map sorted?", ["`hord` is a field", "luck"], 0, "Every RakeMap carries it."),
  q("Where is it used?", ["RakeSieve.next, for `hRmin`", "SimpleGen"], 0, "RakeSieve.lean line 111.")])

node("main", "main: print the first five primes from the RakeSieve",
 "**The surprise:** the verified sieve is also a runnable program; `#eval main` prints its first five primes when the file is compiled. That is a demo, not a proof.",
 r"""
## Plain English

`main` (Main.lean lines 4–10) starts a `PrimeSieve RakeSieve` at [RakeSieve.init](#/node/RakeSieve.init), steps it five times and prints the primes, which should be [2, 3, 5, 7, 11]. Main.lean line 12 runs it with `#eval`. Being the `lean_exe` root, it is built by `lake build`.

The output is not checked by any assertion, and this site did not run it (no Lean build). For a checked computation see the `#guard` on `primes SimpleGen.start 10` (PrimeGen.lean line 97), which is about the simple generator, not the RakeSieve.
""",
 [q("Is `#eval main` a proof of anything?", ["No, it prints output; nothing checks it", "Yes"], 0, "Unlike `#guard`, `#eval` does not fail on a wrong value."),
  q("How many primes does it print?", ["5", "10"], 0, "`for _ in [0:5]`."),
  q("Which generator does it run?", ["PrimeSieve RakeSieve", "SimpleGen"], 0, "Main.lean line 5.")])

node("Rake.zer", "Rake.zer: the placeholder rake {0}",
 "**The surprise:** it exists only so `rem` always returns something; the sieve proves it is never actually reached.",
 r"""
## Plain English

`zer := { d := 0, ks := [0] }` (Rake.lean line 26): the rake whose only term is 0. [Rake.rem](#/node/Rake.rem) returns it if every sequence would be removed; `rem_def` (Rake.lean lines 370–409) shows that cannot happen when the rake has a non-multiple.
""",
 [q("What are its terms?", ["only 0", "all numbers"], 0, "Step 0 and constant 0 give 0 forever."),
  q("When does `rem` return it?", ["when every constant is a multiple of j", "never, by definition"], 0, "See Rake.lean line 361."),
  q("Does the sieve ever reach it?", ["No, HasNonMultiple rules it out", "Yes"], 0, "That is why RakeMap.rem asks for a non-multiple.")])
