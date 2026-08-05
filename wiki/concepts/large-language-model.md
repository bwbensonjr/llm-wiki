---
type: concept
status: reviewed
title: Large Language Model
created: 2026-06-23
tags: [llm, machine-learning]
---

# Large Language Model

A model trained to predict the next token over large amounts of text, almost
always built on the [[transformer]] architecture (LLM).

## Notes

A base LLM has a single training objective — next-token prediction — and is not
directly trained for factual accuracy, reasoning, or conversation; those
behaviors come from post-training (instruction tuning, learning from human
feedback, safety). Generation is a loop: the final token's vector becomes logits
over the vocabulary, softmax (shaped by temperature, top-k, top-p) yields a
distribution, a token is sampled and appended, and the model runs again, usually
reusing the KV cache. Speculative decoding speeds this up with a small draft
model verified in parallel by the large one.

Modern families (GPT, Claude, Gemini, LLaMA, Mistral) share the same
[[transformer]] skeleton and differ mainly in trained weights, configuration, and
post-training.

## Sources

- [[how-llms-actually-work|How LLMs Actually Work]]
- [[mcp-is-dead|MCP is dead]]
