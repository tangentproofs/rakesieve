-- NoEuclidCheck: machine check that the RakeSieve headline does not use Euclid's theorem.
--
-- `#assert_no_euclid t₁ t₂ …` walks the full constant-dependency closure of each theorem
-- (every constant its type or proof mentions, transitively, through Mathlib and core) and
-- fails if the closure contains any constant declared in `Mathlib.Data.Nat.Prime.Infinite`
-- (home of `Nat.exists_infinite_primes`, `Nat.infinite_setOf_prime`, …) or any name on an
-- explicit deny-list of infinitude-of-primes results.
--
-- `#assert_uses_euclid t` is the control: it must FIND Euclid in the closure, so a broken walk
-- that sees nothing cannot pass silently.
import Results
import SimpleGen

open Lean Elab Command

namespace NoEuclidCheck

/-- Infinitude-of-primes results that the headline must not depend on. -/
def denyList : List Name :=
  [`Nat.exists_infinite_primes, `Nat.exists_prime_ge, `Nat.infinite_setOf_prime,
   `Nat.not_bddAbove_setOf_prime, `Nat.infinite_setOf_prime_modEq_one,
   `Nat.Primes.infinite, `Nat.frequently_atTop_prime]

def euclidModule : Name := `Mathlib.Data.Nat.Prime.Infinite

/-- All constants reachable from `roots` through types and values. -/
partial def closure (env : Environment) (todo : List Name) (seen : NameSet) : NameSet :=
  match todo with
  | [] => seen
  | n :: rest =>
    if seen.contains n then closure env rest seen
    else
      let seen := seen.insert n
      match env.find? n with
      | some ci => closure env (ci.getUsedConstantsAsSet.toList ++ rest) seen
      | none => closure env rest seen

def moduleOf (env : Environment) (n : Name) : Option Name :=
  env.getModuleIdxFor? n |>.map fun i => env.header.moduleNames[i.toNat]!

/-- The offending constants in the closure of `root`, and the closure's size. -/
def offenders (env : Environment) (root : Name) : List Name × Nat :=
  let cl := closure env [root] {}
  let bad := cl.toList.filter fun n => denyList.contains n || moduleOf env n == some euclidModule
  (bad, cl.size)

elab "#assert_no_euclid " ids:ident* : command => do
  let env ← getEnv
  for id in ids do
    let n ← liftCoreM <| realizeGlobalConstNoOverloadWithInfo id
    let (bad, size) := offenders env n
    if bad.isEmpty then
      logInfo m!"ok: {n}: {size} constants in its dependency closure, none from {euclidModule} or the deny-list"
    else
      throwError m!"{n} depends on Euclid: {bad}"

elab "#assert_uses_euclid " id:ident : command => do
  let env ← getEnv
  let n ← liftCoreM <| realizeGlobalConstNoOverloadWithInfo id
  let (bad, size) := offenders env n
  if bad.isEmpty then
    throwError m!"control failed: expected {n} to depend on Euclid, but its {size}-constant closure does not"
  else
    logInfo m!"control ok: {n} depends on Euclid via {bad} ({size} constants in closure)"

end NoEuclidCheck

-- The headline theorems, the sieve step, and the `PrimeGen` instance the corollary runs through.
#assert_no_euclid results_rakeSieve_never_empty results_rakeSieve_step
  results_rakeSieve_emits_every_prime results_exists_prime_gt_of_rakeSieve
  results_three_mem_R_two results_three_le_of_mem_R_two
  RakeSieve.next RakeSieve.survivor RakeSieve.init

-- Control: the reference generator really does use Euclid, and the walk sees it.
#assert_uses_euclid simpleGen_exists_prime_gt

#print axioms results_rakeSieve_never_empty
#print axioms results_rakeSieve_step
#print axioms results_rakeSieve_emits_every_prime
#print axioms results_exists_prime_gt_of_rakeSieve
