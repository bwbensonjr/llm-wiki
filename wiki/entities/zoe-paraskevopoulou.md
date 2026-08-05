---
type: entity
status: provisional
title: Zoe Paraskevopoulou
created: 2026-08-05
tags: [programming-languages, formal-methods, program-verification]
---

# Zoe Paraskevopoulou

A researcher in verified compilation, first author with [[andrew-appel|Andrew W. Appel]] of
[[closure-conversion-is-safe-for-space|Closure Conversion Is Safe for Space]] — the
mechanized proof that flat [[closure-conversion|closure conversion]] preserves a program's
time and space consumption, built as part of the **CertiCoq** pipeline from Coq to
assembly.

Her contribution there is a proof technique rather than an optimization: a step-indexed
binary logical relation carrying pre- and postconditions, so resource bounds are
established at the same time as functional correctness. Making it work required confronting
what garbage collection does to such relations — heaps that shrink and get renamed by a
copying collector break the monotonicity ordinary Kripke relations assume — and extending
the result to diverging programs, capturing that a program may run forever in bounded
memory.

## Sources

- [[closure-conversion-is-safe-for-space|Closure Conversion Is Safe for Space]]
