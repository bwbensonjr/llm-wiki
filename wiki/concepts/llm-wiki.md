---
type: concept
title: LLM Wiki
created: 2026-06-23
tags: [knowledge-management, llm-agents]
---

# LLM Wiki

A pattern in which an LLM incrementally builds and maintains a persistent,
interlinked wiki of Markdown files that sits between a curator and their raw
sources.

## Notes

The defining move is to *compile* knowledge once and keep it current, rather
than re-deriving it on every query as [[retrieval-augmented-generation|RAG]]
does — making the wiki a **compounding artifact**. Built on three layers
(immutable raw sources, the LLM-owned wiki, and a schema file) and three
operations (ingest, query, lint), with `index.md` and `log.md` for navigation.
The human curates and asks; the LLM does the bookkeeping. This project is one
instantiation of the pattern; see [[memex|Memex]] for its acknowledged
precursor.

## Sources

- [[karpathys-llm-wiki-pattern|Karpathy's LLM-Wiki pattern]]
- [[when-to-create-an-analysis-entry|When to create an analysis entry]] (analysis)
