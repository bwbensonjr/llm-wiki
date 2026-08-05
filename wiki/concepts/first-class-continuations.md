---
type: concept
status: provisional
title: First-Class Continuations
created: 2026-08-05
tags: [programming-languages, language-implementation, scheme, lisp, continuations]
---

# First-Class Continuations

A continuation reified as an ordinary value with unlimited extent — capturable,
storable, and invocable any number of times. Because it can outlive the call that
created it, the control stack that represents it cannot simply be popped, which is
what makes implementation hard.

## Notes

The distinction that matters is *extent*. In most languages a continuation has
dynamic, nested extent and a stack suffices. In [[scheme]] and Smalltalk-80 (where
they are called contexts) a continuation may become a first-class object of unlimited
lifetime, so a purely stack-based implementation is inadequate — and yet almost all
programs never capture one, so any implementation that taxes ordinary calls to support
the rare capture is paying in the wrong place.

That tension produces the central design goal: a **zero-overhead** strategy, one whose
calling sequence is identical to a conventional stack implementation of a language
without first-class continuations. Programs that never use `call/cc` then pay nothing.

Clinger, Hartheimer, and Ost
([[implementation-strategies-for-first-class-continuations|Implementation Strategies]])
survey the alternatives and supply the vocabulary for comparing them. They
separate **direct cost** — instructions to create, link, and dispose of one frame —
from **indirect costs** such as cache misses, inability to reuse frames, the barring
of mutable variables from frames, cache overflow and underflow, and copying. And they
insist on three usage scenarios rather than one benchmark: programs that never capture,
programs that create a few escape procedures for non-local exits, and the *recapture
scenario* where frames are captured repeatedly. A strategy can win one and lose
another, so the question "which is fastest" is ill-posed without saying what the
program does.

**The strategies this wiki's systems actually use:**

- The **incremental stack/heap** strategy keeps frames in a stack cache with a
  permanent bottom frame whose return address invokes an underflow handler; returning
  through a frame that is not cached traps and copies it back. Zero-overhead, good in
  the recapture scenario, and used by both [[a-tractable-native-code-scheme-system|Scheme 48]]
  and [[larceny]]. Its price: mutable variables cannot live in a continuation frame.
- The **Hieb-Dybvig-Bruggeman** variation, used by [[chez-scheme|Chez Scheme]], swaps
  the single cache for multiple heap-allocated stack segments, the current segment
  acting as the cache. Its own paper,
  [[representing-control-in-the-presence-of-first-class-continuations|Representing Control in the Presence of First-Class Continuations]],
  gives the mechanism: capture seals the occupied part of the current segment and copies
  nothing, reinstatement copies one segment after splitting it to stay under a copy
  bound, and stack overflow and underflow are handled as an implicit capture and an
  implicit reinstatement. [[the-development-of-chez-scheme|Chez]] arrived here by
  stages — Versions 1 and 2 copied the entire stack on capture, which made the cost
  proportional to stack depth, and Versions 3 and 4 moved to segments and
  constant-time operations.
- **One-shot continuations** are not first-class, but they cover non-local exits and
  multitasking, and are what the exception and thread facilities of languages like
  C++ and Java rest on.

First-class continuations are distinct from
[[continuation-passing-style]], which is a compilation technique that makes
continuations explicit in the intermediate representation. A compiler can use CPS
internally without exposing continuations to the programmer, and can support
first-class continuations without using CPS —
[[lambda-the-ultimate-label-a-simple-optimizing-compiler-for-scheme|Twobit]] does
exactly that. Support for them is one of the properties that makes Chez Scheme a
good substrate for other languages, per
[[porting-racket-to-chez-scheme|Racket's]] account of moving onto it.

## Sources

- [[implementation-strategies-for-first-class-continuations|Implementation Strategies for First-Class Continuations]]
- [[representing-control-in-the-presence-of-first-class-continuations|Representing Control in the Presence of First-Class Continuations]]
