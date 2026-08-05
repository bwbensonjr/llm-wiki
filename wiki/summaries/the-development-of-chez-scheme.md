---
type: summary
status: reviewed
title: The Development of Chez Scheme
created: 2026-08-05
source: https://doi.org/10.1145/1159803.1159805
raw: raw/2026-08-05-1159803-1159805.md
tags: [programming-languages, language-implementation, scheme, lisp, chez-scheme, continuations]
---

# The Development of Chez Scheme

## Summary

[[r-kent-dybvig|R. Kent Dybvig]]'s ICFP 2006 retrospective on twenty years of
[[chez-scheme|Chez Scheme]], from Version 1 in 1985 to Version 7 in 2005. It is
organized version by version, each with a highlights table listing that release's
language features, implementation changes, documentation, and supported platforms —
which makes it as much a record of what mattered when as a technical paper.

**The founding insight** came from profiling C-Scheme and finding most time going to
variable lookups and stack-frame creation. Dybvig concluded the standard Scheme
implementation model was simply wrong: heap-allocating environments and call frames
makes closure creation cheap at the expense of everything else, when the common
operations are variable access and procedure call.

His replacement has three parts, and they interlock:

- **Continuations** — use a stack for calls; capture by copying the stack into the
  heap, reinstate by copying back.
- **Closures** — a flat representation, taken from *displays* as described in Randell
  and Russell's book on implementing Algol 60. Access cost becomes constant rather
  than proportional to nesting depth.
- **Boxing assigned variables** — a variable's value could otherwise appear in several
  closures at once, so each assigned variable is replaced by a pointer to a
  single-celled heap object. This also solved the stack problem, letting local values
  live directly in a frame that a continuation capture might copy.

The result: closure creation costs proportional to free-variable count, but variable
access costs one memory reference — two if the variable is ever assigned. The same
boxing move appears in [[lambda-the-ultimate-label-a-simple-optimizing-compiler-for-scheme|Twobit]]
as *assignment elimination*, there justified as making locals immutable so they can be
freely copied for [[lambda-lifting]].

**Version 1** (1985) was, in Dybvig's own words, naive at the high level: it handled a
small set of core forms and its only real optimization treated variables bound by a
direct `lambda` application as locals to avoid allocating and calling a closure. The
effort went into low-level representation and instruction selection instead, plus a
peephole optimizer — a deliberate ordering he defends on the grounds that low-level
details have more leverage because they affect *all* code. One representation hack:
a code-pointer slot alongside the value slot in every symbol, so calls to globally
bound procedures jump unconditionally without a check.

That decision is the paper's recurring method, stated plainly: pick the low-hanging
fruit, leave the rest, move to another tree. There is no point perfecting one area
while others lag.

**Later versions** trace a widening system. Version 2 (1987) brought multiple back
ends and operating systems, optimization levels, inlining of primitives, and
destination-driven code generation that obsoleted the peephole optimizer; the compiler
being written in Scheme meant its own optimizations made it faster, more than paying
for the extra work. Notably, Chez adopted expansion-passing-style and `extend-syntax`
macros here but **did not adopt [[hygienic-macros|hygienic]] expansion until much
later**. Version 3 (1989) replaced whole-stack copying with a segmented mechanism, so
continuation operations stopped being proportional to stack depth, and added a foreign
interface. Version 4 overhauled value representation and reached constant-time
continuation operations and stack-overflow recovery. Version 5 (1994) brought
`syntax-case` macros, multiple values, guardians and weak pairs, and improved register
allocation. Version 7 (2005) added multithreading via POSIX threads and the first
64-bit port, helped by the earlier decision to use BiBOP and segmented memory.

The account is also personal. Bob Hieb — a former carpenter who stood out in Dybvig's
compiler course and became a long-time collaborator — was killed in a car accident in
1992 along with his daughter Iva, and Dybvig writes that he dealt with his grief partly
through the work that became Version 5.

The compiler and much of the run-time system were written in Scheme and bootstrapped
from C-Scheme, with code originally written in C progressively moved to Scheme, where
it can be written more abstractly and is less exposed to changes elsewhere in the
system. Throughout, the stated objectives never change: reliability — correctly
implementing the whole language and never crashing from a compiler or runtime fault —
and uniformly good efficiency.

## Why this matters

The inbox note wanted an in-depth history of an important Scheme compiler, and this
supplies a *longitudinal* view. [[rabbit-a-compiler-for-scheme|RABBIT]],
[[orbit-an-optimizing-compiler-for-scheme|ORBIT]], Twobit, and
[[a-tractable-native-code-scheme-system|Scheme 48]] are each a snapshot that makes its
case for a design and stops.
This one shows twenty years of consequences, including which early decisions kept
paying (BiBOP and segmented memory made the 64-bit and thread ports tractable) and
which were deferred indefinitely.

It substantially deepens [[chez-scheme]], which until now rested on
[[porting-racket-to-chez-scheme|Racket's]] account of adopting it. That page describes
the properties Chez offers a client — proper tail calls, cheap first-class
continuations, the numeric tower, good machine code. This explains where each came
from, and that the continuation performance Racket relies on took until Version 4 to
become constant-time.

It also sits in interesting tension with the rest of the batch on the question of
where compiler effort belongs. Twobit argues for high-level simplicity and treats the
garbage collector as the real determinant; Dybvig spent Version 1 almost entirely on
low-level representation and instruction selection, explicitly deferring high-level
optimization, and got a system that outperformed its contemporaries. Both were right
about their own systems, which suggests the question is less settled than either
paper's confidence implies.

Finally it dates the hygiene adoption curve from the implementer's side: Chez took
`extend-syntax` in 1987 and waited until Version 5 in 1994 for `syntax-case`. Read
against [[hygienic-macro-technology|Clinger and Wand's history]], which tells the same
years from the designers' and standards side, the lag between a solution existing and
a production system shipping it becomes concrete.
