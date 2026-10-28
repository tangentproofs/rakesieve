-- RakeSieve uses a rake to implement a prime sieve.
import RakeMap
import PrimeSieve

structure RakeSieve where
  prop : Nat -> Prop
  rm: RakeMap prop
  p : NPrime               -- the current prime
  c : Nat                  -- the candidate for next prime
  hprop : ∀ n:Nat, prop n ↔ n ∈ R p
  hCinR : c ∈ R p
  hRmin : ∀ r ∈ R p, c ≤ r
  -- every prime factor of the rake's period is one of the primes sifted so far.
  -- (the period is their product, p#.) This is what lets the rake prove it never runs empty.
  hdfac : ∀ q, Nat.Prime q → q ∣ rm.rake.d → q ≤ p.val
  -- Q : Array RakeMap     -- queue of found primes

namespace RakeSieve

open RakeMap

def init : RakeSieve :=
  let rm : RakeMap (λn => n≥2 ∧ ¬2∣n) := rm_ge2 |>.rem 2 (by simp) (by
    use 3; use 1; simp[rm_ge2, Rake.ge2, Rake.term])
  let p := ⟨2, Nat.prime_two⟩
  { prop := rm.pred, rm := rm, p := p, c := 3,
    hprop := by
      have hrm : rm.pred = λn => n ≥ 2 ∧ ¬ 2∣n := by simp[RakeMap.pred]
      show ∀ n, rm.pred n ↔ n ∈ R p
      have hbij := rm.hbij
      unfold R; simp_all; intro n
      apply Iff.intro
      case mp =>
        intro hn
        apply And.intro
        · rw[← hbij] at hn; exact hn.left
        · intro q hq hq'
          simp[←hbij] at hn
          have hp2 : (p : Nat) = 2 := rfl
          have hq2 : 2 ≤ q := Nat.Prime.two_le hq'
          have : 2 = q := by omega
          rw[this] at hn
          omega
      case mpr =>
        simp; intro hn hn2; rw[←hbij]; simp_all
        have hp2: p.val = 2 := by rfl
        have hn2' := hn2
        set p' := p.val
        specialize hn2' p';  simp[hp2] at hn2'
        exact hn2' Nat.prime_two
    hCinR := by
      -- generic base-case fact: 3 ∈ R 2
      simpa [p] using three_mem_R_two
    hRmin := by
      -- generic base-case fact: 3 is least in R 2
      simpa [p] using three_le_of_mem_R_two
    hdfac := by
      -- the period of the start rake is 1 * 2 = 2, whose only prime factor is 2.
      intro q _ hqd
      have hd : rm.rake.d = 2 := (RakeMap.rem_d _ _ _ _).trans rfl
      rw [hd] at hqd
      exact Nat.le_of_dvd (by decide) hqd }

/--
The rake never runs empty: removing the multiples of the candidate `c` always leaves a term.

The witness comes from the rake itself, not from Mathlib's infinitude of primes. `c` is a term
of the rake, say at index `m₀`; one period later, at `m₀ + len`, the rake produces `c + d`.
Every prime factor of `d` is ≤ p < c (`hdfac`), so the prime `c` does not divide `d`, hence
does not divide `c + d`. (This is Euclid's argument, with `c + p#` playing the part of
`p# + 1`, but it is carried by the data structure: no infinitude theorem is imported.) -/
theorem survivor (s : RakeSieve) (hC : Nat.Prime s.c) :
    ∃ n m, ¬ s.c ∣ n ∧ s.rm.term m = n := by
  obtain ⟨m₀, hm₀⟩ := (s.rm.hbij s.c).mp ((s.hprop s.c).mpr s.hCinR)
  refine ⟨s.c + s.rm.rake.d, m₀ + s.rm.rake.ks.length, ?_, ?_⟩
  · intro hdvd
    have hcd : s.c ∣ s.rm.rake.d := (Nat.dvd_add_iff_right (dvd_refl s.c)).mpr hdvd
    have hle : s.c ≤ s.p.val := s.hdfac s.c hC hcd
    have hgt : s.c > s.p.val := r_gt_p s.p.val s.c s.hCinR
    omega
  · show s.rm.rake.term (m₀ + s.rm.rake.ks.length) = _
    rw [Rake.term_add_len, hm₀]

def next (rs₀ : RakeSieve) (hC₀: Nat.Prime rs₀.c) (hNS: nosk' rs₀.p rs₀.c): RakeSieve :=
  let h₀ := rs₀.prop
  have hh₀ : ∀n, h₀ n ↔ n ∈ R rs₀.p := rs₀.hprop
  have hCR₀ := rs₀.hCinR
  have hpgt:PrimeGt rs₀.p rs₀.c := by
    constructor
    · exact hC₀
    · exact r_gt_p (↑rs₀.p) rs₀.c hCR₀
  have hmin: ∀ q < rs₀.c, ¬PrimeGt (↑rs₀.p) q := by
    simp_all; intro q hq hq'; apply hNS at hq'; omega
  let c' : MinPrimeGt rs₀.p := { p:=rs₀.c, hpgt:=hpgt, hmin:=hmin}

  -- to call `rem`, we have to prove that it won't remove everything.
  -- the rake supplies its own witness, c + d (see `survivor`).
  have hsurv : ∃n m, ¬rs₀.c ∣ n ∧ rs₀.rm.term m = n := rs₀.survivor hC₀

  -- now we can use this fact to remove multiples of c
  let rs := rs₀.rm.rem c'.p (Nat.Prime.pos hC₀) hsurv
  let c₁ := rs.rake.term 0
  have hc₁: ∃ i, rs.rake.term i = c₁ := by
    exact exists_apply_eq_apply (fun a => rs.rake.term a) 0
  let h₁ := rs.pred
  have hh₁ : ∀n, h₁ n ↔ h₀ n ∧ ¬(c'.p∣n) := by
    intro n
    rfl
  have hprop : ∀n, h₁ n ↔ n ∈ R c'.p := by
    intro n; exact r_next_prop (hh₀ n) (hh₁ n)
  { prop := rs.pred, rm := rs, p := ⟨c'.p, hC₀⟩, c := c₁,
    hprop := hprop
    hCinR := by
      show c₁ ∈ R c'.p
      · have : h₁ c₁ := by rw[← rs.hbij] at hc₁; exact hc₁
        specialize hprop c₁
        exact hprop.mp this
    hRmin := by
      dsimp[c₁,p,h₁] at *
      intro r hr
      have : ∃k, rs.rake.term k = r := by
        exact (rs.hbij r).mp ((hprop r).mpr hr)
      obtain ⟨k, hk⟩ := this
      rw[←hk]
      exact rs.min_term_zero k
    hdfac := by
      -- the new period is d * c: its prime factors are those of d (all ≤ p < c) and c itself.
      intro q hq hqd
      have hd : rs.rake.d = rs₀.rm.rake.d * rs₀.c := RakeMap.rem_d _ _ _ _
      rw [hd] at hqd
      show q ≤ rs₀.c
      rcases (Nat.Prime.dvd_mul hq).mp hqd with h | h
      · have h₁ := rs₀.hdfac q hq h
        have h₂ : rs₀.c > rs₀.p.val := r_gt_p rs₀.p.val rs₀.c hCR₀
        omega
      · exact Nat.le_of_dvd hC₀.pos h }

instance : PrimeSieveState RakeSieve where
  P x := x.p
  C x := x.c
  next := .next
  hNext := by
    intro s hC hNS s' hs'; simp_all; rw[←hs']
    unfold next at hs'; simp at hs'
    have hpc: s'.p = s.c := by simp_all
    apply And.intro
    · exact hpc
    · show s'.c > s.c
      have := s'.hCinR
      have := r_gt_p
      aesop

open PrimeSieveState

instance : PrimeSieveDriver RakeSieve where
  hCinR x := by dsimp[C]; dsimp[P]; exact x.hCinR
  hRmin x := by dsimp[C]; dsimp[P]; exact x.hRmin
