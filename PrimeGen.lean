-- PrimeGen: a specification for algorithms that generate prime numbers.
import Mathlib.Data.Nat.Prime.Basic
import Mathlib.Data.Nat.Find
import Mathlib.Tactic.Linarith.Frontend

def NPrime : Type := { n: Nat // Nat.Prime n } deriving Repr, Ord, LT, LE

@[simp] theorem NPrime.eq_iff (a b : NPrime) : a = b ↔ a.val = b.val := Subtype.ext_iff
instance : ToString NPrime where toString s := s!"{s.val}"
instance : Dvd NPrime where dvd a b := a.val ∣ b.val
instance : Coe NPrime Nat where coe n := n.val
-- interestingly, the following seems to shadow normal Nat ∈ Set Nat operations.
-- instance : Membership NPrime (Set Nat) where mem n s := n.val ∈ s

/-- A prime generator yields a strictly increasing sequence of consecutive primes.
`init` is intentionally *not* part of the class: only needed for zero-arg `primes`;
prefer `primes g₀ n` with an explicit start state (e.g. `SimpleGen.start` in SimpleGen.lean). -/
class PrimeGen (α : Type) where
  P : α → NPrime
  next : α → α
  /-- No prime is skipped between `P g` and `P (next g)`. -/
  hP' (g:α) : (¬∃ q, Nat.Prime q ∧ P g < q ∧  q < P (next g))
  /-- The generated prime strictly increases at each step.
  Needed for infinitude: `hP'` alone allows a constant generator. -/
  hP_lt (g:α) : (P g : Nat) < P (next g)
open PrimeGen

abbrev PrimeGt (n p:Nat) := Nat.Prime p ∧ n < p

structure MinPrimeGt (n:Nat) where
  p : Nat
  hpgt : PrimeGt n p
  hmin : ∀q:Nat, q < p → (¬ PrimeGt n q)
theorem MinPrimeGt.p' (m:MinPrimeGt n) : Nat.Prime m.p := m.hpgt.left


/- function power. apply f recursively n times to x₀ and collect the results.
  (!! lean has `f^[n] x` but this doesn't collect intermediate results. maybe
  another version exists?) -/
def fpow (f : α → α) (n:Nat) (x₀ : α) : List α :=
  let rec aux (n:Nat) (x:α) (acc:List α) :=
    if n = 0 then x::acc
    else aux (n-1) (f x) (x::acc)
  aux (n-1) x₀ [] |>.reverse

set_option linter.hashCommand false

#guard fpow (λn => n+1) 10 0 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

/-- The first `n` primes from generator state `g₀` (inclusive). -/
def primes {α : Type} [pg: PrimeGen α] (g₀ : α) (n : Nat) : List NPrime :=
  fpow (fun g => pg.next g) n g₀ |>.map fun g => pg.P g


/-- After `k` steps, `P` has increased by at least `k`. -/
theorem PrimeGen.P_iterate_add_le {α : Type} [PrimeGen α] (g : α) (k : Nat) :
    (P g : Nat) + k ≤ P (next^[k] g) := by
  induction k with
  | zero => simp
  | succ k ih =>
    rw [Function.iterate_succ_apply']
    have hlt := hP_lt (next^[k] g)
    -- ih: P g + k ≤ P (next^[k] g); hlt: P (next^[k] g) < P (next (next^[k] g))
    omega

/-- Infinitude of primes from any `PrimeGen` instance (uses `hP_lt` + inhabited start).
`hP'` alone is not enough: a constant generator satisfies `hP'`. -/
theorem exists_prime_gt_of_primeGen {α : Type} [PrimeGen α] (g₀ : α) (n : Nat) :
    ∃ p, Nat.Prime p ∧ n < p := by
  let k := n + 1
  have hle : (P g₀ : Nat) + k ≤ P (next^[k] g₀) := PrimeGen.P_iterate_add_le g₀ k
  have h2 : (P g₀ : Nat) ≥ 2 := Nat.Prime.two_le (P g₀).prop
  refine ⟨P (next^[k] g₀), (P (next^[k] g₀)).prop, ?_⟩
  omega

/-- A prime generator skips nothing: every prime `q` at or above the start prime is emitted at
some step. (Take the first step whose prime passes `q`; the step before it is ≤ `q`, and `hP'`
leaves no room for `q` strictly in between.) -/
theorem PrimeGen.exists_iterate_P_eq {α : Type} [PrimeGen α] (g₀ : α) (q : Nat)
    (hq : Nat.Prime q) (hle : (P g₀ : Nat) ≤ q) : ∃ k, (P (next^[k] g₀) : Nat) = q := by
  classical
  have hex : ∃ k, q < (P (next^[k] g₀) : Nat) :=
    ⟨q + 1, by have := PrimeGen.P_iterate_add_le g₀ (q + 1); omega⟩
  set k := Nat.find hex with hkdef
  have hk : q < (P (next^[k] g₀) : Nat) := Nat.find_spec hex
  have hk0 : k ≠ 0 := by
    intro h0
    rw [h0, Function.iterate_zero, id] at hk
    omega
  obtain ⟨j, hj⟩ : ∃ j, k = j + 1 := Nat.exists_eq_succ_of_ne_zero hk0
  have hjle : (P (next^[j] g₀) : Nat) ≤ q := by
    have := Nat.find_min hex (show j < k by omega)
    omega
  rw [hj, Function.iterate_succ_apply'] at hk
  refine ⟨j, ?_⟩
  by_contra hne
  exact hP' (next^[j] g₀) ⟨q, hq, by omega, hk⟩
