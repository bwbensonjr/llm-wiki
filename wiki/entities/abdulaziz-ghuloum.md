---
type: entity
status: reviewed
title: Abdulaziz Ghuloum
created: 2026-08-05
tags: [programming-languages, language-implementation, scheme, lisp]
---

# Abdulaziz Ghuloum

A Scheme implementer, then at Indiana University, best known for the 2006 paper
and extended tutorial "An Incremental Approach to Compiler Construction".

## Notes

Ghuloum's pedagogical claim is that compiler construction only looks like wizardry
because the literature offers nothing between toy compilers and industrial
optimizers. His answer is a compiler for a large [[scheme]] subset targeting real
x86 assembly, developed as 24 incremental steps, each producing a fully working
compiler for a progressively larger language — so the learner has something that
runs from the first day.

He worked in R. Kent Dybvig's orbit at Indiana; the paper thanks Dybvig and draws
on his group's work, including the storage-management techniques used in
[[chez-scheme|Chez Scheme]].

## Sources

- [[an-incremental-approach-to-compiler-construction|An Incremental Approach to Compiler Construction]]
