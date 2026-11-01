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

## Sources

- [[composable-and-compilable-macros|Composable and Compilable Macros: You Want It When?]]
- [[world-age-in-julia|World Age in Julia: Optimizing Method Dispatch in the Presence of Eval]]
- [[define-sealed-domain|Define Sealed Domain (Dylan Reference Manual)]]
- [[clhs-semantic-constraints|CLHS 3.2.2.3: Semantic Constraints]]
