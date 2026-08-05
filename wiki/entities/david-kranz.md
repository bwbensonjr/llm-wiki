---
type: entity
status: reviewed
title: David A. Kranz
created: 2026-08-05
tags: [programming-languages, language-implementation, scheme, lisp]
---

# David A. Kranz

A computer scientist who, in his 1988 Yale dissertation, built ORBIT — the
optimizing compiler for the [[t-programming-language|T]] dialect of [[scheme]] —
and showed that a higher-order language can be compiled as efficiently as Pascal.

## Notes

Kranz was a member of Yale's T project alongside Norman Adams, Richard Kelsey,
Jim Philbin, and Jonathan Rees, advised by Paul Hudak. Within ORBIT he was
responsible for [[closure-conversion|closure analysis]], register allocation, and
code generation; Kelsey wrote the front end through early binding and Adams the
assembler.

His central claim is that the performance penalty long attributed to first-class
procedures is an artifact of conventional compiler technology rather than a
property of the languages, and that the fix is to treat closures as the
fundamental object of analysis, recovering loops as a special case rather than
the reverse.

## Sources

- [[orbit-an-optimizing-compiler-for-scheme|ORBIT: An Optimizing Compiler for Scheme]]
