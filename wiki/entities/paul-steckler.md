---
type: entity
status: reviewed
title: Paul A. Steckler
created: 2026-08-05
tags: [programming-languages, language-implementation, program-verification]
---

# Paul A. Steckler

A programming-languages researcher, first author with [[mitchell-wand|Mitchell Wand]] of
[[lightweight-closure-conversion|Lightweight Closure Conversion]] — the flow analysis and
correctness proof for omitting a procedure's captured variables when its call sites can
supply them instead. The work formed part of his Northeastern PhD dissertation; by
publication he had moved to the University of Technology, Sydney.

His contribution to the [[closure-conversion]] literature is the proof obligation rather
than the optimization: the transformation's payoff was already plausible, and what the
paper supplies is a deductive system whose constraint solutions justify it, together with
the semantic machinery — occurrence closures, an evaluator preserving them, invariance
sets — needed to state correctness for a higher-order language at all.

## Sources

- [[lightweight-closure-conversion|Lightweight Closure Conversion]]
