---
type: concept
title: Dylan
created: 2026-11-01
tags: [programming-languages, language-implementation]
---

# Dylan

A dynamic, object-oriented programming language with multiple dispatch, generic functions and a class system descended from Lisp's, designed so that a compiler can still produce efficient code. Its main tool for that is **sealing**: a library may declare parts of its class graph and generic functions closed to extension by other libraries. Explicitly defined classes and generic functions are sealed by default, and [[define-sealed-domain|`define sealed domain`]] seals narrower slices of a generic function. Within those declarations a compiler can turn generic dispatch into direct calls and treat a library's internals as fixed when compiling code that uses it, which bears on [[separate-compilation]] in dynamic languages.

## Sources

- [[define-sealed-domain|Define Sealed Domain (Dylan Reference Manual)]]
- [[sealing-dylan-reference-manual|Sealing (Dylan Reference Manual)]]
