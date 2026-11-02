---
type: summary
title: How LLMs Actually Work
created: 2026-06-23
source: https://www.0xkato.xyz/how-llms-actually-work/
raw: raw/2026-06-23-how-llms-actually-work.md
tags: [llm, transformers, machine-learning]
---

# How LLMs Actually Work

## Summary

A from-scratch walkthrough by [[0xkato]] of the [[transformer]] architecture
underlying most modern [[large-language-model|large language models]], written
to make model papers and model cards legible. It traces one forward pass end to
end — text → tokenizer → embedding lookup → positional encoding → N stacked
transformer blocks (attention + feed-forward) → unembedding → softmax → next
token.

![[transformer-pipeline.png]]

**Tokenization** turns text into integer IDs over a fixed subword vocabulary
(tens of thousands to hundreds of thousands of entries); subword pieces trade
off vocabulary size against generalization, and operating on token IDs rather
than letters explains failures like miscounting the R's in "strawberry."
**Embeddings** map each ID to a learned vector (≈4,096 numbers in 7B-class
models); semantically similar tokens land near each other, and vector arithmetic
(king − man + woman ≈ queen) reflects learned geometry. **Positional encoding**
injects word order: the original sinusoidal additive scheme gave way to RoPE,
which rotates Query/Key vectors by a position-dependent angle so attention sees
relative distance, generalizes to longer contexts, and adds no parameters —
though a "lost in the middle" effect persists.

The [[attention-mechanism|attention mechanism]] gives each token Query, Key, and
Value vectors; a scaled dot product of Queries against Keys, passed through
softmax, weights a sum over Values so a token pulls information from earlier
tokens. Causal masking zeroes future tokens for left-to-right generation, and
induction heads (Anthropic, 2022) copy "A B … A → B" patterns underlying
in-context learning; cost grows quadratically with length.

![[transformer-attention-heatmap.png]]

**Multi-head attention** runs many passes in parallel, each a learned
low-dimensional projection (not a fixed slice) of the full vector, with heads
specializing during training; the KV cache and Grouped-Query Attention (GQA) cut
the memory cost. The **feed-forward network** (per-token expand → non-linearity →
compress; ReLU → GELU → SwiGLU) holds most of the parameters and much of the
model's stored factual structure (editable via methods like ROME); Mixture of
Experts scales parameters without proportional compute. The **residual stream**
adds each sub-block's output back to the token vector (a ResNet idea) to keep
deep stacks trainable and is the central object of interpretability, while layer
normalization (modern models favor pre-norm and RMSNorm) keeps it stable.
**Next-token prediction** converts the last token's vector to logits, applies
softmax shaped by temperature/top-k/top-p, samples, appends, and loops.

The closing point: GPT, Claude, Gemini, and LLaMA differ mostly in trained
weights, configuration, and post-training — not the skeleton. The 2023–2025 stack
converged independently on pre-norm, RMSNorm, RoPE, SwiGLU, GQA, and (at the
largest scale) MoE; state-space models like Mamba are credible alternatives, but
tokens, embeddings, positional encoding, attention, the feed-forward network, the
residual stream, and next-token prediction are the durable problems any sequence
model must solve.

## Why this matters

This matters because it is a succinct description of how LLMs work with
well-thought-out, simple figures.
