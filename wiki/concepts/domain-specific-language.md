---
type: concept
status: reviewed
title: Domain-Specific Language
created: 2026-06-24
tags: [domain-specific-languages, programming-languages]
---

# Domain-Specific Language

A programming language specialized to a particular problem domain, letting
developers express solutions in the vocabulary of that domain rather than in a
general-purpose language. An **embedded** DSL (eDSL) is one hosted inside a
general-purpose language — e.g. jQuery or React in JavaScript.

## Notes

eDSLs are the building blocks that [[language-oriented-programming]] composes:
developers solve each aspect of a problem in an appropriate eDSL, then combine
those components into one multilingual system. The article notes that
multilingual eDSL programming is traditionally done ad hoc and cumbersomely —
stepping outside the host language to run configuration files, compilers, and
linkers — which [[racket]] aims to make friction-free.

Worked Racket examples include `video` (a declarative eDSL for editing
conference-talk recordings), `typed/video` (adding a type system, built with the
`turnstile` eDSL for [[type-systems]]), `video/ffi` (an eDSL for multimedia
foreign-function bindings), and `shill` (a secure scripting language).

## Sources

- [[a-programmable-programming-language|A Programmable Programming Language]]
