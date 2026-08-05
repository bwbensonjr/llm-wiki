---
type: summary
status: reviewed
title: "libscheme: Scheme as a C Library"
created: 2026-06-29
source: https://github.com/bwbensonjr/libscheme/blob/main/src/doc/libscheme.md
raw: raw/2026-06-29-libscheme.md
tags: [scheme, lisp, programming-languages]
---

# libscheme: Scheme as a C Library

## Summary

[[scheme|Scheme]] is a small, lexically-scoped dialect of [[lisp|Lisp]] often
seen as an ideal extension/scripting language. **libscheme** makes Scheme
available as a C library: its interface is a single C header, and it is easily
extended with new primitive procedures, new primitive types, and new syntax. It
is portable to any system with an ANSI C compiler and Hans Boehm's conservative
garbage collector.

The design explicitly learns from Tcl's success — Tcl became the de facto
extension language largely because it embeds into C through a single header and
library archive, and is easily extended with new primitive commands. libscheme
aims for the same embeddability while offering Scheme's advantages over Tcl for
writing scripts: lexical scope, nested procedures, a richer set of real data
types (rather than Tcl's "everything is a string"), and extensible syntax via
`defmacro`.

**Architecture.** Beyond a small kernel (memory management, error handling, and
evaluation), every Scheme primitive is implemented the same way as a user
extension — the same strategy Tcl uses. Every value is a `Scheme_Object` (a
pointer to a type object plus a two-word union; larger or foreign structures are
stored separately and reached through a `ptr_val` field). Primitive procedures
are C functions taking `(argc, argv)`, each responsible for checking its own
argument count and types; syntax forms instead receive their *unevaluated* form
plus an environment, so they can choose what to evaluate (the `if` special form
is the worked example, since it must not evaluate all of its arguments). Users
register new types at runtime with `scheme_make_type()` and new globals with
`scheme_add_global()`. An environment (`Scheme_Env`) is a global hash table plus
chained local frames (parallel symbol/value vectors); lookup walks the frame
chain and falls back to the global table. The interpreter interface is
`scheme_read` / `scheme_eval` / `scheme_write` / `scheme_display`; errors are
raised with `scheme_signal_error()` or a failed `SCHEME_ASSERT()` and caught
with `SCHEME_CATCH_ERROR()`. Memory is managed by the Boehm/Demers conservative
collector, which application and extension writers are encouraged to use too.

**Example application.** `dwarfscheme` embeds libscheme alongside the libdwarf
library to give an interactive Scheme read-eval-print loop for browsing DWARF
debugging information in an object file. The paper walks through the boilerplate
REPL `main()`, the initialization routine that registers DWARF types and
primitives, and a sample primitive (`dwarf-first-die`) that checks its argument,
extracts the foreign pointer, calls into libdwarf, and returns a new tagged
object or Scheme false.

**Assessment.** libscheme is simple to understand and use and builds on Scheme's
powerful semantics, but the interpreter is slow — an inefficient
function-calling sequence dynamically allocates needless garbage — though
adequate for the interactive and scripting use it targets. Planned future work
included POSIX, socket, and regular-expression bindings. At publication it was
being used by the DNPAP team at Delft University of Technology in an ethernet
monitor, and distributed via the Scheme Repository at `ftp.cs.indiana.edu`.

*Published in the USENIX 1994 Very High Level Languages Symposium Proceedings
(October 26–28, 1994, Santa Fe, New Mexico).
Author: [[brent-benson|Brent W. Benson Jr.]], Harris Computer Systems.*

## Why this matters

This is important to me because I want to view it in the context of the other
Scheme implementations and papers that I'll add to the llm-wiki over time.
