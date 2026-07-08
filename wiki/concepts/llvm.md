---
type: concept
title: LLVM
created: 2026-07-08
tags: [llvm, language-implementation, programming-languages]
---

# LLVM

A compiler infrastructure providing a low-level, SSA-based intermediate
representation (LLVM IR) together with a large library of optimization passes
and native code generators. Originally designed with imperative and
object-oriented languages in mind, it has become a popular backend for research
and production compilers.

## Notes

LLVM spares compiler writers from maintaining per-architecture native code
generators and is a better "portable assembly language" than C. But its design
carries a bias toward C runtime conventions, which makes it an awkward target
for functional-language implementations that need guaranteed tail-call
optimization, specialized register/calling conventions, a garbage-collector
interface, and first-class continuations.

[[compiling-with-continuations-and-llvm|Farvardin and Reppy]] address this for
[[continuation-passing-style]] compilers by adding a "Jump-With-Arguments" (JWA)
calling convention to a fork of LLVM, using the `naked` attribute and an assembly
shim for stack management, and exploiting JWA's matched call/return convention to
manufacture first-class labels. Other functional-language LLVM backends include
those for [[standard-ml|Standard ML]] (SML/NJ, MLton, SML#), Haskell (GHC), and
Erlang (ErLLVM), each with its own strategy for tail calls.

## Sources

- [[compiling-with-continuations-and-llvm|Compiling with Continuations and LLVM]]
