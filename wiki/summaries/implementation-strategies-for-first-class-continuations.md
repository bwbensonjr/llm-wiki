---
type: summary
status: reviewed
title: Implementation Strategies for First-Class Continuations
created: 2026-08-05
source: https://doi.org/10.1023/A:1010016816429
raw: raw/2026-08-05-a-1010016816429.md
tags: [programming-languages, language-implementation, scheme, lisp, continuations]
---

# Implementation Strategies for First-Class Continuations

## Summary

[[william-clinger|William D. Clinger]], Anne H. Hartheimer, and Eric M. Ost survey and
measure the ways a language can implement
[[first-class-continuations|first-class continuations]]. Because [[scheme]] and
Smalltalk-80 continuations may have unlimited extent, the purely stack-based
implementation that suffices for most languages is inadequate; the paper's job is to
lay out the alternatives and say what each actually costs.

**The cost framework** is the paper's organizing contribution. It separates:

- **Direct cost** — machine instructions to create one continuation frame, link it to
  the continuation being extended, and dispose of it. As a rough rule of thumb the
  authors assume one continuation frame per hundred instructions executed, which is
  what makes direct cost commensurable across strategies.
- **Indirect costs** — everything else, and the paper devotes a long section to them:
  cache misses, failure to reuse frames, inability to allocate mutable variables in
  frames, stack-cache overflow and underflow, and copying and sharing.

A strategy is called **zero-overhead** if its calling sequence matches a conventional
stack implementation of a language without first-class continuations — that is, if
programs that never use `call/cc` pay nothing.

**Three scenarios** span the behavior space: programs using no first-class
continuations at all; programs creating a few escape procedures for non-local exits;
and the *recapture scenario*, where many frames are captured repeatedly. Most real
programs fall somewhere along that spectrum, and the scenarios are what separate
strategies that otherwise look similar.

**The strategies**, each given typical PowerPC code for a non-tail call, a
zero-overhead verdict, per-scenario performance, at least one primary indirect cost,
and a naming of the earliest implementation known to use it: garbage-collection,
spaghetti, heap, stack, chunked-stack, stack/heap, **incremental stack/heap**, the
**Hieb-Dybvig-Bruggeman** variation, one-shot continuations, and Mateu's coroutines.

Two recur across the implementations this wiki covers. The **incremental stack/heap**
strategy keeps frames in a stack cache with a permanent frame at the bottom whose
return address points to
system code; returning through a frame not in the cache traps and copies it back in.
It is zero-overhead, shares the stack strategy's calling sequence, and in the
recapture scenario — where capturing a previously captured frame is more common than
returning through one — approaches stack/heap performance. Its price is that mutable
variables cannot live in a continuation frame. The paper names
[[a-tractable-native-code-scheme-system|Scheme 48]] and [[larceny]] as its users. The
**Hieb-Dybvig-Bruggeman** variation, used by [[chez-scheme|Chez Scheme]], replaces the
single cache with multiple heap-allocated stack segments, the current one serving as
the cache. It extends naturally to *one-shot* continuations, which are not first-class
but suffice for non-local exits and multitasking — and which is what the exception and
thread facilities of C++ and Java rest on.

Later sections cover Appel and Shao's estimates for copying and sharing,
**observational equivalence** between strategies, continuation-intensive benchmarks,
multitasking (which the authors note *creates* a recapture scenario), and difficulty
of implementation.

**The conclusion** is measured rather than triumphal: on most programs the
zero-overhead strategies beat the garbage-collection strategy, but *all* strategies
have indirect costs. The incremental stack/heap strategy is singled out as performing
well and not being hard to implement, with Hieb-Dybvig-Bruggeman and stack/heap also
attractive.

The acknowledgments record where the idea came from. Algol 60 technique used a single
stack for both environments and continuations; during 1982–83 Jonathan Rees pointed
out that environments could be dropped from that stack entirely by assuming all
variables live in registers or heap storage, and that insight is what produced the
stack/heap and incremental stack/heap strategies.

## Why this matters

The inbox note asked for compilation approaches to Scheme continuations, and this is
the paper the rest of the corpus has been citing. Its reference
number [5] is what
[[lambda-the-ultimate-label-a-simple-optimizing-compiler-for-scheme|Twobit]] points at
when it claims the incremental stack/heap strategy has zero overhead — a claim the
[[larceny]] hub already repeats. That claim now has its source, and the source is more
careful than the citation: zero overhead means the *calling sequence* matches a
conventional stack, not that the strategy is free. Its indirect cost — mutable
variables barred from continuation frames — is real and named.

It also turns several scattered implementation details in this wiki into instances of
one taxonomy. Scheme 48's stack cache with a dummy bottom frame and an underflow
handler, Larceny's identical arrangement, and
[[the-development-of-chez-scheme|Chez Scheme's]] progression from copying the whole
stack (Versions 1–2) to a segmented mechanism with constant-time operations (Versions
3–4) are not three unrelated engineering stories: they are the incremental stack/heap
strategy, the same strategy again, and the Hieb-Dybvig-Bruggeman variation. Bob Hieb,
whose death in 1992 Dybvig records in the Chez history, is the first name on that
variation.

The methodological point is worth as much as the taxonomy. By separating direct from
indirect cost and testing against three scenarios rather than one benchmark suite, the
paper makes visible that a strategy can win decisively in one usage pattern and lose in
another — so "which continuation implementation is fastest" is not a well-posed
question without saying what the program does. That is a sharper version of the caution
Twobit raises about benchmarks measuring the collector rather than the compiler, and it
comes from the same author.
