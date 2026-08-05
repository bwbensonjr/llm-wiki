---
type: summary
status: reviewed
title: Karpathy's LLM-Wiki pattern
created: 2026-06-23
source: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
raw: raw/2026-06-23-llm-wiki.md
tags: [knowledge-management, llm-agents, obsidian]
---

# Karpathy's LLM-Wiki pattern

## Summary

[[andrej-karpathy|Andrej Karpathy]]'s "LLM Wiki" gist describes a pattern for
[[personal-knowledge-management|personal knowledge bases]] that an LLM
incrementally **builds and maintains**. The central contrast is against
[[retrieval-augmented-generation|RAG]]: rather than re-retrieving and
re-synthesizing raw documents on every query, the LLM *compiles* knowledge once
into a persistent, interlinked wiki of Markdown files and keeps it current — a
**compounding artifact** whose cross-references, contradiction flags, and
synthesis already exist and grow richer with every source and question.

The architecture has three layers: immutable **raw sources** (the source of
truth, never modified), the LLM-owned **wiki** (summaries, entity/concept pages,
comparisons — the human reads, the LLM writes), and a **schema** file
(`CLAUDE.md`/`AGENTS.md`) encoding conventions and workflows, co-evolved by human
and LLM.

Three operations drive it: **Ingest** (drop a source; the LLM reads, discusses,
summarizes, and updates ~10–15 pages plus the index and log), **Query** (ask
questions; the LLM finds pages via the index and synthesizes a cited answer —
and good answers file back as new pages so explorations compound), and **Lint**
(periodic health checks for contradictions, stale claims, orphan pages, and
missing cross-references). Two navigation files anchor it: `index.md` (a content
catalog, read first at query time) and `log.md` (an append-only, greppable
chronological record). Index-first navigation reportedly works well to ~100
sources without embedding-based [[retrieval-augmented-generation|RAG]]
infrastructure.

The division of labor is the crux: the human curates sources, asks good
questions, and judges what it all means; the LLM does the bookkeeping that causes
humans to abandon wikis — *"LLMs don't get bored."* Karpathy ties the idea to
[[memex|Memex]] (1945), whose unsolved problem — who does the maintenance — the
LLM now handles. The wiki is meant to be browsed in [[obsidian|Obsidian]]: the
editor is the IDE, the LLM is the programmer, the wiki is the codebase.

## Why this matters

This article matters because it is the basis for the architecture of this
llm-wiki project.
