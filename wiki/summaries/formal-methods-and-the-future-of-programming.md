---
type: summary
title: Formal methods and the future of programming
created: 2026-06-22
source: https://blog.janestreet.com/formal-methods-at-jane-street-index/
raw: raw/2026-06-22-formal-methods-at-jane-street-index.md
tags: [formal-methods, type-systems, agentic-coding, program-verification]
---

# Formal methods and the future of programming

## Summary

[[yaron-minsky|Yaron Minsky]] announces that [[jane-street|Jane Street]] —
after 25 years of treating full [[formal-methods|formal methods]] as not worth
the cost — is now building a team around them. The trigger is
[[agentic-coding|agentic coding]]: LLMs lower the cost of constructing proofs
(broadening who can use these tools productively) while raising the benefit,
because agent-generated code creates a *verification bottleneck* and agents
themselves "thrive on feedback."

The post frames [[type-systems|type systems]] as a lightweight formal method
Jane Street already relies on — universal `∀` guarantees that can eliminate
whole classes of bugs (data races, cross-site scripting) by construction, as
seen in [[oxcaml|OxCaml]]. Minsky argues Jane Street is well-positioned because
it controls its own language (so it can shape it toward proof-oriented
techniques) and has a user base eager for stronger guarantees. seL4 is cited as
the cautionary cost example (25 person-years to verify 8,700 lines of C), and
the post nods to outside tools like Lean, Dafny, Rocq, Agda, and Iris.

## Why this matters

I am always interested in Yaron Minsky and the Jane Street take on things
because of their great taste in programming languages (OCaml) and tool
building. Their takes on AI are also becoming important, and this formal methods
interest may end up being important to other trendsetters as well.
