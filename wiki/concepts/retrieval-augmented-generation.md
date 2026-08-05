---
type: concept
status: reviewed
title: Retrieval-Augmented Generation
created: 2026-06-23
tags: [llm-agents]
---

# Retrieval-Augmented Generation

Grounding an LLM's answer by retrieving relevant chunks from a document
collection at query time and generating from them (RAG).

## Notes

The approach the [[llm-wiki|LLM-Wiki]] pattern contrasts itself against: RAG
re-discovers knowledge from raw documents on every question, so nothing
accumulates — a subtle question spanning several documents must re-find and
re-piece the fragments each time. The LLM-Wiki pattern instead compiles the
knowledge once into a maintained wiki, and at moderate scale (~100 sources)
relies on index-first navigation rather than embedding-based RAG.

## Sources

- [[karpathys-llm-wiki-pattern|Karpathy's LLM-Wiki pattern]]
