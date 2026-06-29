---
type: concept
title: Scheme
created: 2026-06-29
tags: [scheme, lisp, programming-languages]
---

# Scheme

A small, lexically-scoped dialect of [[lisp|Lisp]] built on the principle that a
language should not include "everything but the kitchen sink," but rather
provide a minimal framework in which it is easy to build the kitchen sink. A
very small number of expression-forming rules, freely composed, suffice for a
practical language supporting functional, procedural, and object-oriented
styles, with first-class procedures (closures), high-level data types, and
automatic memory management.

## Notes

Scheme's conceptual simplicity makes it a natural extension and scripting
language: it can be implemented in relatively little code while still offering
lexical scope, nested procedures, and real data types. [[libscheme-scheme-as-a-c-library|libscheme]]
exploits exactly this, packaging Scheme as an embeddable C library in the mold
of Tcl.

Scheme is the trunk of a lineage already present in this wiki:

- [[racket|Racket]] is an heir of Scheme — it began life in January 1995 as PLT
  Scheme / MzScheme, and MzScheme was bootstrapped from
  [[libscheme-scheme-as-a-c-library|libscheme]]'s code. Racket pushes Scheme's
  macro system toward a full platform for [[language-oriented-programming]].
- [[janet|Janet]] is a modern, Scheme-influenced Lisp that, like libscheme, is
  designed to embed cleanly into C — a parallel solution to the same
  extension-language problem two decades later.
- [[chez-scheme|Chez Scheme]] is a high-performance, R6RS Scheme implementation
  whose optimizing compiler and continuation support made it a good target VM —
  [[racket|Racket]] now runs on it (see
  [[porting-racket-to-chez-scheme|Porting Racket to Chez Scheme]]).

The defining Scheme features are lexical scope, first-class procedures that
close over their free variables, and a macro/syntax system more powerful than
C-style token substitution. Standardized in the Revised^n Reports on the
Algorithmic Language Scheme.

## Sources

- [[libscheme-scheme-as-a-c-library|libscheme: Scheme as a C Library]]
- [[porting-racket-to-chez-scheme|Porting Racket to Chez Scheme]]
