---
type: summary
status: provisional
title: Another Module System for Scheme
created: 2026-11-01
source: inbox-files/rees-another-module-system-for-scheme.md
raw: raw/2026-11-01-another-module-system-for-scheme.md
tags: [scheme, macros, language-implementation, programming-languages]
---

# Another Module System for Scheme

## Summary

[[jonathan-rees|Jonathan Rees]]'s memo (3 January 1993, updated 15 January 1994; HTML at `https://mfleck.cs.illinois.edu/envision/scheme48/module/module.html`) describing the module system of [[scheme-48|Scheme 48]]. The design draws on Standard ML modules and on Scheme Xerox. Its stated aim is to support "both static linking and rapid turnaround during program development". Modules are described in a separate **configuration language**. A module, which can be instantiated as one or more *packages*, exports *structures*: views onto its bindings, each with an *interface*, which acts as the structure's type. A module body can see only the structures its description names in `open` clauses (all of their exports visible) or `access` clauses (reached by qualified `structure-ref`). Even `define-structure` and the `scheme` bindings are visible only if some opened structure provides them.

Two rules matter for compilation. First, assigning with `set!` to an imported or undefined variable is not allowed: a package must `define` a variable before it can assign it. Second, hygienic macros can be exported, and the auxiliary names a macro introduces resolve in the environment where the macro was defined. `delay` expands into a call to `make-promise`, which the `scheme` structure never exports, yet every client reaches the right `make-promise` even if it shadows the name.

The **compiling and linking** section is short and specific. Scheme 48's static linker builds **stand-alone heap images** from module descriptions: the programmer names one procedure in one structure as the entry point, and the linker follows `open` and `access` links to decide what goes into the image. At the time there was no separate compilation, and the linker's only input was source. Rees expected it to be easy to add. The unit of compilation would be one module, not one file. A module could be compiled knowing only its imports' interfaces, except for macros: any structure supplying macros must first be processed far enough to extract their definitions. The main difficulty he names is resolving those auxiliary bindings. The compiler has to pass the loader or linker the search path for each one, so that `make-promise` is found in `delay`'s defining package rather than in the package being loaded.

The development environment takes the opposite approach from the static linker. Configurations can be changed while a program runs: an interface can be edited, a structure replaced, a binding shadowed. Variable references always resolve according to the *current* structures and interfaces, which caching with invalidation keeps fast. A command processor, which keeps meta-level commands separate from the program's own names, provides commands to switch packages, load and reload. The discussion section explains why structures and interfaces are **second-class**: "it must be possible for the compiler and linker to expand macros and resolve variable bindings before the program is executed." Because imported bindings can never be assigned, a module compiled as a block can treat every variable it only defines as never assigned, even if exported, so simple analysis is enough for inlining. It also explains why multi-module programs can be loaded into other Schemes. Scheme 48 can therefore be bootstrapped without itself, unlike Smalltalk-80.

## Why this matters

The memo puts two approaches side by side in one system: a static linker that traces a module graph from an entry point to build a standalone image, and a development environment where any binding can be rebound and is resolved again on every reference. Its account of separate compilation pins down the macro problem the same way [[extending-the-scope-of-syntactic-abstraction|Waddell and Dybvig]] and [[composable-and-compilable-macros|Flatt]] later address it. The rest of a module can be compiled against interfaces, but exported macros cannot, and the bindings they introduce must be resolved in the macro's home package at link time. The ban on assigning to imported variables is a cheap version of what [[sealing-dylan-reference-manual|Dylan's sealing]] declares outright: a guarantee that lets a module compiler treat its own definitions as fixed. All of this bears directly on [[separate-compilation]].
