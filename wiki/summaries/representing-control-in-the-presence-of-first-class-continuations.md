---
type: summary
status: provisional
title: Representing Control in the Presence of First-Class Continuations
created: 2026-08-05
source: https://doi.org/10.1145/93548.93554
raw: raw/2026-08-05-93548-93554.md
tags: [programming-languages, language-implementation, scheme, lisp, chez-scheme, continuations]
---

# Representing Control in the Presence of First-Class Continuations

## Summary

[[robert-hieb|Robert Hieb]], [[r-kent-dybvig|R. Kent Dybvig]], and Carl Bruggeman's
PLDI 1990 paper introducing the **segmented stack** model for
[[first-class-continuations|first-class continuations]]. It is the design that
[[chez-scheme|Chez Scheme]] adopted, and the one the
[[implementation-strategies-for-first-class-continuations|Clinger–Hartheimer–Ost survey]]
names the *Hieb-Dybvig-Bruggeman* variation.

**The problem.** A continuation represents the rest of the computation, which is the
current chain of activation records, and in [[scheme]] it has indefinite extent — it may
be invoked after control has already left the point of capture, and invoked more than
once. So a pointer into a reusable stack is not enough. The paper lays out why each
obvious answer is unsatisfactory. Heap-allocating a linked list of frames makes capture
and reinstatement nearly free and turns stack overflow into ordinary heap overflow, but
taxes every call with frame-linkage writes, extra collector work, and worse locality —
and frames can never be reused or modified, so objects of dynamic extent cannot be
stack-allocated. Appel's argument that large memories make heap allocation competitive
is answered on locality grounds: it assumes memory can be used without penalty, which
caches and virtual memory do not grant. The naive **copy** strategy (traced to
McDermott) keeps a real stack and copies it to the heap on capture, but then a
continuation operation costs time proportional to stack depth, and repeated capture can
retain many copies of one large stack. Bartley and Jensen's bounded **stack cache**
fixes the worst case by capping the cache, but ties the bound on continuation cost to
the bound on recursion depth, which produces the *bouncing* pathology: a program that
recurses to the brink of overflow and then loops makes the worst-case call cost the
average case.

**The model.** The control stack becomes a **linked list of stack segments**, each
segment a true stack of frames. A *stack record* per segment holds a pointer to the
segment's base, a link to the next record, the segment's size, and the return address
of its topmost frame. Frames carry no dynamic link at all: the frame pointer is
adjusted by a constant immediately before a call and back after the return, and the
compiler emits the **frame size as a data word in the code stream just before the
return point**, so a stack walker can go from a return address to the size of the frame
below it. There is no stack pointer, only a frame pointer, which simplifies argument
access and removes push/pop increments — valuable on RISC machines with no
auto-increment addressing.

**Capture is constant-time and copies nothing.** The occupied portion of the current
segment is sealed: the current stack record becomes the continuation object (its size
field adjusted, the current return address stored in it), the return address in the
current frame is replaced by the address of an **underflow handler**, and a fresh stack
record is allocated whose base is the word above the sealed portion and whose size is
whatever remains. Each capture therefore *shortens* the current segment rather than
copying it, and eventually forces allocation of a new one. A capture with an empty
current segment changes nothing and reuses the link field as the continuation — which
is what keeps a tail-recursive loop that calls `call/cc` every iteration from growing
the control stack without bound (see [[tail-recursion]]).

**Reinstatement is bounded by a constant.** The continuation's segment is copied over
the current segment. If it exceeds a **copy bound**, it is first split — walking
backwards through the frames until one more would exceed the bound, then dividing the
segment in the same way capture divides it. Bounding the copy also requires bounding
frame size, so the *frame bound* fixes the worst-case cost while the copy bound fixes
the average case; extra arguments and locals spill to auxiliary structures when a frame
would be too large, which the authors report is rarely necessary. Returning from the
frame at a segment's base hits the underflow handler, which simply reinstates the
continuation in the link field.

**Overflow and underflow become continuation operations.** Overflow is treated as an
implicit capture and underflow as a reinstatement, so one mechanism serves both. The
authors wanted memory-protection faults to detect overflow for free, and report that
this failed in practice across the machines they targeted — either the fault could not
be generated reliably or the system state could not be recovered afterward — so they
use **explicit checks**, made cheap by keeping an end-of-stack pointer `esp` in a
register and comparing it against the frame pointer. The `esp` is set a constant
distance before the true end, with room for two frames, so that procedures making no
non-tail calls need no check at all; leaf routines and tight tail-recursive loops
therefore pay nothing, and static analysis removes further checks where the callee's
stack use is known and bounded.

**Comparison with the stack/heap hybrid.** The paper argues directly against
[[william-clinger|Clinger]], Hartheimer, and Ost, whose hybrid allocates frames on a
stack and moves them into a heap-allocated list on capture, never copying them back.
That guarantees only one copy of a frame ever exists, but returns must test whether
they are returning from stack or heap, dynamic-extent objects still cannot be
stack-allocated because they move on capture, and the stack must stay small to bound
capture cost — so overflows are frequent. The segmented model does duplicate frames,
but the segment-size bound bounds the duplication to a constant factor.

The mechanism was implemented in Chez Scheme, without the compiler enforcing the frame
bound: static analysis of Chez's own source showed 99% of frames under 30 words. The
authors credit Danvy for the observation that multiple continuation copies can cause
unbounded allocation, and point to their own work on concurrent continuations as the
next step.

## Why this matters

This is the primary source for a mechanism that pages here describe from the
outside. The
[[implementation-strategies-for-first-class-continuations|Clinger, Hartheimer, and Ost survey]]
catalogues the *Hieb-Dybvig-Bruggeman* variation as one
strategy among a dozen and scores it on the direct/indirect cost framing;
[[the-development-of-chez-scheme|The Development of Chez Scheme]] records the arrival of
constant-time continuation operations as a version-by-version milestone reached in
Versions 3 and 4. This paper is the argument itself, with the segment-splitting detail
that makes the constant bound real rather than asserted.

It also completes an exchange. The survey and this paper are opposing positions by
overlapping authors: Clinger, Hartheimer, and Ost argue for the stack/heap hybrid in
1988, and here Hieb, Dybvig, and Bruggeman answer in 1990 on the specific grounds of
frame reuse, dynamic-extent allocation, and overflow frequency — while conceding the
hybrid's one clean advantage, that a frame is never duplicated. Reading the two
together shows a design disagreement being settled by argument about cost models rather
than by benchmark, which is the same method [[william-clinger|Clinger]] brings to
compilers.

The engineering lesson worth carrying is the unification: once overflow is an implicit
capture and underflow an implicit reinstatement, one mechanism handles deep recursion,
multiple control threads, and `call/cc`, and the ordinary calling sequence stays
untaxed. That is what makes the strategy zero-overhead in the sense
[[first-class-continuations]] defines, and it explains why
[[chez-scheme|Chez Scheme]] can offer cheap continuations to clients built on top of
it. The reported failure to use memory-protection faults portably is worth keeping too:
it is a concrete account of a technique that is elegant on paper and unavailable in
practice.
