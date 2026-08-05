---
type: concept
status: reviewed
title: Janet
created: 2026-06-23
tags: [janet, lisp, programming-languages]
---

# Janet

A small, practical [[lisp|Lisp]] dialect with an imperative core, first-class
functions, and a tiny standard library, designed to be easy to embed and to
compile into self-contained native executables.

## Notes

Janet leans toward practical use over Lisp tradition. Its core is eight special
forms with macros layered on top; runtime semantics are close to JavaScript with
value types. Distinctive strengths called out by [[ian-henry|Ian Henry]]:
self-contained native binaries (Janet compiles to bytecode embedded in a
generated C file, then through the system C compiler), parsing expression
grammars (PEGs) in place of regular expressions, an `sh` subprocess-scripting DSL
that rivals Bash, easy C embedding, mutable/immutable collection types, and
non-hygienic but referentially-transparent macros (via unquoting literal
functions).

Its most unusual feature is passing values from compile time to run time: Janet
runs top-level code at compile time and snapshots the full program state
(including shared references, generators, and closures) to disk, to be resumed
later — enabling precomputation, asset embedding, and code generation without
macros. The free book *Janet for Mortals* (janet.guide) is the author's
book-length treatment.

Implemented mostly in standard C99 and portable across Windows, Linux, and
macOS, Janet is more "batteries-included" than most embeddable languages —
shipping threading, networking, an event loop, subprocess handling, green
threads, and Erlang-style supervision trees — with a 600+ function core library
and a companion build tool, `jpm`, for producing standalone executables.

## Sources

- [[why-janet|Why Janet?]]
- [[the-janet-programming-language|The Janet Programming Language]]
