---
type: summary
status: provisional
title: A Tractable Native-Code Scheme System
created: 2026-08-05
source: https://www.deinprogramm.de/sperber/papers/tractable-native-code-scheme-system.pdf
raw: raw/2026-08-05-tractable-native-code-scheme-system.md
tags: [programming-languages, language-implementation, scheme, lisp, continuations]
---

# A Tractable Native-Code Scheme System

## Summary

Martin Gasbichler, [[richard-kelsey|Richard Kelsey]], and Michael Sperber describe
adding an optimizing native-code compiler to [[scheme-48]], a byte-code
implementation of [[scheme]]. The paper's subject is less the compiler than the
*method*: how to add native code to an existing system without destroying the
simplicity and modularity that made it worth extending. Previous attempts had
failed on exactly that, and the authors are candid that their own time was limited
and non-contiguous — a constraint that shaped the design rather than merely
excusing it.

Three decisions carry the result:

- **The native-code compiler is a mere translator.** It maps each byte-code
  instruction to a corresponding sequence of native code and performs *no analysis
  whatsoever*. A set of *compilators*, one per opcode, emits the code; a compilator
  may emit straight-line code, call static glue, or request an operation from the
  VM. Crucially it can **throw back to the VM** for exceptions and for instructions
  it does not yet handle, which is what let the translator be developed
  incrementally rather than all at once.
- **Optimization is a separate pass over byte code**, not part of the translator.
- **Existing components were reused** wherever possible.

The reuse claim is the paper's spine, and Scheme 48's architecture is what makes it
possible. Its VM is written in **Pre-Scheme**, a Scheme subset compiled to efficient
C by a compiler that ships with the system — and the Pre-Scheme compiler's front end
is just the ordinary Scheme front end. That front end and the *Transformational
Compiler* behind it are general infrastructure, not Pre-Scheme–specific, and their
distinguishing feature is a single [[continuation-passing-style|CPS]]-based
intermediate representation used at almost every stage.

So the byte-code optimizer needs no optimizer of its own. It translates byte code
*into* the Transformational Compiler's CPS representation, lets that compiler do the
work, and translates back to byte code — a third context for the same machinery. The
byte-code parser is likewise reused, driven by a declarative instruction-format
description and a set of per-opcode attribution functions.

The CPS intermediate language is the λ-calculus plus constants and *primops*, with
even procedure calls and returns expressed as explicit primops. Its λ forms are
annotated into three classes — `λcont`, `λjump`, and `λproc` — and that
classification is what the optimizations act on. Among them: constant folding, beta
reduction, matching procedures with their call sites, boolean short-circuiting, and
turning recursive loops into iterative ones. The worked example shows a `λproc`
specialized for its single continuation, demoted to a `λjump`, and its calls
rewritten from `unknown-tail-call` into direct `jump`s — the CPS-level move that
later shows up as the largest win in the benchmarks.

Section 4 recounts streamlining the VM's stack discipline. The original design used
linked environments allocated on the stack and copied to the heap on closure
creation, following the program's lexical structure — a choice that deliberately
avoided any live-variable analysis in the compiler.

**Benchmarks** (a subset of the Gabriel benchmarks, on a 3.0 GHz Pentium 4) put
native code at a **2–4× speedup** over byte code, with optimization adding **up to
2×** on top — the gain concentrated precisely where the optimizer converts tail
calls into jumps. The authors report the gains are small when recursive calls
dominate, because those still compile to an indirect `jmp` rather than a direct one.
Both benchmark figures are charts the PDF conversion did not carry over.

A final reuse result: Sperber and Thiemann's earlier run-time code generation
facility for Scheme 48 works by composing code-generation combinators, derived from
the byte-code compiler's own source, with a partial evaluator's back end. Composing
those generators with the new native-code compilators yields straight-through
run-time native-code generation — no intermediate source or byte code — at very
little additional cost.

The related-work section situates all of this against Java JIT compilers, observing
that most JVM code generators interpose one or more intermediate representations
between byte code and native code and are correspondingly more complex. It also
notes that Squeak Smalltalk's VM is built the same way Scheme 48's is: written in a
subset of its own language and translated to C.

## Why this matters

The inbox note saved this for the virtual-machine-to-native-code path, and the paper
delivers that — but its more transferable claim is about *how* to get there. The
translator is trivial and does no analysis; all the intelligence lives in a
pre-existing optimizer reached by translating byte code into a CPS IR and back. The
throw-back-to-the-VM escape hatch is what makes the whole thing incrementally
buildable, since an unhandled opcode is a fallback rather than a blocker.

That is a distinct answer to a question the corpus keeps circling. Ghuloum's
incrementality is 24 progressively larger source subsets, each a working compiler.
Here incrementality runs the other way: a complete slow system already exists, and
native code is added opcode by opcode with the VM catching everything not yet
translated. Both get a working system at every step; they differ in what is held
fixed.

It also sharpens the CPS thread running through
[[rabbit-a-compiler-for-scheme|RABBIT]],
[[orbit-an-optimizing-compiler-for-scheme|ORBIT]], and
[[compiling-with-continuations-and-llvm|LLVM-targeted CPS]]. Scheme 48
uses one CPS IR for Pre-Scheme compilation, for ordinary Scheme compilation, and for
byte-code optimization — three consumers of one representation. That is the
strongest corpus evidence yet for CPS as *reusable infrastructure* rather than one
compiler's internal choice, and it stands against
[[lambda-the-ultimate-label-a-simple-optimizing-compiler-for-scheme|Clinger's]]
preference for direct style, which rejects CPS on the grounds that it complicates
register allocation and targeting. Both are arguing from working compilers.

Finally it connects two clusters already here through a person: Richard Kelsey wrote
ORBIT's front end at Yale and is a co-author on Scheme 48, making
[[t-programming-language|T]] and Scheme 48 branches of one lineage rather than
unrelated systems.
