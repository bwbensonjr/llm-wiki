---
type: summary
title: Implicit Phasing for R6RS Libraries
created: 2026-10-31
source: inbox-files/1291151.1291197.pdf
raw: raw/2026-10-31-1291151-1291197.md
tags: [macros, scheme, language-implementation, programming-languages]
---

# Implicit Phasing for R6RS Libraries

## Summary

[[abdulaziz-ghuloum|Abdulaziz Ghuloum]] and [[r-kent-dybvig|R. Kent Dybvig]]'s ICFP 2007 paper on a portable implementation of the R6RS library system (the `psyntax` expander, built from Chez Scheme's portable `syntax-case`). It expands R6RS libraries and programs into a small core subset of R5RS, so the same library system runs on interpreters, incremental compilers and batch compilers, and it was ported to Chez Scheme, Chicken, Gambit, Gauche, Ikarus, Larceny and MzScheme. Its defining choice is **implicit phasing**: an `import` form says only *what* a library needs, and the expander infers *when*, at compile time or run time, from where each imported identifier is actually used. The paper's slogan is that the programmer says what is needed and the implementation decides when.

The library manager orders libraries by their acyclic import graph and **visits** a library (evaluates its macro transformers) when its keywords are needed for expansion, and **invokes** it (evaluates variable definitions and initialization) when its variables are needed at compile time or at run time. The authors argue that every library must be **expanded exactly once**: two separately expanded copies of one library can export inconsistent bindings, as when a macro inlines a constant under one configuration and defines a variable under another, so a program linked against both is "unlinkable". Each expansion therefore gets a globally unique identifier, which catches violations that "might occur through improperly managed separate compilation". The same guarantee lets a programmer rely on values fixed at compile time, such as unique structure tags or a compile-time timestamp, being the same across later invocations.

They invoke each library at most once per Scheme process, on demand, unlike [[composable-and-compilable-macros|Flatt's MzScheme]], which instantiates a fresh copy per phase. Their reasons: repeated initialization costs compile time, which matters because `eval` can compile at run time, and some resources cannot be duplicated, such as a symbol table, where per-phase copies would make `string->symbol` return non-`eq?` symbols. They argue explicit phase declarations overestimate needs (forcing extra invocations), constrain programs, and are no easier to implement, while R6RS leaves implementations free to initialize libraries when they choose anyway. An expanded library has three parts: metadata (name, version, unique ID, export labels, visit and invoke requirements), **visit-time code** and **invoke-time code**, both already reduced to core Scheme. Because visit code is needed only to compile other libraries, it "need not be shipped in the final application if the application performs no run-time compilation". Related work contrasts Chez Scheme's modules, which leave loading to `eval-when` and file operations, and Chicken's eggs, which keep macros out of libraries.

## Why this matters

This paper is the counterpoint to [[composable-and-compilable-macros|Flatt]] on the macro-phase part of [[separate-compilation]]. Both separate compile-time from run-time code in a library, but Ghuloum and Dybvig infer phases and share one instance across them, while Flatt declares phases and instantiates per phase. Their single-expansion invariant names a concrete hazard of separately compiled macro libraries: two builds of the same library may not link. The split into strippable visit code and shipped invoke code shows how a library system can serve both separate compilation and a standalone executable without the expander.
