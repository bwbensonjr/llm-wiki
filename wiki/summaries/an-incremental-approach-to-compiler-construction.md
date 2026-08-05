---
type: summary
status: provisional
title: An Incremental Approach to Compiler Construction
created: 2026-08-05
source: http://scheme2006.cs.uchicago.edu/11-ghuloum.pdf
raw: raw/2026-08-05-11-ghuloum.md
tags: [programming-languages, language-implementation, scheme, lisp, education]
---

# An Incremental Approach to Compiler Construction

## Summary

[[abdulaziz-ghuloum|Abdulaziz Ghuloum]]'s paper from the 2006 Scheme and
Functional Programming Workshop, arguing that "building a compiler can be as easy
as building an interpreter." Its target is a pedagogical failure: compiler books
are polarized between educational toys and industrial-strength optimizers, with
nothing in between, so the novice — facing what Ghuloum calls "wizard-talk" —
concludes they had better write an interpreter instead.

The remedy is a compiler for a large subset of [[scheme]] emitting real Intel x86
assembly, developed in **24 small steps**, each of which "can be implemented and
tested in one sitting" and each of which yields a *fully working compiler* for a
progressively larger subset of the language. The contrast Ghuloum draws is with
the conventional pass-structured curriculum, where only the final pass produces
anything that runs; here there is a working artifact from day one, which both
minimizes the risk of never finishing and suits self-directed learners and a
fixed academic semester.

The methodology is explicitly test-first: choose a small language subset, write
test cases covering it, write a compiler that emits assembly for it, make the
tests pass, refactor, then enlarge the subset and repeat. The compiler is a
single Scheme procedure `compile-program` taking an s-expression, with an `emit`
form routing output to an assembly file; a test driver compiles each case, links
it with a small C runtime, runs the executable, and diffs against expected
output. Scheme is chosen as *both* source and implementation language — its
uniform syntax defers scanners and parsers to the very end, and representing
programs as ordinary data means the reading problem is solved for free.

The steps build in a deliberate order. **Integers** starts by cheating
productively: compile `int scheme_entry(){ return 42; }` with gcc `-S`, read the
seven lines of assembly it produces, and emit the same thing from Scheme —
`(emit "movl $~a, %eax" x)` plus `ret`. **Immediate constants** introduces
tag-and-mask encoding so booleans, characters, and the empty list are disjoint
types in a machine word (fixnums take the low two bits as `00`, leaving 30 bits
of value; characters an 8-bit tag; booleans a 7-bit tag). Then unary and binary
primitives, local variables, conditionals, heap allocation, and procedure calls.

**Closures** (step 9) is where the compiler stops being a toy: a `closure` form
stores a code label in the first cell and free-variable values in the rest,
`%edi` serves as the closure pointer, and source `lambda` forms are lowered in
two moves — free-variable analysis annotating each `lambda` with the variables it
references but does not bind, then conversion into `labels`/`code`/`closure`
forms with the code lifted to the top. This is [[closure-conversion]] presented
as something a learner can implement in an afternoon. **Proper tail calls** (step
10) follows: rather than a call plus return, evaluate the arguments, put the
operator in `%edi`, copy the arguments down over the current frame, and issue an
indirect `jmp` — the frame-collapsing technique that gives
[[tail-recursion|unbounded tail calls in constant space]].

The remaining steps carry the language to most of R5RS: complex constants,
assignment, syntax extension, symbols and separate compilation, foreign calls,
error checking and safe primitives, variable-arity procedures, `apply`, output
and input ports, a tokenizer, a recursive-descent reader, and finally an
interpreter — the stated end goal, chosen because compiling an interactive
evaluator forces most of the interesting problems into the open. Ghuloum notes
that once `write` exists in Scheme, the C runtime's writer becomes redundant and
can be deleted.

A closing section maps the road onward without taking it: a full numeric tower,
multiple values, `syntax-case` macros and a module system, heap and stack
overflow checks (the latter enabling efficient continuation capture), or
alternatively a [[continuation-passing-style]] transformation before closure
conversion, which would simplify `call/cc` at the cost of more runtime closures.
On performance he is candid that the compiler performs essentially no
optimization — the `letrec` treatment is "extremely inefficient," every complex
operand gets a temporary stack slot, and no safe primitives are open-coded — and
points at better `letrec` handling, greedy shuffling for tail calls, copy
propagation, and eventually register allocation and inlining. The compiler's data
representation, however, is deliberately compact from the start, which keeps
error checks cheap.

## Why this matters

Filed for the incremental-transformation angle, though it is worth being precise
about which kind of incrementality this is. Ghuloum's compiler grows by
*progressively larger subsets of the source language* — 24 working compilers, one
after another — rather than by decomposing a single compiler into many tiny
passes. The nanopass framework proper (Sarkar, Waddell, and Dybvig) is the
latter, and this paper never mentions it; the two come from the same Indiana
lineage — Ghuloum thanks R. Kent Dybvig and leans on Waddell/Sarkar/Dybvig's
"Fixing letrec" — and both react against the monolithic-pass tradition, but they
are different ideas and worth keeping distinct in the wiki.

What the paper is unambiguously good for is the on-ramp. It is the practical
counterweight to [[rabbit-a-compiler-for-scheme|RABBIT]] and
[[orbit-an-optimizing-compiler-for-scheme|ORBIT]]: those establish what a serious
Scheme compiler must do, while this shows the smallest path to standing one up at
all, with [[closure-conversion]] and proper tail calls arriving as steps 9 and 10
rather than as chapters of theory. Read together they bracket the subject from
both ends.
