# About this site

**RakeSieve** ([tangentproofs/rakesieve](https://github.com/tangentproofs/rakesieve), formerly `leansieve`) is a small Lean 4 library by Michal Wallace (tangentstorm). It models sets of natural numbers as *rakes*, lists of arithmetic sequences k + d·n that share one step d, and builds a prime sieve from them: start with 2 + n, and at each prime p, split every sequence by p and drop the ones that are all multiples of p. The smallest constant left is the next prime. The [project home](../) has the overview and build notes.

This site reads the Lean back into plain English. Each node is one Lean declaration with its verbatim Lean, a plain-English reading, caveats and a short quiz. Tick **I understand** when you do. A node counts as understood once everything its statement mentions is understood too.

The [Lean source](src/index.html) is on the site, highlighted, and every "File.lean lines a–b" reference opens those exact lines.

Start with [the statements](#/start), or read the [review](#/review). It explains what the headline theorems say, and why the infinitude corollary no longer leans on Mathlib's infinitude of primes.

**Credit.** Lean library: Michal Wallace (MIT). Explanations: drafts by Grok Bot, not yet reviewed, and possibly wrong. The Lean is the ground truth.
