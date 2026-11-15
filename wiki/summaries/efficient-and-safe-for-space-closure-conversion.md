---
type: summary
title: Efficient and Safe-for-Space Closure Conversion
created: 2026-11-15
source: https://dl.acm.org/doi/epdf/10.1145/345099.345125
raw: raw/2026-11-15-efficient-and-safe-for-space-closure-conversion.md
tags: [programming-languages, language-implementation, continuations, standard-ml]
---

# Efficient and Safe-for-Space Closure Conversion

## Summary

[[zhong-shao|Zhong Shao]] and [[andrew-appel|Andrew W. Appel]]'s TOPLAS paper (vol. 22,
no. 1, January 2000; preliminary version at LFP 1994) presents the
[[closure-conversion|closure-conversion]] algorithm of
[[standard-ml|Standard ML of New Jersey]]: one that shares closures aggressively and keeps
as much environment as possible in registers, while still obeying the
[[safe-for-space|"safe for space complexity" (SSC)]] rule — *any local variable binding
must be unreachable after its last use within its scope.*

**The space argument.** The paper opens with a small SML program in which flat closures
use O(N) space and traditional **linked** closures use O(N²), because each closure for an
inner function keeps a pointer to its parent's closure and so retains a large list that is
no longer needed. The authors report finding real programs whose live data was 2 to 80
times larger than necessary under early SML/NJ versions that introduced such leaks. They
argue SSC is not an optimization but a requirement for any garbage-collected functional
language: a function like a compiler driver, `phase1` through `phaseN` binding each
intermediate representation in turn, keeps every intermediate form live if the compiler
treats it like a C subroutine with one stack frame, where a C programmer would have freed
each phase's data by hand. Stack frames and linked closures both violate SSC; flat closures
satisfy it but copy the same variables from closure to closure.

**Safely linked closures** are the representation that resolves the trade-off. Each
closure holds exactly its own free variables, as a flat closure does, but variables that
share a *lifetime* are grouped into a separate record that several closures can point to.
Nothing dead is retained, and nesting never exceeds two levels (the closure itself and one
shared record), so a free-variable access costs at most one extra indirection.

**No runtime stack.** All activation records are treated as closures of continuation
functions in [[continuation-passing-style]] and live either in the heap or in
**callee-save registers**. The authors argue that maintaining SSC on a conventional stack
is very hard once tail calls, generational stack collection, efficient `call/cc`, and
exceptions are all supported, whereas without a stack each of these becomes
straightforward and SSC holds as long as each closure contains only variables live in its
target and collection happens only at function entry.

**The algorithm** runs as four passes over a closed CPS program, ending in closure-passing
style:

1. build an **extended CPS call graph** (an edge also from a caller to the continuation it
   passes), run interval analysis to find loop nesting, and assign each path a *loop level*
   used as a static branch prediction;
2. compute each function's **raw free variables** with lifetimes, measured in *stage
   numbers* (the order of function-return points), recording each variable's first and
   last use, biased toward loop edges;
3. run **closure-strategy analysis**, deciding how many register slots each closure gets:
   one for an escaping user function (its environment goes to the heap), the k callee-save
   registers for an escaping continuation, and for a known function an iterative
   refinement that caps its slots by those of the callers that also have it free, so its
   environment is not forced into registers that will only be spilled;
4. choose the **closure layout** (which variables go in registers, which are grouped into
   shared heap records) and translate.

The authors stress that only the last property matters for SSC (each closure holding only
its own free variables); everything else is heuristics for more sharing and better
register use.

**Case studies.** A function making several sequential calls builds one shared closure
for all its continuations instead of one per call. Allocating a known function's
environment in registers, which is what [[lambda-lifting]] amounts to, can raise register
pressure in its callers and cause repeated save and reload traffic; the slot analysis
limits it, and in the paper's example puts that closure in the heap instead. For general
recursion such as `map`, the recursive continuation gets a special convention with fewer
callee-save registers, reached through a small coercion continuation.

**Measurements** on ten SML benchmarks, comparing the new algorithm against SML/NJ 1.03z's
previous one with the same three callee-save registers: heap allocation down 32% (closure
allocation down 40%), memory fetches for local and global variables down 46%, execution
14% faster, and code 19% smaller on average, with individual benchmarks up to 27% faster.
Compilation got about 6% faster as well, which the authors attribute to replacing ad hoc
heuristics with a systematic algorithm. Varying the number of callee-save registers barely
changed speed but did change allocation, and three floating-point callee-save registers
did not help, because captured continuations and exception handlers must be packed into a
single heap word. Garbage-collection time fell on eight benchmarks and nearly doubled on
one.

**Related work** places it against Steele's [[rabbit-a-compiler-for-scheme|RABBIT]], Rozas's
Liar, [[david-kranz|Kranz's]] [[orbit-an-optimizing-compiler-for-scheme|ORBIT]] with its
six closure strategies, and Appel and Jim's sharing strategies, all of which the authors
say violate SSC through unsafe closure sharing, and cites
[[lightweight-closure-conversion|Wand and Steckler's lightweight closures]] and Clinger's
1998 formal definition of SSC. The algorithm shipped in SML/NJ and in Yale's FLINT/ML
compiler.

## Why this matters

This is the algorithm behind the safe-for-space rule: the paper both argues why the rule
is a requirement rather than a nicety and shows a closure representation that keeps it
without giving up sharing. That makes it the engineering counterpart to
[[closure-conversion-is-safe-for-space|Paraskevopoulou and Appel]], who later prove
space safety formally for flat closure conversion and cite this work as the more efficient
safe-for-space design nobody had yet verified.

It is also the alternative to flat closures that
[[optimizing-closures-in-o-0-time|Keep, Hearn, and Dybvig]] weigh and decline. Reading the
two together makes the trade-off concrete. Shao and Appel share environment records among
closures with the same variable lifetimes and lean on callee-save registers and a
stackless runtime; Chez keeps flat closures on a stack and optimizes within them, partly
because much of Shao and Appel's reported saving came from global variables that Chez does
not put in closures at all. Both satisfy the same space rule, so the disagreement is about
which costs dominate, not about correctness.

For the wider closure thread, the paper is a bridge. It explicitly integrates the
techniques of [[rabbit-a-compiler-for-scheme|RABBIT]] and
[[orbit-an-optimizing-compiler-for-scheme|ORBIT]] into one analysis driven by lifetimes and
loop structure instead of per-construct strategies, and it extends
[[continuation-passing-closure-passing-style|Appel and Jim's]] closure-passing back end
with the callee-save registers that make a stackless CPS compiler competitive. Its
treatment of known functions also gives a precise reason why lifting a function's free
variables into registers can lose, the same caution Chez's paper reaches by measurement.
