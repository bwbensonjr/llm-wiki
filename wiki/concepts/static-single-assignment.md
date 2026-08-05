---
type: concept
status: reviewed
title: Static Single Assignment
created: 2026-07-08
tags: [language-implementation, programming-languages]
---

# Static Single Assignment

A compiler intermediate-representation property (SSA form) in which every
variable is assigned exactly once, and each use refers to a single, explicit
definition. Where control flow merges, a *ϕ* (phi) operation selects the value
according to the path taken.

## Notes

SSA makes the flow of values from definitions to uses explicit, which simplifies
many dataflow optimizations and eliminates spurious anti- and output
dependencies that would otherwise block reordering transformations.

It recurs across the compiler pages in this wiki:

- [[llvm|LLVM]] IR is an SSA representation with an explicit Phi instruction; the
  lack of SSA in GCC (until 2005) was one gap LLVM was designed to fill — see
  [[the-llvm-compiler-infrastructure|The LLVM Compiler Infrastructure]].
- The Manticore/PML CFG IR in
  [[compiling-with-continuations-and-llvm|Compiling with Continuations and LLVM]]
  is already in SSA form, but uses block parameters instead of explicit ϕ-nodes —
  the "SSA is functional programming" view (Appel) in which a block's parameters
  are supplied by its predecessors.

## Sources

- [[the-llvm-compiler-infrastructure|The LLVM Compiler Infrastructure]]
- [[compiling-with-continuations-and-llvm|Compiling with Continuations and LLVM]]
