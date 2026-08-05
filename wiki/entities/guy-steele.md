---
type: entity
status: reviewed
title: Guy L. Steele Jr.
created: 2026-08-05
tags: [programming-languages, language-implementation, scheme, lisp]
---

# Guy L. Steele Jr.

A computer scientist who, with Gerald Jay Sussman, invented [[scheme]] at MIT in
1975. Author of the RABBIT compiler and, with Sussman, of the
[[lambda-papers|Lambda Papers]].

## Notes

Steele's 1977 MIT dissertation, published as *RABBIT: A Compiler for SCHEME*,
established [[continuation-passing-style]] as a compiler intermediate
representation and argued that a procedure call is a `GOTO` that passes
arguments — that `LAMBDA` is "rename plus GOTO." His companion paper "Debunking
the 'Expensive Procedure Call' Myth" pressed the same point: the cost of function
calls is an implementation artifact, not a property of abstraction.

His recurring method is to shrink a language to a small
[[lambda-calculus]]-shaped basis set and recover the rest through macros, then
show that a handful of source-to-source transformations optimize the result as
well as a conventional compiler would.

## Sources

- [[rabbit-a-compiler-for-scheme|RABBIT: A Compiler for Scheme]]
- [[lambda-the-ultimate-label-a-simple-optimizing-compiler-for-scheme|Lambda, the Ultimate Label: A Simple Optimizing Compiler for Scheme]]
- [[hygienic-macro-technology|Hygienic Macro Technology]]
