---
type: summary
status: reviewed
title: Compiling with Continuations and LLVM
created: 2026-07-08
source: https://arxiv.org/pdf/1805.08842
raw: raw/2026-07-08-1805.md
tags: [language-implementation, llvm, continuations, standard-ml, programming-languages]
---

# Compiling with Continuations and LLVM

## Summary

A 2018 ML Workshop paper by [[john-reppy|John Reppy]] and Kavon Farvardin
(University of Chicago) showing how to use [[llvm]] as a backend for
functional-language compilers that rely on **heap-allocated first-class
continuations** — a runtime model LLVM's C-oriented design does not natively
accommodate. The work is implemented in the Parallel ML (PML) compiler of the
Manticore system, but the authors argue it transfers to other
[[continuation-passing-style]] compilers such as [[standard-ml|Standard ML]] of
New Jersey.

The core problem: functional languages need guaranteed tail-call optimization,
specialized register/calling conventions, a simple GC interface, and first-class
continuations — none of which LLVM serves well out of the box. Prior LLVM
backends worked around this with trampolining (MLton) or language-specific
calling conventions (GHC, ErLLVM); none had implemented heap-allocated
first-class continuations.

Their solution rests on three mechanisms. **(1) A new calling convention,
"Jump-With-Arguments" (JWA):** it uses all hardware registers, preserves none
across calls, and makes the call and return register conventions identical — so
a continuation throw is just a JWA tail call. Combined with the `naked`
attribute (no prologue/epilogue) and an assembly shim that provisions one
over-sized spill frame per hardware thread (a technique borrowed from SML/NJ),
this delivers the proper tail calls CPS demands. **(2) A simple GC interface:**
because there is no stack to scan, the existing collector needed no changes; the
compiler emits heap-limit checks and saves live roots into a heap object before
a non-tail call to `@invoke-gc`, relying on LLVM's aliasing rules to force
reloads. **(3) First-class labels for preemption:** heap-limit checks double as
safe points; forcing a check to fail lets the runtime capture an implicit
continuation whose code address is a mid-function return point. Since LLVM can't
name such a label, they exploit JWA's matched call/return convention plus a
`@genLabel` assembly shim to manufacture a first-class label — similar in spirit
to Dolan et al.'s SWAPSTACK, but leveraging CPS liveness.

The JWA convention was added in a fork of LLVM (x86-64 only). They also tune
LLVM: the `@llvm.expect` intrinsic keeps cold GC-overflow blocks off the hot
path, and two hand-crafted pass sequences ("Basic" and "Extra") replace the
stock `-Ox` pipelines, which are tuned for C/C++ frontends. Evaluation against
the older MLRISC backend (average of 50 trials) shows LLVM generally produces
smaller, faster code, with large wins on `nbody` (owing to MLRISC's poor
floating-point register allocation) and a regression on parallel `blackscholes`
that appears CPU-specific.

## Why this matters

I am considering writing a [[scheme|Scheme]] implementation that compiles into
[[llvm]] IR, and this paper offers a possible approach — in particular its
handling of guaranteed tail calls and heap-allocated first-class continuations,
which are exactly the features that make LLVM awkward as a functional-language
backend.
