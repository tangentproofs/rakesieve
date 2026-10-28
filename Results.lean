-- Results: the headline theorems of the RakeSieve.
--
-- None of these depend on Mathlib's infinitude of primes (`Nat.exists_infinite_primes` or
-- anything else in `Mathlib.Data.Nat.Prime.Infinite`); NoEuclidCheck.lean checks this by
-- walking each theorem's full dependency closure. The brute-force `SimpleGen`, which does
-- assume Euclid, lives in SimpleGen.lean as a reference spec and is not imported here.
import PrimeGen
import PrimeSieve
import RakeSieve

theorem results_three_mem_R_two : (3 : Nat) ∈ R 2 :=
  three_mem_R_two

theorem results_three_le_of_mem_R_two : ∀ r ∈ R 2, (3 : Nat) ≤ r :=
  three_le_of_mem_R_two

/-- **Headline 1: the rake never runs empty.** In every RakeSieve state, removing the
multiples of the candidate `c` leaves a term of the rake (namely `c + d`, one period on).
So the sieve can always take another step. -/
theorem results_rakeSieve_never_empty (s : RakeSieve) :
    ∃ n m, ¬ s.c ∣ n ∧ s.rm.term m = n :=
  s.survivor (c_prime RakeSieve s)

/-- **Headline 2: each step emits the next prime, none skipped.** For every RakeSieve state,
the step's new prime is the old candidate, which is prime, larger than the old prime, and no
prime lies strictly between them. -/
theorem results_rakeSieve_step (s : RakeSieve) :
    ((nextState s).p : Nat) = s.c ∧ Nat.Prime s.c ∧ (s.p : Nat) < s.c ∧
      ¬ ∃ q, Nat.Prime q ∧ (s.p : Nat) < q ∧ q < s.c :=
  ⟨(PrimeSieveState.hNext s (c_prime RakeSieve s) (no_skipped_prime RakeSieve s) rfl).1,
    c_prime RakeSieve s, c_gt_p RakeSieve s, no_skipped_prime RakeSieve s⟩

/-- **Headline 3: started at `RakeSieve.init`, the sieve emits every prime.** For every prime
`q` there is a step count `k` after which the sieve's current prime is `q`. -/
theorem results_rakeSieve_emits_every_prime (q : Nat) (hq : Nat.Prime q) :
    ∃ k, (PrimeGen.P (PrimeGen.next^[k] ({ state := RakeSieve.init } : PrimeSieve RakeSieve)) : Nat) = q :=
  PrimeGen.exists_iterate_P_eq _ q hq (Nat.Prime.two_le hq)

/-- CONDITIONAL: any prime generator (an instance of `PrimeGen`) implies infinitely many primes. -/
theorem results_exists_prime_gt_of_primeGen {α : Type} [PrimeGen α] (g₀ : α) (n : Nat) :
    ∃ p, Nat.Prime p ∧ n < p :=
  exists_prime_gt_of_primeGen g₀ n

/-- **Corollary: there are infinitely many primes**, because the rake sieve never stops and its
primes strictly increase. The proof does not use Mathlib's infinitude of primes. -/
theorem results_exists_prime_gt_of_rakeSieve (n : Nat) :
    ∃ p, Nat.Prime p ∧ n < p :=
  exists_prime_gt_of_primeGen ({ state := RakeSieve.init } : PrimeSieve RakeSieve) n
