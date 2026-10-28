-- SimpleGen: a brute-force *reference* prime generator.
--
-- This file is NOT on the RakeSieve's headline path. `SimpleGen` finds the next prime with
-- `Nat.find`, which needs a proof that a bigger prime exists, so it ASSUMES Euclid's theorem
-- (Mathlib's `Nat.exists_infinite_primes`). It is kept as an executable reference spec for
-- `PrimeGen`, not as evidence for infinitude: its "proof" that primes never run out is circular.
-- The RakeSieve (RakeSieve.lean) does not import this file; see NoEuclidCheck.lean.
import PrimeGen
import Mathlib.Data.Nat.Prime.Infinite

set_option linter.hashCommand false

section simple_gen

  /-- Euclid, imported: the reference generator assumes a prime above every `c`. -/
  theorem ex_prime_gt (c:Nat) : ∃ p, PrimeGt c p := by
    let d := c + 1 -- because the line below has ≤ and we need <
    let ⟨p, hcp, hprime⟩ : ∃ (p : ℕ), d ≤ p ∧ Nat.Prime p :=
      Nat.exists_infinite_primes d
    use p; constructor
    · exact hprime
    · omega

  def min_prime_gt (n: Nat) : MinPrimeGt n :=
    let e := ex_prime_gt n
    { p:=Nat.find e,
      hpgt:=Nat.find_spec e,
      hmin:= by exact fun {q} a => Nat.find_min e a}

  structure SimpleGen where
    p : NPrime
    c : MinPrimeGt p.val

  def SimpleGen.next (g:SimpleGen) : SimpleGen :=
    { p:=⟨g.c.p, g.c.hpgt.left⟩, c:=min_prime_gt g.c.p }

  /-- Canonical start state for `SimpleGen` (replaces class-level `init`). -/
  def SimpleGen.start : SimpleGen :=
    { p := ⟨2, Nat.prime_two⟩, c := min_prime_gt 2 }

  instance : PrimeGen SimpleGen where
    P g := g.p
    next := .next
    hP' g := by  -- goal: no prime q between g.p and (g.next.p = g.c.p)
      -- why? that would imply prime_gt (g.p) q, but hmin contradicts this
      intro h
      rcases h with ⟨q, hq, hgt, hlt⟩
      exact (g.c.hmin q hlt) ⟨hq, hgt⟩
    hP_lt g := by
      -- g.next.p = g.c.p and g.c witnesses PrimeGt g.p
      simpa [SimpleGen.next] using g.c.hpgt.right

  open PrimeGen

end simple_gen

#guard (primes SimpleGen.start 10 |>.map (·.val)) = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

/-- Euclid's theorem, run through the reference generator. CIRCULAR: `SimpleGen` is built from
`Nat.exists_infinite_primes` (via `ex_prime_gt`), so this only checks the `PrimeGen` plumbing.
(Formerly `results_exists_prime_gt_of_simpleGen` in Results.lean.) -/
theorem simpleGen_exists_prime_gt (n : Nat) : ∃ p, Nat.Prime p ∧ n < p :=
  exists_prime_gt_of_primeGen SimpleGen.start n
