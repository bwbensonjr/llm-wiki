---
type: summary
status: provisional
title: "CLHS 3.2.2.3: Semantic Constraints"
created: 2026-10-31
source: https://lispworks.com/documentation/HyperSpec/Body/03_bbc.htm
raw: raw/2026-10-31-clhs-section-3-2-2-3.md
tags: [lisp, language-implementation, programming-languages]
---

# CLHS 3.2.2.3: Semantic Constraints

## Summary

The section of the Common Lisp HyperSpec (the ANSI standard as published by LispWorks) that lists what a conforming program must keep consistent between compile time and run time, "designed to minimize the observable differences between compiled and interpreted programs". It is the standard's statement of what a file compiler may assume, and so of how far compilation can go before a later redefinition invalidates it.

The constraints: referenced macros must be defined in the compilation environment, and a form not naming a macro or special operator is compiled as a function call; `special` proclamations must be visible at compile time; a function declared `inline` must have the same definition at run time; inside a function `F`, an apparent recursive call to `F` may be assumed to be the same definition unless `F` is declared `notinline`; **a call within a file to a function defined in the same file refers to that function, unless declared `notinline`, and the consequences are unspecified if functions are redefined individually at run time or defined more than once in the same file**; `ftype`-declared argument syntax and return-value counts must hold at run time; constant variables must have similar values; `deftype` and `defstruct` types, and `defclass` classes, must keep their definitions, so subtype relationships cannot change; and type declarations must be accurate, on pain of undefined behavior.

Everything not listed is left open. Except in those situations, "a function defined in the evaluation environment is permitted to have a different definition or a different signature at run time, and the run-time definition prevails". Where compile-time and run-time definitions differ, an implementation may signal an error, use the compile-time definition, or use the run-time one. Calling an operator undefined at compile time is not a compile-time error.

## Why this matters

This is the baseline the [[lisp|Common Lisp]] standard sets for [[separate-compilation]]. The file is the unit within which a compiler may resolve calls directly and inline, and across files the default is that the run-time definition wins, so cross-file calls must stay late-bound unless the programmer adds `inline` or `ftype` declarations. That draws the boundary between what a separately compiled Common Lisp library can optimize on its own and what needs whole-program knowledge or an image dump to settle, which is the line any Lisp aiming at standalone executables has to decide where to draw.
