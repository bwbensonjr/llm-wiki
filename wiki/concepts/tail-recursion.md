---
type: concept
status: reviewed
title: Tail Recursion
created: 2026-08-05
tags: [programming-languages, language-implementation, continuations]
---

# Tail Recursion

The property that a call in tail position consumes no additional control stack,
so a loop written in apparently recursive form executes iteratively. Guaranteed
tail calls are a defining requirement of [[scheme]].

## Notes

The intuition Steele draws out is that function calls do not push control stack —
*argument evaluation* does. A call therefore need not save a return address, and
can be compiled as a `GOTO` that passes arguments.

Tail recursion is not independent of lexical scoping. In dynamically scoped Lisps
a call must push stack in order to undo dynamic bindings on return, so tail
recursion is impossible; a lexically scoped language that fails to tail-call
merely wastes space.

The property becomes a hard constraint downstream: because
[[continuation-passing-style]] expresses loops and returns as tail calls,
guaranteed tail-call optimization is what makes CPS backends viable, and its
absence is precisely what compilers targeting [[llvm]] have to work around.

After CPS conversion a tail call is syntactically evident — it is a call whose
continuation is a variable rather than a lambda expression. Proper tail recursion
also constrains storage: a stack-allocated closure must be reclaimed as soon as it
is inaccessible, or a tail-recursive loop would grow the stack.

The simplest implementation, spelled out in
[[an-incremental-approach-to-compiler-construction|Ghuloum's tutorial]], is frame
collapsing: evaluate the arguments, copy them down over the current frame, and issue
an indirect `jmp` instead of a `call`.

Storage strategy can obstruct it in a subtler way. If non-local variables are
stack-allocated, a tail call cannot deallocate its frame when that frame holds
non-locals the callee still needs — so a return may have to deallocate frames
belonging to neither the returning procedure nor its caller.
[[lambda-the-ultimate-label-a-simple-optimizing-compiler-for-scheme|Twobit]]
sidesteps this rather than solving it: [[lambda-lifting]] removes non-local
variables outright, leaving only those already destined for the heap as part of a
closure.

## Sources

- [[rabbit-a-compiler-for-scheme|RABBIT: A Compiler for Scheme]]
- [[orbit-an-optimizing-compiler-for-scheme|ORBIT: An Optimizing Compiler for Scheme]]
- [[an-incremental-approach-to-compiler-construction|An Incremental Approach to Compiler Construction]]
- [[lambda-the-ultimate-label-a-simple-optimizing-compiler-for-scheme|Lambda, the Ultimate Label: A Simple Optimizing Compiler for Scheme]]
- [[a-tractable-native-code-scheme-system|A Tractable Native-Code Scheme System]]
- [[the-development-of-chez-scheme|The Development of Chez Scheme]]
