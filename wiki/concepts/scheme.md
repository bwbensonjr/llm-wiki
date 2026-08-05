---
type: concept
status: reviewed
title: Scheme
created: 2026-06-29
tags: [scheme, lisp, programming-languages]
---

# Scheme

A small, lexically-scoped dialect of [[lisp|Lisp]] built on the principle that a
language should not include "everything but the kitchen sink," but rather
provide a minimal framework in which it is easy to build the kitchen sink. A
very small number of expression-forming rules, freely composed, suffice for a
practical language supporting functional, procedural, and object-oriented
styles, with first-class procedures (closures), high-level data types, and
automatic memory management.

## Notes

Scheme's conceptual simplicity makes it a natural extension and scripting
language: it can be implemented in relatively little code while still offering
lexical scope, nested procedures, and real data types. [[libscheme-scheme-as-a-c-library|libscheme]]
exploits exactly this, packaging Scheme as an embeddable C library in the mold
of Tcl.

Scheme is the trunk of a lineage already present in this wiki:

- [[racket|Racket]] is an heir of Scheme — it began life in January 1995 as PLT
  Scheme / MzScheme, and MzScheme was bootstrapped from
  [[libscheme-scheme-as-a-c-library|libscheme]]'s code. Racket pushes Scheme's
  macro system toward a full platform for [[language-oriented-programming]].
- [[janet|Janet]] is a modern, Scheme-influenced Lisp that, like libscheme, is
  designed to embed cleanly into C — a parallel solution to the same
  extension-language problem two decades later.
- [[chez-scheme|Chez Scheme]] is a high-performance, R6RS Scheme implementation
  whose optimizing compiler and continuation support made it a good target VM —
  [[racket|Racket]] now runs on it (see
  [[porting-racket-to-chez-scheme|Porting Racket to Chez Scheme]]).

The defining Scheme features are lexical scope, first-class procedures that
close over their free variables, and a macro/syntax system more powerful than
C-style token substitution. Standardized in the Revised^n Reports on the
Algorithmic Language Scheme.

Scheme's heap-allocated first-class continuations (`call/cc`) connect it to the
[[continuation-passing-style]] compilation techniques in
[[compiling-with-continuations-and-llvm|Compiling with Continuations and LLVM]] —
a candidate approach for compiling a Scheme to [[llvm]] IR.

Scheme was invented by [[guy-steele|Guy L. Steele Jr.]] and Gerald Jay Sussman at
MIT in 1975, and its design and compilation were worked out across the
[[lambda-papers|Lambda Papers]]. The "minimal framework" philosophy above is that
series' central claim: a small [[lambda-calculus]]-shaped basis set plus macros,
with [[tail-recursion]] guaranteed so that iteration can be expressed
applicatively.

That Scheme can be compiled as efficiently as Pascal — rather than being an
inherently slow language — was established by
[[orbit-an-optimizing-compiler-for-scheme|ORBIT]], whose benchmarks beat an
optimizing Pascal compiler wherever procedure calls dominate.

## Sources

- [[libscheme-scheme-as-a-c-library|libscheme: Scheme as a C Library]]
- [[porting-racket-to-chez-scheme|Porting Racket to Chez Scheme]]
- [[compiling-with-continuations-and-llvm|Compiling with Continuations and LLVM]]
- [[rabbit-a-compiler-for-scheme|RABBIT: A Compiler for Scheme]]
- [[orbit-an-optimizing-compiler-for-scheme|ORBIT: An Optimizing Compiler for Scheme]]
- [[an-incremental-approach-to-compiler-construction|An Incremental Approach to Compiler Construction]]
- [[lambda-the-ultimate-label-a-simple-optimizing-compiler-for-scheme|Lambda, the Ultimate Label: A Simple Optimizing Compiler for Scheme]]
- [[a-tractable-native-code-scheme-system|A Tractable Native-Code Scheme System]]
- [[hygienic-macro-technology|Hygienic Macro Technology]]
- [[the-development-of-chez-scheme|The Development of Chez Scheme]]
