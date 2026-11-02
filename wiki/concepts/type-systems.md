---
type: concept
title: Type Systems
created: 2026-06-22
tags: [type-systems, formal-methods]
---

# Type Systems

Static checks that constrain what programs can express, providing universal
guarantees at compile time. Framed as a "lightweight formal method": cheap to
adopt yet capable of eliminating whole classes of bugs by construction.

## Notes

- Used at [[jane-street|Jane Street]] to rule out entire defect categories
  (e.g. data races, cross-site scripting) rather than merely test for them.
- Seen as especially valuable when programming with agents: the `∀` guarantees
  give reliable feedback that agent-generated code respects invariants.
- In [[racket]], a type system is one point on a spectrum of soundness: a
  language can be equipped with static checking (`typed/racket`, `typed/video`),
  built using the `turnstile` eDSL for expressing type systems, or rely instead
  on runtime contracts.

## Sources

- [[formal-methods-and-the-future-of-programming|Formal methods and the future of programming]]
- [[a-programmable-programming-language|A Programmable Programming Language]]
