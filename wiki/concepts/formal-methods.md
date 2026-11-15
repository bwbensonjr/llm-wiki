---
type: concept
title: Formal Methods
created: 2026-06-22
tags: [formal-methods, program-verification]
---

# Formal Methods

Mathematically rigorous techniques for specifying and proving properties of
software, giving universal (`∀`) guarantees that testing cannot. Historically
expensive — seL4 famously took ~25 person-years to verify 8,700 lines of C.

## Notes

- [[type-systems|Type systems]] are a lightweight, widely-used form of formal
  method.
- [[agentic-coding|Agentic coding]] is reshaping the cost/benefit calculus:
  models lower the cost of writing proofs and raise the value of machine-checked
  guarantees as a feedback signal.
- Tooling landscape: Lean, Dafny, Rocq, Agda, Iris.
- [[legislation-formalization|Legislation formalization]] extends the approach to
  statutory structures and executable rules. [[lexifina|Lexifina]] uses
  [[lean-proof-assistant|Lean]] for drafting certificates and tax-model proofs;
  proof checking does not establish the fidelity of the translation from law.

## Sources

- [[formal-methods-and-the-future-of-programming|Formal methods and the future of programming]]
- [[closure-conversion-is-safe-for-space|Closure Conversion Is Safe for Space]]
- [[formalizing-the-us-tax-code|Formalizing the US tax code]]
