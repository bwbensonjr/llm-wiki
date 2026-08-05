---
type: summary
status: reviewed
title: Continuation-Passing, Closure-Passing Style
created: 2026-08-05
source: https://www.cs.princeton.edu/~appel/papers/cpcps.pdf
raw: raw/2026-08-05-cpcps.md
tags: [programming-languages, language-implementation, standard-ml, continuations]
---

# Continuation-Passing, Closure-Passing Style

## Summary

[[andrew-appel|Andrew W. Appel]] and Trevor Jim's POPL 1989 paper (read here as Princeton
tech report CS-TR-183-88) describing the
[[continuation-passing-style|CPS]] code generator for
[[standard-ml|Standard ML of New Jersey]]. Its predecessor was an abstract stack machine
whose main inefficiency, on inspection, was that every value went on and off the stack too
many times; rather than retrofit a register allocator, they rebuilt the back end around
CPS, citing [[david-kranz|Kranz's]]
[[orbit-an-optimizing-compiler-for-scheme|ORBIT]] for the insight that CPS is a natural
setting for register allocation and representation decisions.

**Decomposition is the paper's organizing claim.** The compiler runs ten phases, of which
this paper covers four through nine: CPS conversion, CPS optimization, closure conversion,
scope flattening, register spilling, and instruction generation. The comparison is drawn
explicitly and pointedly — ORBIT does "an impressive set of analyses in its back end, but
they're all tangled together into a single phase," so "where the ORBIT compiler has one
black box covering phases 6 through 9, we have four smaller black boxes," with
semantically well-defined interfaces that make an individual analysis easy to isolate. The
CPS language is an ML datatype in which all functions are named and most ill-formed
expressions are unrepresentable.

**Closure conversion, and the known/escaping split.** A closure is a record holding a
function's free variables plus a code pointer at a fixed offset, so callers need not know
the record's format or size. Several functions can share one record holding the union of
their free variables. A record is *necessary* only for a function that **escapes** — some
call site is unknown because it is passed as an argument, stored, or returned. For a
**known** function, whose every call site is visible, the free variables are instead
**added as extra arguments**, with each call arranging to pass them; the paper says this
is aimed at efficient loops, and credits the Categorical Abstract Machine for the
technique. A function that both escapes and is called from known sites can be split in
two, the escaping one defined in terms of the known one. The rewrite itself inserts a
`RECORD` at each `FIX` binding an escaping function, adds a closure argument to every
function, and rewrites free-variable references as `SELECT`s from it — the explicit
representation they name **closure-passing style**.

On closure *shape*, the paper lays out the trade-off rather than settling it: a **flat**
closure holds all free variables; **linked** closures reach existing records by pointer to
avoid recopying; combinations trade closure-creation time against access cost and size.
One consequence is noted as subtle — linked closures can occupy *more* space than flat
ones, because they retain closures the collector could otherwise reclaim.

**Spilling as a source-to-source rewrite.** After flattening all definitions into one set
of mutually recursive functions, a spilling phase rewrites the CPS so that no
subexpression has more than *n* free variables, *n* being tied to the machine's register
count: excess variables are packed into a `RECORD` and re-`SELECT`ed at their uses. The
authors keep this separate from closure conversion despite the overlap, on the grounds
that spilling is rare — profiling put spill records at one or two percent of heap
allocation on their Vax, where *n* was 8.

**No stack at all.** "Since modern garbage collectors are so cheap we have dispensed with
the stack." Call frames and continuation records are heap-allocated, which removes the
analysis deciding what may be stack-allocated, simplifies the runtime, makes
`call/cc`-style operators cheaper, lets a generational collector traverse only the newest
frames, and avoids preallocating a large stack per thread. They confront the obvious
objection with numbers: stack-allocating every closure record would save an estimated
**6–10%**, while the stackless strategy typically uses about **20% less memory**, because
objects tend to be retained on a stack past their last use.

Instruction generation is left with a very simple form — procedures never return, no
non-constant free variables remain, scopes are not nested, and live variables never
outnumber registers — so its decisions are mostly register allocation, guided by
**targeting** (put a value where a later call wants it), **anti-targeting** (avoid a
register another call needs), and two-address preferences. Following ORBIT, known
functions get special treatment: their code is not generated until a call site has been,
so formals can be assigned the registers the actuals already occupy and control can fall
through without a jump, making at least one call to each known function nearly free.

**Results.** Up to four times faster than the stack-based generator on small benchmarks
and comparable to Pascal and ORBIT, but only 25% better on the large "real world"
benchmark — the generator excels at tight tail-recursive loops, while big programs make
more calls that require saving state.

## Why this matters

This is the account of closure-passing style from the compiler that
[[lambda-the-ultimate-label-a-simple-optimizing-compiler-for-scheme|Twobit]] argues
against, and having it first-hand sharpens a distinction the hub pages draw at second
hand. Clinger and Hansen's point is that Twobit's flow equation involves only the
variables whose scope is actually being left, where SML/NJ's is global — and this paper
shows what that means concretely: SML/NJ *does* separate known from escaping functions,
and for known functions it adds free variables as extra parameters, which is
[[lambda-lifting|lambda lifting]] by another name. So the two compilers differ over how
far to lift and what justifies it, not over whether the transformation is worth doing.
[[closure-conversion]] and [[lambda-lifting]] can now cite the same mechanism from both
sides.

It also reframes a piece of the corpus's chronology. The argument for splitting a
compiler into many small phases with well-defined interfaces — made here in 1988 against
ORBIT's single tangled back end — is recognizably the [[nanopass]] argument, which
[[a-nanopass-framework-for-commercial-compiler-development|Keep and Dybvig]] press
twenty-five years later with a commercial compiler and published costs. Reading the two
together shows a design principle being restated with progressively better evidence
rather than being invented once.

The stackless decision is the sharpest disagreement it introduces. Appel dispenses with
the stack because collectors are cheap, and quantifies the concession at 6–10%; the
continuation-implementation literature here answers directly.
[[implementation-strategies-for-first-class-continuations|Clinger, Hartheimer, and Ost]]
catalogue the heap strategy's indirect costs, and
[[representing-control-in-the-presence-of-first-class-continuations|Hieb, Dybvig, and Bruggeman]]
take up Appel's large-memory argument by name and answer it on locality
grounds — caches and virtual memory penalize programs that use memory without locality.
That is a genuine argument between working compilers about a cost model, with both sides
now readable from their own papers.

Finally, the remark that linked closures can retain garbage flat ones would release is the
seed of the [[safe-for-space|safe-for-space]] work that follows it, and it explains why
[[chez-scheme|Chez Scheme]]'s choice of flat closures
([[the-development-of-chez-scheme|per Dybvig]]) is a space decision as much as an access-cost
one.
