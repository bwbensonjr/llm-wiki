---
type: entity
status: reviewed
title: Richard Kelsey
created: 2026-08-05
tags: [programming-languages, language-implementation, scheme, lisp]
---

# Richard Kelsey

A Scheme implementer whose work reaches across compiler lineages this wiki covers: he
wrote the front end of [[orbit-an-optimizing-compiler-for-scheme|ORBIT]] on Yale's
[[t-programming-language|T]] project, and is a co-author of
[[scheme-48|Scheme 48]] and its native-code compiler.

## Notes

At Yale he was part of the T group alongside Norman Adams,
[[david-kranz|David Kranz]], Jim Philbin, and Jonathan Rees, under Paul Hudak.
Within ORBIT he was
responsible for the front end through early binding, while Kranz took closure
analysis, register allocation, and code generation.

His later work on Scheme 48 carries a recognizable continuity of method. ORBIT's
front end and Scheme 48's Transformational Compiler both organize compilation around
a [[continuation-passing-style|CPS]] intermediate representation, and Scheme 48
pushes the idea further by using a *single* CPS IR across Pre-Scheme compilation,
Scheme compilation, and byte-code optimization. The through-line is treating the
intermediate representation as shared infrastructure rather than one compiler's
private detail.

That the same person is behind both makes [[t-programming-language|T]] and
[[scheme-48|Scheme 48]] branches of one lineage rather than independent systems — a
connection worth holding onto when reading either.

## Sources

- [[orbit-an-optimizing-compiler-for-scheme|ORBIT: An Optimizing Compiler for Scheme]]
- [[a-tractable-native-code-scheme-system|A Tractable Native-Code Scheme System]]
