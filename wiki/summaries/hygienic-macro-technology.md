---
type: summary
status: reviewed
title: Hygienic Macro Technology
created: 2026-08-05
source: https://dl.acm.org/doi/pdf/10.1145/3386330
raw: raw/2026-08-05-3386330.md
tags: [programming-languages, language-implementation, scheme, lisp, macros]
---

# Hygienic Macro Technology

## Summary

[[william-clinger|William D Clinger]] and [[mitchell-wand|Mitchell Wand]]'s HOPL IV
history of [[hygienic-macros|hygienic macro expansion]], shepherded by
[[guy-steele|Guy L. Steele Jr.]] — a long-form account of a problem recognized in
the 1960s that took twenty years to solve reliably and another ten to solve well.

The paper opens by grounding the problem in logic rather than in programming. Naïve
substitution is unsound: universal elimination, stated as substituting a term `t`
for free occurrences of `x` in φ, fails without the side condition that no variable
free in `t` occurs bound in φ. The remedy logicians reach for is alpha conversion —
renaming bound variables. Macro expansion is the same substitution problem, made
worse by block structure, higher-order functions, and module boundaries.

The running example is a short-circuiting `or` macro whose third rewrite rule binds
a local `temp` to avoid evaluating its first operand twice. That `let` is what makes
the macro correct in the presence of side effects, and it is also what breaks it: a
programmer who already has a variable named `temp` in scope has it silently captured.
Both properties come from the same feature, which is why the problem resisted easy
fixes.

Clinger and Wand attribute Lisp's unusual reliance on macros to its fully
parenthesized Cambridge Polish syntax — a `read` procedure can parse it without
knowing the syntax of any construct it represents, yielding a standard representation
for uninterpreted abstract syntax trees. That representation is what makes macros
convenient, and convenience is what made the leaky abstraction matter.

The history proper runs through:

- **Macros in Lisp and Scheme before hygiene**, including workarounds programmers
  used (generated names, obscure identifiers) and the development of Common Lisp.
  A 1984 workshop at Brandeis gets a full section, with the invitation list,
  represented implementations, and agenda reproduced.
- **Kohlbecker's algorithm** — the first reliable, actually-implemented technology
  giving programmers freedom from inadvertent capture. Eugene Kohlbecker completed
  his dissertation at Indiana in 1986 under Dan Friedman, amid half a dozen
  colleagues publishing on macro technology. The paper credits Matthias Felleisen
  with suggesting the word *hygiene*, which Barendregt had used for the alpha
  conversion needed to make beta conversion correct. Its fatal cost: it traversed
  the entire tree at every expansion, which could take quadratic or even exponential
  time.
- **Syntactic closures**, and their rise and fall — they failed because they required
  the macro writer to declare which identifiers came from where *before* the
  information needed to decide was available. Hygiene was not automatic.
- **Macros That Work** (Clinger and Rees, 1991), the Strong Hygiene Condition,
  referentially transparent local macros, explicit renaming, and standardization
  through R4RS.
- **Strong hygiene turning out not to be so strong** — Petrofsky extraction and
  Kiselyov defilement, two attacks showing the condition Clinger himself had claimed
  did not hold as advertised. He is candid that the claim was made without proof.
- **`syntax-case`** and syntax objects, framed as resolving the central tension: the
  hardest problem for an expander is deciding which parts of its output were already
  present in the macro use (no renaming needed) versus inserted by the macro (renaming
  required). Kohlbecker solved it by brute-force traversal, syntactic closures by
  asking the programmer too early, and `syntax-case` by combining `syntax-rules`'
  speed and automatic hygiene with procedural power and a controlled escape hatch.
- **The standards arc** — R4RS → R5RS → R6RS → R7RS, including the collapse of the
  RRRS-authors consensus process, the R6RS library and record systems, and a frank
  section on the causes and consequences of the record-system controversy.
- **Bindings as sets of scopes**, the more recent model, plus sections on subtleties
  of hygiene (are record field names symbols or identifiers? how should keywords
  match?), **Clojure's less naïve macro expansion** with an assessment of whether it
  would have sufficed, and hygienic macros for languages with conventional syntax.

## Why this matters

The inbox note asked for a broad overview of hygienic macro technology, and this is
the authoritative one — a HOPL paper by two of the people who built the thing,
shepherded by a third.

Its value here is that it takes macros as its subject, where much of the surrounding
material leans on them in passing: [[rabbit-a-compiler-for-scheme|RABBIT]] extends a
tiny basis set by macros, [[a-programmable-programming-language|Racket's]] whole thesis
is language-oriented programming built on them, and [[janet]] and [[lisp]] treat them
as the defining feature of the family. This page and [[hygienic-macros]] give that
scattered discussion somewhere to land, and an account of what makes macros hard.

It also complicates the picture of [[william-clinger|Clinger]]. He appears elsewhere as
the Twobit author arguing that compilers can be simple;
here he is across twenty years of a problem that stubbornly refused to be, publishing
a strong-hygiene claim "without proof" that was later broken and saying so plainly in
his own history. The two papers together are a better picture of him than either
alone, which is an argument for the hub-per-person structure rather than
summary-only filing.

The deepest point may be the one made in the first two pages: this is the substitution
problem from logic, and the fix — alpha conversion — was known long before anyone
tried to macro-expand a program. Twenty years of failure were not about discovering
the answer but about making it work on real programs with local macros, separate
compilation, and acceptable asymptotic complexity. That gap between knowing the
principle and shipping it is the same gap the compiler papers in this corpus keep
describing from the other side.
