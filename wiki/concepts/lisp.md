---
type: concept
status: reviewed
title: Lisp
created: 2026-06-23
tags: [lisp, programming-languages]
---

# Lisp

The family of parenthesized, expression-oriented programming languages built on
s-expressions (code as data) and powerful macro systems.

## Notes

[[janet|Janet]] is a modern, practically-minded dialect that deliberately breaks
with older Lisp conventions (`first` over `CAR`, `do` over `PROGN`, `fn` over
`LAMBDA`, real Booleans, and `nil` as its own type rather than the empty list).
[[scheme|Scheme]] is the small, lexically-scoped dialect now covered on its own
page — the trunk from which [[racket|Racket]] descends. [[racket|Racket]] is an
heir of Scheme that eliminates the boundary between library and language to
support [[language-oriented-programming]]. Other notable dialects — Common Lisp
and Clojure — are not yet covered in this wiki; when a source on one is filed,
give it its own concept page and link it back here.

The shared throughline across the family is the macro system: because code is
represented as ordinary data structures, programs can manipulate and generate
code at compile time. [[rabbit-a-compiler-for-scheme|RABBIT]] makes the strongest
version of this argument: if the primitive basis set is small enough, nearly
every "language feature" is a macro over it, and a handful of source-to-source
transformations compile the result as well as a conventional compiler would.

## Sources

- [[why-janet|Why Janet?]]
- [[the-janet-programming-language|The Janet Programming Language]]
- [[a-programmable-programming-language|A Programmable Programming Language]]
- [[libscheme-scheme-as-a-c-library|libscheme: Scheme as a C Library]]
- [[porting-racket-to-chez-scheme|Porting Racket to Chez Scheme]]
- [[rabbit-a-compiler-for-scheme|RABBIT: A Compiler for Scheme]]
- [[orbit-an-optimizing-compiler-for-scheme|ORBIT: An Optimizing Compiler for Scheme]]
- [[an-incremental-approach-to-compiler-construction|An Incremental Approach to Compiler Construction]]
- [[lambda-the-ultimate-label-a-simple-optimizing-compiler-for-scheme|Lambda, the Ultimate Label: A Simple Optimizing Compiler for Scheme]]
- [[a-tractable-native-code-scheme-system|A Tractable Native-Code Scheme System]]
- [[hygienic-macro-technology|Hygienic Macro Technology]]
