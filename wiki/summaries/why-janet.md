---
type: summary
status: reviewed
title: Why Janet?
created: 2026-06-23
source: https://ianthehenry.com/posts/why-janet/
raw: raw/2026-06-23-why-janet.md
tags: [janet, lisp, programming-languages]
---

# Why Janet?

## Summary

A sales pitch by [[ian-henry|Ian Henry]] for [[janet|Janet]], a small
[[lisp|Lisp]] dialect that has become his go-to language for side projects and
the subject of his free book *Janet for Mortals*. The article argues for Janet
through a sequence of strengths:

- **Simplicity** — an imperative language with first-class functions, a single
  namespace, and lexical scoping; the core is just eight special forms (`do`,
  `def`, `var`, `set`, `if`, `while`, `break`, `fn`), with macros supplying
  higher-level control flow. Runtime semantics resemble JavaScript "minus all
  the wats," and the standard library fits on one page.
- **Distributability** — Janet compiles to bytecode embedded in a generated C
  file that bundles the runtime, then hands it to the system C compiler,
  yielding self-contained native executables (<1 MB) that need no separate Janet
  install.
- **Text parsing** — instead of regular expressions, Janet uses *parsing
  expression grammars* (PEGs): composable, first-class parsers that handle
  multi-line text, non-regular languages (HTML, JSON), and even binary formats.
- **Subprocess scripting** — a third-party `sh` library provides a shell-scripting
  DSL with pipes and redirects, making Janet a credible alternative to Bash for a
  surprising range of programs.
- **Embeddability** — the runtime is a small C library, so Janet embeds easily
  into other programs and even websites to expose programmable DSLs.
- **Value semantics** — collections come in mutable (`@`-prefixed, reference
  semantics) and immutable (value semantics) flavors, with immutable composite
  values built into the standard library.
- **Macros** — the author's real reason to learn Janet. They are unhygienic and
  share one namespace, but unquoting literal functions makes referentially
  transparent macros possible — a simple solution to a delicate problem.
- **Compile-time to run-time values** — Janet's most distinctive feature:
  top-level code runs at compile time, then the full program state (shared
  references, generators, closures) is snapshotted to disk and resumed at run
  time. This enables precomputation, embedding assets, and code generation (e.g.
  autogenerating database bindings from a SQL schema) — no macros required.
- **Syntax and conventions** — pervasive parentheses broken up by `[]` and `{}`,
  `@` for mutable literals, `|(+ 1 $)` function shorthand, `;` splats,
  arbitrary-backtick strings, `&` rest params, and no reader macros (so the
  syntax is fixed). Janet also abandons Lisp tradition: `first` not `CAR`, `do`
  not `PROGN`, `fn` not `LAMBDA`, real Booleans, and `nil` as its own type rather
  than the empty list.

## Why this matters

This matters to me because I am always interested in the Lisp family of
languages, and Janet seems like it leans into practical usage rather than
theoretical.
