---
type: concept
status: reviewed
title: Hygienic Macros
created: 2026-08-05
tags: [programming-languages, language-implementation, scheme, lisp, macros]
---

# Hygienic Macros

Macro expansion that cannot accidentally capture identifiers: names a macro
introduces never collide with names at the use site, and names passed into a macro
keep the meaning they had where they were written.

## Notes

The problem is substitution, and it is older than programming. Naïve substitution is
unsound in first-order logic too — universal elimination needs the side condition
that no variable free in the substituted term occurs bound in the target formula, and
the remedy is alpha conversion. Barendregt used *hygiene* for exactly that renaming;
Matthias Felleisen suggested Eugene Kohlbecker borrow the word for macros.

The canonical illustration is a short-circuiting `or` macro that binds a temporary to
avoid evaluating its first operand twice. The binding is what makes the macro correct
under side effects, and the same binding captures a user's variable of that name. One
feature, both properties — which is why the problem resisted piecemeal fixes and why
programmers' workarounds (generated names, deliberately obscure identifiers) were
never more than mitigation.

**The central technical difficulty**, as
[[hygienic-macro-technology|Clinger and Wand]] frame it, is telling apart the parts of
an expander's output that were already in the macro use — needing no renaming — from
the parts the macro inserted, which do. Each generation answered differently:

- **Kohlbecker's algorithm** (1986, Indiana, under Dan Friedman) was the first
  reliable, implemented solution: traverse the whole tree at every expansion. Correct,
  but quadratic or even exponential.
- **Syntactic closures** pushed the decision onto the macro writer, requiring it
  before the information needed to make it existed. Hygiene was not automatic, and
  they fell out of favor.
- **Macros That Work** (Clinger and Rees, 1991) introduced the Strong Hygiene
  Condition and referentially transparent local macros, and fed into R4RS.
- **`syntax-case`** combined `syntax-rules`' speed and automatic hygiene with the
  expressive power of procedural macros and a controlled escape from hygiene, via
  syntax objects.
- **Bindings as sets of scopes** is the more recent model.

Hygiene is not an absolute. Strong hygiene was claimed without proof and later broken
by *Petrofsky extraction* and *Kiselyov defilement*. And thorough hygiene is itself a
limitation: a fully hygienic system cannot express macros that bind identifiers
implicitly, which is why every practical design provides a deliberate escape hatch.

Hygienic macros are the mechanism underneath
[[language-oriented-programming|language-oriented programming]] as
[[a-programmable-programming-language|Racket]] practices it, and the reason
[[lisp]]-family languages treat macros as a load-bearing abstraction rather than a
preprocessor. [[racket]] and [[chez-scheme]] both carry substantial macro-system
machinery, and the standards arc from R4RS through R7RS is largely an argument about
this feature.

## Sources

- [[hygienic-macro-technology|Hygienic Macro Technology]]
- [[the-development-of-chez-scheme|The Development of Chez Scheme]]
