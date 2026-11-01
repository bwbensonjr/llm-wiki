---
type: summary
status: provisional
title: "Common Lisp Cookbook: Scripting, Command-Line Arguments, Executables"
created: 2026-10-31
source: https://lispcookbook.github.io/cl-cookbook/scripting.html
raw: raw/2026-10-31-scripting-command-line-arguments-executables.md
tags: [lisp, language-implementation, programming-languages]
---

# Common Lisp Cookbook: Scripting, Command-Line Arguments, Executables

## Summary

A practical chapter of the community Common Lisp Cookbook on running [[lisp|Common Lisp]] programs from the terminal, as scripts and as self-contained executables. Scripts use a shebang such as `#!/usr/bin/env -S sbcl --script` and start in about 0.03 s, but slow down as dependencies are loaded. A file has no `main` function: loading it executes every top-level form, so the entry point is simply a top-level call, wrapped in `eval-when (:execute)` so the file can still be compiled and loaded from the editor without side effects. Loading a Quicklisp dependency in mid-script needs `eval-when` too, because the reader sees a package that does not exist yet; the chapter recommends an ASDF system definition instead.

The executable story is **image dumping**. In SBCL, after loading the program and its dependencies, `sb-ext:save-lisp-and-die` with `:executable t` and a `:toplevel` entry function writes the running Lisp heap out as a binary. It cannot be done with multiple threads running, so not from inside SLIME; builds run from a plain REPL or a Makefile. The mechanism is implementation-specific (CCL calls it `ccl:save-application`), so portable builds use `uiop:dump-image` or ASDF's `program-op` via `asdf:make`. The Deploy library goes further, collecting the foreign C libraries (such as `libssl`) the program needs into a `bin/` directory, since a dumped image still links to shared libraries wherever the build machine kept them.

The chapter is frank about the trade. Implementations "all create self-contained executables" that start almost instantly, but open-source ones are large, because they include "the whole Lisp including its libraries, the names of all symbols, information about argument lists to functions, the compiler, the debugger, source code location information", with the upside that a running program can still compile and load Lisp code. A comparison table has SBCL at about 48 MB with 6 ms startup, CCL about half that size, and ECL, which compiles Lisp to C, an order of magnitude smaller but slower to start (about 0.5 s). LispWorks' paid edition offers a **tree shaker** that strips unused code (an 8 MB hello-world). SBCL's zstd core compression cuts a 46 MB hello-world to 11 to 12 MB, and an application from 120 MB to 23 MB, for about a dozen milliseconds of startup. A custom **core image** with dependencies preloaded gives scripts fast startup without a full executable.

## Why this matters

This is the default Common Lisp answer to standalone executables, and it sidesteps [[separate-compilation]] altogether: load everything into one live image, then freeze the heap. That is why the result is large and why it keeps the compiler, the opposite trade from [[flow-directed-lightweight-closure-conversion|Stalin's]] closed-world binary, and why tree shaking, which must decide what a program can never reach, is a premium feature. It sits alongside [[janet|Janet's]] snapshot of program state and [[raco-exe-creating-stand-alone-executables|Racket's runtime bundling]] as a third way to ship a dynamic Lisp.
