---
type: concept
status: reviewed
title: Lambda Papers
created: 2026-08-05
tags: [programming-languages, language-implementation, scheme, lisp]
---

# Lambda Papers

The series of MIT AI Lab memos written by [[guy-steele|Guy L. Steele Jr.]] and
Gerald Jay Sussman between 1975 and 1980, in which [[scheme]] was invented and
its implementation techniques worked out.

## Notes

The series includes "SCHEME: An Interpreter for Extended Lambda Calculus" (1975),
"LAMBDA: The Ultimate Imperative" (1976), "LAMBDA: The Ultimate Declarative"
(1976), "Debunking the 'Expensive Procedure Call' Myth" (1977), and Steele's
RABBIT dissertation (1977/78).

Their cumulative argument is that a language modelled directly on
[[lambda-calculus]] — lexically scoped, [[tail-recursion|tail-recursive]], with
first-class anonymous functions — needs only a tiny set of primitive constructs,
because the traditional imperative constructs can be defined as macros over that
basis and compiled into code as good as a conventional compiler's. Several ideas
that later became standard equipment originate here, notably
[[continuation-passing-style]] as a compiler IR.

## Sources

- [[rabbit-a-compiler-for-scheme|RABBIT: A Compiler for Scheme]]
- [[lambda-the-ultimate-label-a-simple-optimizing-compiler-for-scheme|Lambda, the Ultimate Label: A Simple Optimizing Compiler for Scheme]]
