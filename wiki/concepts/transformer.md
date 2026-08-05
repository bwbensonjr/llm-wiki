---
type: concept
status: reviewed
title: Transformer
created: 2026-06-23
tags: [transformers, machine-learning]
---

# Transformer

The neural-network architecture (Vaswani et al., 2017) that most modern
[[large-language-model|large language models]] are built from, by stacking
identical blocks of [[attention-mechanism|attention]] and feed-forward layers.

## Notes

A transformer processes a sequence in one forward pass: tokenization →
embeddings → positional encoding → N stacked blocks (each an
[[attention-mechanism|attention]] sub-layer plus a feed-forward network, wrapped
in residual connections and normalization) → unembedding → softmax over the
vocabulary. Information moves between tokens only in the attention sub-layer; the
feed-forward network processes each token independently and holds most of the
parameters.

Most of the architecture is shared across model families — what differs between
GPT, Claude, Gemini, and LLaMA is mostly trained weights, configuration (layer
count, head count, dense vs. Mixture of Experts), and post-training. The
2023–2025 stack converged independently on pre-norm placement, RMSNorm, rotary
position embeddings (RoPE), SwiGLU, and Grouped-Query Attention. State-space
models such as Mamba are credible alternatives for very long sequences, but the
transformer absorbed much of the field across language, vision, and audio.

## Sources

- [[how-llms-actually-work|How LLMs Actually Work]]
