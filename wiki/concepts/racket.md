---
type: concept
title: Racket
created: 2026-06-24
tags: [racket, lisp, programming-languages]
---

# Racket

A programming language and 20-year research project (begun January 1995, first
as PLT Scheme / MzScheme) in the [[lisp]] and [[scheme|Scheme]] tradition,
designed as a platform for [[language-oriented-programming]]. Available at
[http://racket-lang.org/](http://racket-lang.org/).

Its 1995 starting point was a fusion of two off-the-shelf C/C++ libraries — a
Scheme interpreter ([[libscheme-scheme-as-a-c-library|Benson 1994]]) and a
cross-platform GUI toolkit — per [[porting-racket-to-chez-scheme|Porting Racket
to Chez Scheme]], which is the source for that lineage.

## Notes

Racket's guiding principle is to empower programmers to create new programming
languages easily and add them to a codebase with a friction-free process. Its
defining moves:

- **Library/language boundary erased** — new linguistic constructs are imported
  as seamlessly as functions and classes; the `class` system and `for` loops are
  themselves plain library imports.
- **Per-module language declaration** — every module names its language on the
  first line (`#lang ...`), like a shell script, so installing a language is
  just writing a module that provides its services.
- **Modular, hygienic syntax system** — an improvement over Scheme's macros
  (themselves an improvement over Lisp's tree transformation), allowing
  constructs to be added, reinterpreted, or subtracted incrementally.
- **A spectrum of soundness** — from unsound C-level FFI veneers, through
  runtime checks and higher-order contracts with blame, to static
  [[type-systems]] like `typed/racket`.
- **Internalized OS services** — sandboxes, inspectors, and custodians become
  language constructs rather than escapes to the operating system.

Variants include `racket/base` (core), `racket` ("batteries included"), and
`typed/racket` (typed). Used in practice by Sony's Naughty Dog studio for a
language-oriented game-development framework.

As of "Racket CS," the implementation was rebuilt to run on
[[chez-scheme|Chez Scheme]] in place of its original C runtime, for
maintainability and a stronger functional-language substrate — see
[[porting-racket-to-chez-scheme|Porting Racket to Chez Scheme]].

## Sources

- [[a-programmable-programming-language|A Programmable Programming Language]]
- [[porting-racket-to-chez-scheme|Porting Racket to Chez Scheme]]
