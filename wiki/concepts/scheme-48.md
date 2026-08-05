---
type: concept
status: provisional
title: Scheme 48
created: 2026-08-05
tags: [programming-languages, language-implementation, scheme, lisp]
---

# Scheme 48

A byte-code implementation of [[scheme]] built with tractability and reliability as
its primary design goals — a clear, modular, readable system intended as a platform
for programming-language implementation experiments, later extended with an
optimizing native-code compiler.

## Notes

Its defining structural choice is that **the VM is written in Scheme** — specifically
in *Pre-Scheme*, a subset compiled to efficient C by a compiler shipped with the
system. The VM can therefore run as an ordinary Scheme program, which is how its
developers debug it, and be compiled to C for production. Squeak Smalltalk's VM is
built on the same principle.

The Pre-Scheme compiler is where the system's reuse discipline shows: its front end
simply invokes the general Scheme front end, and behind that sits the
*Transformational Compiler*, whose distinguishing feature is a single
[[continuation-passing-style|CPS]]-based intermediate representation used at almost
every stage of compilation. That IR is the λ-calculus plus constants and *primops*,
with calls and returns expressed as primops and λ forms annotated as `λcont`,
`λjump`, or `λproc`.

Because that infrastructure is general rather than Pre-Scheme–specific, later
additions could be built largely by rearranging existing parts. The byte-code
optimizer translates byte code *into* the CPS IR, lets the Transformational Compiler
optimize, and translates back — no new optimizer. The native-code compiler is a
per-opcode translator doing no analysis at all, able to throw back to the VM for
anything it does not handle, which is what made it buildable incrementally. Native
code buys 2–4× over byte code, with optimization adding up to 2× more where it turns
tail calls into direct jumps.

It sits in this wiki's collection of Scheme implementations alongside
[[chez-scheme|Chez Scheme]], [[racket|Racket]], and [[larceny|Larceny]]. Through
[[richard-kelsey|Richard Kelsey]] it shares a lineage with
[[t-programming-language|T]] and [[orbit-an-optimizing-compiler-for-scheme|ORBIT]].

## Sources

- [[a-tractable-native-code-scheme-system|A Tractable Native-Code Scheme System]]
