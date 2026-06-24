---
type: concept
title: Racket
created: 2026-06-24
tags: [racket, lisp, programming-languages]
---

# Racket

A programming language and 20-year research project (begun January 1995, first
as PLT Scheme / MzScheme) in the [[lisp]] and Scheme tradition, designed as a
platform for [[language-oriented-programming]]. Available at
[http://racket-lang.org/](http://racket-lang.org/).

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

## Sources

- [[a-programmable-programming-language|A Programmable Programming Language]]
