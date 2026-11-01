---
type: concept
status: provisional
title: Separate Compilation
created: 2026-10-31
tags: [language-implementation, lisp, scheme, programming-languages]
---

# Separate Compilation

Compiling a program's modules or libraries independently, so each can be built once and linked into many programs, as opposed to whole-program compilation, which compiles a program and everything it uses together. In dynamic [[lisp|Lisp]]-family languages it collides with two things the languages value: macros that run arbitrary code inside the compiler, and the ability to redefine or `eval` anything at run time. The same tension governs how a standalone executable is produced, since what may change after compilation decides what can be optimized, pruned or left out.

## Notes

**Macros and phases.** When a library exports macros, importing it means running its code at compile time. [[composable-and-compilable-macros|Flatt's MzScheme module system]] makes that sound by separating compile-time from run-time imports and instantiating a module afresh for each phase and each compilation, so compiled code never depends on what else happened to be loaded, and all compile-time code can be stripped from the finished program.

## Sources

- [[composable-and-compilable-macros|Composable and Compilable Macros: You Want It When?]]
