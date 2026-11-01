---
type: summary
status: provisional
title: Standalone Rhombus Programs
created: 2026-11-01
source: https://docs.racket-lang.org/rhombus-guide/standalone.html
raw: raw/2026-11-01-10-5-standalone-rhombus-programs.md
tags: [racket, language-implementation, programming-languages]
---

# Standalone Rhombus Programs

## Summary

Section 10.5 of the Rhombus Guide, on building standalone executables from programs in Rhombus, the newer language built on [[racket|Racket]]. Racket's tools generally work on Rhombus programs, and the workflow has three steps. `raco exe prog.rhm` produces an executable. It runs only on the machine that built it, because it still relies on an installed Racket and Rhombus. `raco dist prog_dist prog` then assembles every needed file into a directory that can be installed on another machine.

By default the executable and its distribution package "all of the support needed to run a program the same as when running rhombus or racket directly". The guide names the condition for doing better. If a program does not use dynamic compilation facilities such as `eval`, **demodularizing** it and removing unneeded code produces a smaller program that starts faster. `raco demod -g` performs that pruning and writes a single `.zo` file, which can then become an executable or a distribution. `raco cross` handles cross compilation.

## Why this matters

This page states the bundling route to a standalone executable, and the condition for improving on it, more plainly than [[raco-exe-creating-stand-alone-executables|the `raco exe` reference]]. By default the executable ships the whole runtime, so nothing about the program's dynamism is lost. Pruning becomes possible only once the program gives up `eval`, because only then can a tool know which code is unreachable. That is the same closed-world trade [[separate-compilation]] keeps returning to, in Chez's whole-program mode and Stalin, here offered as an optional final step.
