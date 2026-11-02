---
type: summary
title: Improving the Clasp Programming Experience
created: 2026-10-31
source: https://drmeister.wordpress.com/2016/01/29/improving-the-clasp-programming-experience/
raw: raw/2026-10-31-improving-the-clasp-programming-experience.md
tags: [language-implementation, lisp, programming-languages]
---

# Improving the Clasp Programming Experience

## Summary

A short 2016 post on [[christian-schafmeister|Christian Schafmeister]]'s blog announcing a scraper that automates how [[clasp|Clasp]] exposes its C++ internals to Common Lisp. Before it, functions, classes, methods, symbols, enums and initializers were made visible to Lisp by thousands of hand-written registration calls run at startup. Now the C++ source is annotated with preprocessor tags (`CL_DEFUN`, `CL_DEFMETHOD`, `LISP_CLASS`, plus optional `CL_LAMBDA` for a Lisp lambda list, including `&optional` defaults, and `CL_DOCSTRING`). The build runs the C preprocessor with those tags defined, scrapes the output, and generates the startup code. A function named `ext__add_two_numbers` binds to the Lisp symbol `ext:add-two-numbers` with no other declaration. Generated code is rebuilt only when it needs to be.

He cites two benefits. Adding a new entity no longer means finding the right place to register it at startup. And the scraper records a source location for every entity, so in SLIME, `M-.` on a Clasp symbol jumps to its definition, in C++ or in Lisp. C++ functions and methods now also carry lambda lists and docstrings into the Lisp environment. The scraper is itself written in standard Common Lisp, so SBCL becomes a build dependency, and the earlier [[python|Python]] scrapers are retired, removing Python as a dependency.

## Why this matters

This matters because of the use of LLVM for a Lispy language.
