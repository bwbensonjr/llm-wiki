---
type: summary
status: provisional
title: "Lambda, the Ultimate Label: A Simple Optimizing Compiler for Scheme"
created: 2026-08-05
source: https://3e8.org/pub/scheme/doc/lisp-pointers/v7i3/p128-clinger.pdf
raw: raw/2026-08-05-p128-clinger.md
tags: [programming-languages, language-implementation, scheme, lisp, continuations]
---

# Lambda, the Ultimate Label: A Simple Optimizing Compiler for Scheme

## Summary

William D Clinger and Lars Thomas Hansen's LFP '94 paper describing **Twobit**, the
[[scheme]] compiler behind [[larceny]]. Its thesis is that an optimizing compiler for
a higher-order language need not be complex: allocate every non-local and assigned
variable in the heap, then use [[lambda-lifting]] to eliminate almost all non-local
variables anyway, so that what remains are locals that live in registers. The
resulting slogan gives the paper its title — a lifted `lambda` expression is an
assembly-language label, and its formal parameter list is an invariant asserting
which registers are live there.

Twobit is explicitly positioned as heir to [[rabbit-a-compiler-for-scheme|RABBIT]],
[[orbit-an-optimizing-compiler-for-scheme|ORBIT]], and Gambit, but with different
goals: not advancing the state of the art in code quality, but simplicity,
portability, and fast compilation while staying competitive with
[[chez-scheme|Chez Scheme]], [[standard-ml|Standard ML of New Jersey]], and
commercial Common Lisp. The machine-independent compiler is under 5,000 lines.

The front end runs two passes. **Pass 1** expands macros, eliminates internal
definitions, checks syntax, and alpha-converts every local variable to a unique
name, building for each variable a table `R` of its references, assignments, and
calls. **Pass 2** carries almost all optimization, structured as a cascade:

- **Single assignment analysis** — a first-order closure analysis, which the paper
  notes had long been used in MacScheme but never described in print. It finds
  formal parameters assigned exactly once, at the head of the body, to a `lambda`,
  and called as often as referenced. Such a parameter is really a *known local
  procedure* whose call sites are all visible, so it needs no closure; the
  assignment is rewritten back into an internal definition. (This is a distinct
  technique from SSA form, despite the similar name.)
- **Assignment elimination** — remaining assigned locals are boxed into heap cells
  (`MAKE-CELL`/`CELL-REF`/`CELL-SET!`), which renders all locals immutable as in
  Standard ML and therefore freely copyable, a precondition for lifting.
- **Local source transformations** — eight on `if`, three on `let`, `begin`
  flattening, dead-constant removal; the paper says these are essentially RABBIT's.
- **Lambda lifting** — the hardest pass. Lifting one known local procedure past a
  parameter it references means adding that parameter to it and to every call, which
  can cascade: the paper works an example where lifting `f` forces `g` to escape and
  then strands `f` outside the scope of `y`. The fix is to lift each *group* of known
  local procedures as a unit, after a flow analysis over recursive equations solved
  by a general fixed-point routine. Twobit lifts unless the body already requires a
  closure.

The remaining passes are code generation for a register-based hypothetical
*MacScheme machine* (a planned representation-inference pass sits between them,
unimplemented), then a table-driven optimizing assembler emitting byte code or SPARC.
The most interesting code-generation optimization is **parallel assignment
optimization**: build a dependency graph over the argument registers and topologically
sort it to find an evaluation order that computes each operand directly into the
register that will pass it. Paired with lambda lifting's parameter ordering, the two
amount to a strategy for global register allocation — lifted parameters usually
already sit in their target registers at the call.

Two implementation discussions stand out. On **first-class continuations**, Larceny
uses the incremental stack/heap strategy — continuation frames in a stack cache with
a dummy frame at the bottom whose return address invokes an underflow handler — which
the authors say has zero overhead when `call/cc` is unused. This is precisely what
Twobit's original code generator broke by allocating separate spill frames not
corresponding to any procedure call, which the paper calls a major design error. On
**[[tail-recursion]]**, stack allocation of non-local variables makes proper tail calls
hard, since a tail call cannot deallocate a frame holding non-locals the callee needs;
lambda lifting dissolves the problem by eliminating non-local variables outright,
leaving only those already heap-allocated in a closure.

The benchmarks (Section 11) compare Larceny against Chez Scheme, Allegro CL, and
SML/NJ on a SPARCstation IPC, and the authors are careful to frame them as context
rather than a victory claim: they argue procedure call cost, allocation, and garbage
collection matter more than compiler optimization for this class of language, and
that most of the benchmarks test the collector rather than the compiler.

On related work, the paper is unusually precise about lineage. Steele's RABBIT
contributed alpha conversion and the local transformations, and
[[guy-steele|Steele]] is credited for the view that a call is a `goto` passing
arguments — from which "a lambda expression is a label" follows directly, the
[[lambda-papers|lambda-the-ultimate]] move the title invokes. Lambda lifting as a
practical technique came from Augustsson's Lazy ML. Assignment elimination came from
ORBIT, which the authors also credit as probably the first Scheme compiler to treat
argument evaluation as a parallel assignment to registers. And lambda lifting is
identified with SML/NJ's [[closure-conversion|closure conversion]], with the
difference that Twobit's flow equation is *local* — involving only variables whose
scope is being left — so lifting can stop short of the outermost `lambda`, sharing
more environment structure than SML/NJ's global, all-or-nothing approach. The paper
attributes Larceny's better code on the `sieve-4` benchmark to exactly that
difference. Notably, Clinger prefers direct style over
[[continuation-passing-style|CPS]]: premature CPS conversion, he argues, makes
register allocation, targeting, and parallel assignment harder, and Twobit gets some
of CPS's benefits without the conversion.

## Why this matters

The inbox note saved this for its treatment of code transformation and lambda
lifting, and the paper is probably the clearest single account of lambda lifting as
a *compiler engineering* decision rather than a functional-programming curiosity —
including the failure mode (cascading extra parameters, escaping procedures) that
makes the naive version wrong, and the group-lifting flow analysis that fixes it.

Placed against what the wiki already holds, it completes an arc. RABBIT established
that a call is a `goto` and left closure strategy open; ORBIT supplied the analyses
and showed a higher-order language can match Pascal; Ghuloum showed the pipeline at
its smallest. Twobit is the entry that argues the *simplicity* case directly — that
you can get most of the way with a heap-everything default plus one strong
transformation, and that the residual performance question belongs to the garbage
collector rather than the compiler. That last claim is the sharpest thing here, and
it cuts against the implicit premise of the rest of the compiler-lineage batch.

It also supplies the corpus's most explicit statement of the relationship between
[[lambda-lifting]] and [[closure-conversion]] — the same transformation under two
names, differing in how global the flow equation is — which is the kind of
terminological knot the hub pages exist to untie.
