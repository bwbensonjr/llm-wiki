---
type: summary
status: provisional
title: "World Age in Julia: Optimizing Method Dispatch in the Presence of Eval"
created: 2026-10-31
source: https://arxiv.org/pdf/2010.07516
raw: raw/2026-10-31-2010.md
tags: [language-implementation, programming-languages, formal-methods]
---

# World Age in Julia: Optimizing Method Dispatch in the Presence of Eval

## Summary

An OOPSLA 2020 paper (Belyakova, Chung, Gelinas, Nash, Tate and Vitek; extended version) on how Julia keeps `eval` from undermining its optimizer. `eval` comes from [[lisp|Lisp]], and in Julia, as in Lisp and Clojure, it runs only at the top level, so it cannot touch a function's local variables. The harder side effect is redefinition: Julia relies on symmetric multiple dispatch (multiplication alone has 357 standard methods), so fast code depends on resolving calls at compile time, and any call could be invalidated by a newly `eval`ed method.

Julia's answer is **world age**. A global counter increments on every method definition; each method records a birth age and, if replaced, a death age. When a call starts at the top level it fixes the set of visible methods, and nothing it calls sees methods defined later until control returns to the top level. The paper's Clojure contrast makes the difference concrete: where a function that redefines `g` via `eval` and then calls `g` sees the new definition at once in Clojure, the first call in Julia still sees the old one. Because the method table is frozen for the duration of a top-level call, the JIT can inline, devirtualize and specialize without any deoptimization machinery. Programmers who need a fresh definition opt out explicitly with `invokelatest` (or a slower nested `eval`), paying the cost only at those call sites. Global *variables* are deliberately exempt: data changes are visible immediately, and the compiler relies on the method table, not on globals.

The contributions are Juliette, a core calculus that replaces counters with method tables copied at the top level; proofs that inlining, devirtualization and specialization are correct under it; a Redex model for testing; and a corpus study of all 4,011 registered packages (August 2020), which estimates that only 4 to 9% might be affected by world age, most often by defining functions with `eval` and then calling them. The conclusion argues the idea generalizes to any language that updates function definitions at run time, possibly with an explicit "freeze" point instead of Julia's top level, for systems such as servers that have no natural top level.

## Why this matters

The paper isolates the second of the two forces behind [[separate-compilation]] trouble in dynamic languages: if any function can be redefined at run time, a compiler cannot inline across a call it does not control, whether that call crosses a module boundary or not. World age shows one disciplined escape: make the moment when new definitions become visible explicit, and compiled code can treat everything else as fixed. That is a useful lens for deciding which redefinitions a separately compiled library or a standalone executable must still honor, and which it may assume away.
