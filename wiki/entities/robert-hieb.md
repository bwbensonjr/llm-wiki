---
type: entity
status: reviewed
title: Robert Hieb
created: 2026-08-05
tags: [programming-languages, language-implementation, scheme, lisp, continuations]
---

# Robert Hieb

An Indiana University computer scientist who worked on the implementation of
[[scheme]] with [[r-kent-dybvig|R. Kent Dybvig]], and first author of
[[representing-control-in-the-presence-of-first-class-continuations|Representing Control in the Presence of First-Class Continuations]]
— the paper that introduced the
segmented stack model behind [[chez-scheme|Chez Scheme]]'s constant-time
[[first-class-continuations|continuation]] operations.

His work approaches control as a representation problem rather than a compilation one:
the segmented stack answers "what shape should the control stack have" instead of "what
should the compiler translate a capture into," which is why the design transfers to
stack overflow and multiple control threads as readily as it does to `call/cc`. The
same line runs through his work with Dybvig on engines built from continuations and on
concurrent continuations.

## Sources

- [[representing-control-in-the-presence-of-first-class-continuations|Representing Control in the Presence of First-Class Continuations]]
