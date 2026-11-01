---
type: summary
status: provisional
title: "Composable and Compilable Macros: You Want It When?"
created: 2026-10-31
source: https://users.cs.utah.edu/plt/publications/macromod.pdf
raw: raw/2026-10-31-macromod.md
tags: [macros, scheme, racket, language-implementation, programming-languages]
---

# Composable and Compilable Macros: You Want It When?

## Summary

[[matthew-flatt|Matthew Flatt]]'s ICFP 2002 paper on the module and macro system of MzScheme (the language that became [[racket|Racket]]), built so that macro-using code compiles separately and predictably. The problem it names is that expressive macro systems run arbitrary code at compile time, usually in the same language as run-time code, so implementations let compile-time values, run-time values and values from separate compilations mingle. In a typical [[scheme|Scheme]] a program written in an extension language `E` is run by `(load "E.scm") (load "P.scm")`. Compiling that file is useless, because the result is just two compiled `load` calls, so the full compiler is needed at run time. The conventional fix, `eval-when` annotations, is fragile (a run-time helper added to `E.scm` silently invalidates them), hard to get right for tall "language towers", and can appear to work by accident when run-time code happens to supply what compile-time code needed.

Flatt's requirement is that compiling new code must never affect previously compiled code, and the result must be the same whether everything is compiled in advance, interleaved with execution at a REPL, or "half the code is compiled today and the rest is compiled on a different machine tomorrow". When a whole application is compiled, all compile-time code must be strippable from the deliverable. MzScheme meets this by making module dependencies explicit (`require` instead of `load` side effects) and by separating run-time imports from compile-time ones (`require-for-syntax`). Each module is *instantiated separately per phase and per compilation*: compiling a client re-runs a compile-time dependency, and running it runs that dependency's run-time part again, so state never leaks between compilations. Even core Scheme exists in multiple phases; the compile-time `cons` is in principle unrelated to the run-time `cons`.

The hard part comes from the two features that make Scheme macros worth having, macro-generating macros and lexical scope ([[hygienic-macros]]): whether a templated identifier is compile-time or run-time code is not statically decidable, and is discovered only as expansion proceeds. So each identifier carries lexical information for each phase, and a reference that resolves to a binding from the wrong phase is a syntax error, even when interleaved REPL evaluation would happen to have the binding available. Because invoking a compiled module never requires running its macros, the compiler can drop every compile-time expression, and whole modules used only through `require-for-syntax`, from the final program. A formal model shows effects confined to one phase. In related work Flatt contrasts the [[scheme-48|Scheme 48]] module system, which has `for-syntax` imports but instantiates a module once per session so state can leak across compilations, and Chez Scheme's lexically scoped modules, which leave phase management to `load`, `visit` and `eval-when`. This is the problem [[separate-compilation]] names in a macro-extensible language.

## Why this matters

Flatt states, as a design requirement, the exact condition that makes separate compilation hard in a Lisp with full macros: a library is not just code to link but code that runs inside the compiler of everything that imports it. His answer, explicit per-phase instantiation that can be stripped from the deliverable, ties the two halves of the question together, since the same separation that makes separate compilation sound is what lets a standalone executable omit the compiler. That makes it a reference point for how a system like Emit Scheme might organize library phases before trying to link compiled libraries into an executable.
