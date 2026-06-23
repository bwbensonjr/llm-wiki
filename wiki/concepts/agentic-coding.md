---
type: concept
title: Agentic Coding
created: 2026-06-22
tags: [agentic-coding]
---

# Agentic Coding

Using LLM agents to write software. Agents are good at achieving a stated goal
but tend toward "slop" — overly complex code with corner-case bugs that ignores
codebase invariants — which shifts effort onto verifying their output.

## Notes

- Creates a *verification bottleneck*: the gap between code an agent generates
  and code worth releasing.
- Agents "thrive on feedback," both in RL training and in use;
  [[formal-methods|formal methods]] and [[type-systems|type systems]] are
  powerful feedback signals that improve their results.
- This dynamic is why [[jane-street|Jane Street]] reconsidered formal methods in
  2026.

## Sources

- [[formal-methods-and-the-future-of-programming|Formal methods and the future of programming]]
