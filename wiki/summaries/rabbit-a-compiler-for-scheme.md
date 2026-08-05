---
type: summary
status: provisional
title: "RABBIT: A Compiler for Scheme"
created: 2026-08-05
source: https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html
raw: raw/2026-08-05-compiler-optimization-guy-l-steele-jr.md
tags: [programming-languages, language-implementation, scheme, lisp, continuations]
---

# RABBIT: A Compiler for Scheme

## Summary

[[guy-steele|Guy Lewis Steele Jr.]]'s 1977 MIT dissertation, revised as *RABBIT:
A Compiler for SCHEME* (1978) and abridged into the chapter "Compiler
Optimization Based on Viewing LAMBDA as RENAME plus GOTO." This transcription is
one of the [[lambda-papers|Lambda Papers]], the series in which Steele and Gerald
Jay Sussman worked out the semantics and implementation of [[scheme]], a
lexically-scoped dialect of [[lisp]] embedded in MacLISP.

The compiler's organizing insight is in the title: a `LAMBDA`-expression is a
**rename** (it binds parameters, nothing more) and a procedure call is a
**GOTO** that happens to pass arguments. Under [[lambda-calculus|lambda-calculus]]
semantics with lexical scoping and [[tail-recursion]], a call need never push a
return address — it is argument *evaluation* that pushes control stack, not
invocation. The consequence is Steele's central polemic, developed further in
"Debunking the 'Expensive Procedure Call' Myth": function calls are not
inherently expensive, and languages whose programmers avoid procedures are
suffering from an implementation artifact rather than a law of nature.

RABBIT compiles a deliberately tiny basis set — `LAMBDA`, `IF`, `QUOTE`,
`LABELS`, `ASET'`, `CATCH`, and combinations. Everything else a programmer
expects (`AND`, `OR`, `COND`, `BLOCK`, sequencing, assignment, looping, `GOTO`)
is a **macro** expanding into that basis. Steele shows the standard technique for
writing capture-free macro rules: rather than inventing a fresh variable and
risking a name conflict (the "`GENSYM` problem"), wrap the continuation in a
thunk — `(OR x . rest)` expands to `((LAMBDA (V R) (IF V V (R))) x (LAMBDA ()
(OR . rest)))`. Because calls are cheap and the extra lambdas mostly optimize
away, this costs nothing in the generated code.

The paper's methodological claim is that macros and optimizations are *the same
kind of thing*: both are source-to-source rewrites on Scheme programs, expressible
in the same meta-language. Shrinking the basis set therefore shrinks the set of
optimizations needed, and their effects compose multiplicatively rather than
additively — a large body of traditional compiler optimizations falls out as
special cases of a few transformations. Steele works a full example: `(IF (AND
PRED1 PRED2) (PRINT 'WIN) (ERROR 'LOSE))` expands into nested lambdas, then
beta-substitution of singly-referenced variables, dead-code elimination on
constant predicates, `((LAMBDA () body)) => body` collapsing, and the
`IF`-distribution rule reduce it to code whose remaining `(Q2)` calls compile to
plain `GOTO`s branching to shared code — with no closures created at runtime.

Compilation proceeds by converting the source into
[[continuation-passing-style]], which RABBIT uses as an intermediate
representation that is *itself* a subset of Scheme. This is the origin of the
CPS-based compiler architecture: because the IR is a subset of the source
language, the same optimizer can run at both levels. CPS makes every intermediate
quantity manifest as a variable and fixes the order of evaluation, so an
apparently applicative representation admits an imperative reading — no control
stack is needed and no function ever returns, which makes transcription to
machine code straightforward.

After CPS conversion RABBIT performs environment and
[[closure-conversion|closure analysis]], classifying each `LAMBDA`-expression
into one of three cases: **fully closed** (the function escapes as data, so it
needs a standard closure), **partially closed** (called only by name, but from
within other closures, so its environment must be consed up without a code
pointer), or **not closed at all** (the environment is always recoverable at the
point of call). Because lexical scoping means the compiler sees every reference
to a variable, it is free to lay out run-time environments however it likes —
preferring registers to heap allocation — which Steele frames as the compiler
acting as a designer of data structures. A predecessor throw-away compiler,
CHEAPY, established the CPS approach; RABBIT, about fifty pages of Scheme written
part-time in roughly a month, is the optimizing version. Steele closes by
proposing Scheme as an ideal UNCOL (universal intermediate language) at two
levels — the applicative level and the CPS level — arguing that earlier UNCOL
designs failed by thinking imperatively about data manipulation instead of about
environment and control.

## Why this matters

A seminal compiler paper by one of Scheme's two inventors, and the point where
several ideas this wiki keeps circling back to were first assembled in one place.
[[continuation-passing-style]] as a compiler IR starts here, which is what
[[compiling-with-continuations-and-llvm|Farvardin and Reppy]] are still working
against four decades later when they fight [[llvm]] over guaranteed tail calls.
The "small basis set plus macros" strategy is the direct ancestor of the
language-oriented programming argued for in
[[a-programmable-programming-language|the Racket Manifesto]], and the treatment
of the compiler as a source-to-source transformer anticipates the nanopass style. It is also a useful
corrective: the claim that cheap function calls are an implementation choice
rather than a cost of abstraction is one the industry had to relearn repeatedly.
