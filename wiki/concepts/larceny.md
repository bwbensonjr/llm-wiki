---
type: concept
status: reviewed
title: Larceny
created: 2026-08-05
tags: [programming-languages, language-implementation, scheme, lisp]
---

# Larceny

An implementation of IEEE/ANSI [[scheme]] built on the Twobit compiler, written by
Lars Thomas Hansen under [[william-clinger|William Clinger]]'s direction, and used
as a research vehicle for studying how programming style affects performance —
especially garbage-collection performance.

## Notes

Larceny's architecture follows from Twobit's: the compiler targets a hypothetical
register-based *MacScheme machine* whose instruction set was designed for effective
peephole optimization, and a table-driven optimizing assembler lowers that to SPARC
machine code (a second assembler emits byte code for an interpreter). Branch delay
slots are filled by the standard trick of moving the branch target into the slot and
annulling the branch.

For first-class continuations it uses the **incremental stack/heap strategy**:
continuation frames are allocated in a stack cache with a dummy frame at the bottom
whose return address invokes an underflow handler, which copies one frame back from
the heap and returns through it. The authors claim zero overhead relative to
conventional stack allocation when `call/cc` is not used. The strategy is fragile in
one specific way — it requires that *every* continuation frame correspond to some
procedure call, which is why Twobit's original habit of allocating separate spill
frames is described as a major design error.

Larceny can be configured with any of three interchangeable garbage collectors, and
flushes the stack cache on every collection. Its benchmark profile against
[[chez-scheme|Chez Scheme]], Allegro Common Lisp, and
[[standard-ml|Standard ML of New Jersey]] mostly reflects collector behavior rather
than compiler quality — a point the authors make themselves, arguing that allocation
and collection dominate compiler optimization for this class of language.

## Sources

- [[lambda-the-ultimate-label-a-simple-optimizing-compiler-for-scheme|Lambda, the Ultimate Label: A Simple Optimizing Compiler for Scheme]]
