---
type: concept
status: reviewed
title: Lambda Calculus
created: 2026-08-05
tags: [programming-languages, language-implementation]
---

# Lambda Calculus

Alonzo Church's formal system of function abstraction and application, and the
semantic model that the [[scheme]]/[[lisp]] line of languages deliberately
mirrors.

## Notes

Two of its conversion rules do direct work in compilers. **Alpha-conversion** —
renaming a bound parameter and all its references without changing meaning —
implies that a compiler can locate every reference to a variable, which under
lexical scoping means it may lay out run-time environments however it likes.
**Beta-conversion** — substituting an argument expression for a parameter
reference in a function body — is the substitution step that drives
source-to-source optimization, subject to avoiding name capture and side-effect
reordering.

[[tail-recursion]] follows indirectly from the same axioms, which is what lets
iteration be expressed applicatively. Steele's slogan that `LAMBDA` is "rename
plus GOTO" is a compiler-writer's reading of exactly these two rules.

## Sources

- [[rabbit-a-compiler-for-scheme|RABBIT: A Compiler for Scheme]]
- [[hygienic-macro-technology|Hygienic Macro Technology]]
