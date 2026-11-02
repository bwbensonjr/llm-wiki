---
type: summary
title: "Chez Scheme User's Guide: System Operations"
created: 2026-10-31
source: https://cisco.github.io/ChezScheme/csug9.5/system.html
raw: raw/2026-10-31-system-operations.md
tags: [chez-scheme, scheme, language-implementation, programming-languages]
---

# Chez Scheme User's Guide: System Operations

## Summary

Chapter 12 of the [[chez-scheme|Chez Scheme]] Version 9.5 User's Guide, a long reference chapter covering exceptions, interrupts, environments, compilation and loading, source management, timing, profiling and more. Its compilation section (12.4) documents how Chez compiles, links and packages code, which is the part read here.

**`eval` is the compiler.** `eval` hands its argument to the current evaluator, which by default is `compile`: expand, compile to machine code, run. Petite Chez Scheme substitutes the interpreter. So a program that keeps `eval` keeps the expander and compiler (or the interpreter) with it.

**Separate compilation, with information carried across boundaries.** `compile-library` and `compile-program` build object files per library and per R6RS top-level program, and `maybe-compile-*` recompiles only out-of-date files, including, when `compile-imported-libraries` is set, files whose imported libraries changed. `compile-program` returns the libraries the program actually invokes; a program invokes a library only if it references one of its exported variables, so the set can differ from what it imports, and with `library-requirements` and `library-object-filename` it identifies the object files to ship. By default `enable-cross-library-optimization` embeds enough information in a library's object code for its constants and procedures to be propagated and inlined into dependent libraries; turning it off shrinks object files and exposes less near-source information. `verify-loadability` checks, without running anything, that object files and their dependencies are present and from mutually compatible compilation instances, with compile-time dependencies checked for `visit` and run-time ones for `revisit`.

**Whole-program compilation.** With `generate-wpo-files` on, the per-file compilers also write "whole program optimization" (`.wpo`) files. `compile-whole-program` takes a program's wpo file and folds in every library whose wpo file it can find, producing one object file; libraries with only an object file are left to load at run time, and the procedure returns their list, empty when the result is self-contained. It "discards unused code and optimizes across program and library boundaries", with only limited optimization across libraries left outside. Incorporated libraries are visible to `environment` and `eval` only if the `libs-visible?` argument is true, unless something loaded at run time still needs them. It linearizes library initialization by static dependencies only, so initialization that reaches other libraries dynamically through `eval` or `environment` can break, and the fix of adding a static import plus a run-time reference "not in general" suffices. `compile-whole-library` does the same for a library and keeps everything visible.

**Packaging.** `strip-fasl-file` removes source information and library *visit code*, the macro transformers and meta definitions needed only to compile dependent libraries, from object files. `make-boot-file` concatenates object code behind a header naming the base boot files it depends on (ultimately `petite.boot`); boot files load explicitly or by the name of the executable.

## Why this matters

The chapter shows a production Scheme answering both halves of the question with explicit knobs rather than a single policy. Separate compilation is the default, with optional cross-library inlining; whole-program compilation is a second pass that prunes and optimizes only as far as the declared `eval` visibility allows, and fails to preserve initialization orders that depend on `eval`. Visit code is strippable because it is needed only to compile, not to run. Each of those knobs corresponds to one of the reasons a dynamic Lisp resists [[separate-compilation]] and standalone delivery, so the chapter works as a checklist of design decisions an LLVM-backed Scheme would face.
