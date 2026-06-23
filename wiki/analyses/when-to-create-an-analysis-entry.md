---
type: analysis
title: When to create an analysis entry
created: 2026-06-23
question: What does Karpathy's llm-wiki article say about when to create an analysis entry?
tags: [knowledge-management, llm-agents]
sources: ["[[karpathys-llm-wiki-pattern]]", "[[llm-wiki]]"]
---

# When to create an analysis entry

## Answer

Karpathy's article frames analysis-creation as part of the **Query** operation,
not a separate step you plan in advance. The guidance is: when you ask a
question, the LLM finds pages and synthesizes a cited answer — and **good answers
should be filed back into the wiki as new pages so that explorations compound**
the same way ingested sources do ([[karpathys-llm-wiki-pattern]]).

The test for *when* is therefore about the **value and durability** of the
answer rather than a fixed trigger. The article's own examples of what is worth
filing are *a comparison you asked for, an analysis, or a connection you
discovered* — things that "are valuable and shouldn't disappear into chat
history." A throwaway lookup need not become a page; a synthesis you would want
to keep, cite, or build on should.

The underlying rationale traces to the pattern's central idea ([[llm-wiki]]):
the wiki is a **compounding artifact** whose synthesis grows richer with every
source *and every question*. Filing answers back is how the "every question"
half of that compounding actually happens — otherwise queries leave no residue.
This sits alongside the other two operations the pattern describes, Ingest and
Lint.

## Why this matters

I want to file this analysis to clarify when an analysis entry needs to be
created (which is quite meta and circular, I admit).
