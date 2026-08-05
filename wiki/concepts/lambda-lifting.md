---
type: concept
status: provisional
title: Lambda Lifting
created: 2026-08-05
tags: [programming-languages, language-implementation]
---

# Lambda Lifting

The transformation that eliminates a nested function's non-local variables by
turning them into extra formal parameters, so the function can be hoisted to the
top level — becoming, in a register-based compiler, an assembly-language label whose
parameter list names the live registers.

## Notes

The technique entered practical compilation through Augustsson's compiler for Lazy
ML, by analogy with combinator abstraction. Its payoff in a Scheme compiler is
register allocation: a variable that was non-local had to live in the heap or in a
stack frame, but a variable that has become a formal parameter can live in a
register.

**The hard case is groups.** Lifting a single known local procedure past a parameter
it references means adding that parameter to the procedure and to every one of its
call sites — and that can cascade. Clinger and Hansen
([[lambda-the-ultimate-label-a-simple-optimizing-compiler-for-scheme|Twobit]])
work an example in which lifting `f` forces it to take `g` and `x` as extra
parameters, which makes `g` escape and negates the closure analysis that justified
the lift, and then lifting `g` in turn would strand `f` outside the scope of `y`. The
fix is to lift each *group* of mutually-referring known local procedures as a unit,
after a flow analysis over recursive equations that determines exactly which
parameters each member needs.

Lifting is not unconditionally desirable. Each added parameter is a register that
must be saved across a non-tail-recursive call, so Twobit lifts only until the body
of a `lambda` already requires a closure — a local, incremental policy.

**Relationship to [[closure-conversion]].** They are largely the same transformation
under two names: Clinger and Hansen note that what Twobit calls lambda lifting is
what SML/NJ's compiler calls closure conversion. The substantive difference is the
scope of the flow equation. SML/NJ's is global and all-or-nothing; Twobit's involves
only the variables whose scope is actually being left, so lifting can stop short of
the outermost `lambda` and share more environment structure. The paper credits that
locality for Larceny generating better code than SML/NJ on one benchmark. A further
terminological hazard: Wand and Steckler use "closure conversion" for a source-level
transformation replacing a procedure with a representation of it, which is orthogonal
to lifting.

Lambda lifting also interacts with [[tail-recursion]]. Stack-allocating non-local
variables obstructs proper tail calls, because a tail call cannot deallocate a frame
holding non-locals its callee still needs. Lifting dissolves that obstruction by
removing non-local variables entirely, leaving only those that were going to be
heap-allocated in a closure regardless.

## Sources

- [[lambda-the-ultimate-label-a-simple-optimizing-compiler-for-scheme|Lambda, the Ultimate Label: A Simple Optimizing Compiler for Scheme]]
