---
type: concept
status: reviewed
title: Attention Mechanism
created: 2026-06-23
tags: [transformers, machine-learning]
---

# Attention Mechanism

The mechanism inside a [[transformer]] that lets each token look at the other
tokens it is allowed to see and pull in information from them — the operation the
architecture is named for.

## Notes

Each token is projected into three vectors: a Query ("what am I looking for"), a
Key ("what do I offer"), and a Value ("what I pass along"). A scaled dot product
of one token's Query against every visible token's Key, passed through softmax,
produces weights for a weighted sum over the Value vectors. In decoder-only
[[large-language-model|language models]], causal masking drives the weight on
future tokens to ~zero so generation stays left-to-right.

**Multi-head attention** runs many such passes in parallel, each a learned
low-dimensional projection of the full token vector (not a fixed slice); heads
specialize during training (grammar, coreference, induction heads, and more).
Cost grows quadratically with sequence length, motivating efficiency work
(FlashAttention, sparse/linear attention). The KV cache stores past Keys and
Values to avoid recomputation during generation, and Grouped-Query Attention
(GQA) lets query heads share fewer key/value heads to cut that memory cost.

## Sources

- [[how-llms-actually-work|How LLMs Actually Work]]
