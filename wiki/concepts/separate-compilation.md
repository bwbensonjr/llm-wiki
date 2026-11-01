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

**Redefinition and `eval`.** If any function may be redefined at run time, a compiler cannot inline or resolve a call it does not control. [[world-age-in-julia|Julia's world age]] confines the effect: new definitions become visible only when control returns to the top level, so code compiled for a call can treat the method table as fixed, and programmers opt into fresh definitions explicitly.

**Declaring what may not change.** Languages give the compiler a boundary to optimize within. Common Lisp makes the file that unit: [[clhs-semantic-constraints|CLHS 3.2.2.3]] lets a file compiler assume same-file calls reach the same-file definition, while across files the run-time definition prevails unless `inline` or `ftype` declarations say otherwise. Dylan instead lets a library seal parts of its generic functions and class graph; [[define-sealed-domain|`define sealed domain`]] lets the compiler drop methods other libraries are barred from adding, at the cost that some violations appear only when independently compiled libraries are combined.

**Whole-program compilation and standalone delivery.** [[chez-scheme-system-operations|Chez Scheme]] offers both modes: per-library object files that by default carry inlining information into dependents, and `compile-whole-program`, which folds libraries into one object file, discards unused code, and optimizes across boundaries. The limits are explicit: incorporated libraries stay reachable from `eval` only if requested, initialization that depends on `eval` may not survive linearization, and macro *visit code* can be stripped because it is needed only to compile. At the far end, [[flow-directed-lightweight-closure-conversion|Stalin]] gives up `eval`, the REPL and separate compilation entirely; the closed world lets whole-program flow analysis prove what other compilers are only told by unsafe flags, and the output is a single executable.

**Bundling the runtime instead.** [[raco-exe-creating-stand-alone-executables|Racket's `raco exe`]] produces a standalone executable by embedding a program's modules in a copy of the Racket runtime. It keeps the language fully dynamic, gains no speed, and cannot see what a program reaches through `eval` or `dynamic-require`, so those modules must be declared by hand.

## Sources

- [[composable-and-compilable-macros|Composable and Compilable Macros: You Want It When?]]
- [[world-age-in-julia|World Age in Julia: Optimizing Method Dispatch in the Presence of Eval]]
- [[define-sealed-domain|Define Sealed Domain (Dylan Reference Manual)]]
- [[clhs-semantic-constraints|CLHS 3.2.2.3: Semantic Constraints]]
- [[chez-scheme-system-operations|Chez Scheme User's Guide: System Operations]]
- [[flow-directed-lightweight-closure-conversion|Flow-Directed Lightweight Closure Conversion]]
- [[raco-exe-creating-stand-alone-executables|raco exe: Creating Stand-Alone Executables]]
