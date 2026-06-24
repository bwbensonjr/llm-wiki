---
type: concept
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
[[racket|Racket]] is another dialect now covered here: an heir of Scheme that
eliminates the boundary between library and language to support
[[language-oriented-programming]]. Other notable dialects — Common Lisp and
Clojure — are not yet covered in this wiki; when a source on one is filed, give
it its own concept page and link it back here.

The shared throughline across the family is the macro system: because code is
represented as ordinary data structures, programs can manipulate and generate
code at compile time.

## Sources

- [[why-janet|Why Janet?]]
- [[the-janet-programming-language|The Janet Programming Language]]
- [[a-programmable-programming-language|A Programmable Programming Language]]
