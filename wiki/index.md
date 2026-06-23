# Index

Catalog of every page in the wiki, grouped by type. Each entry is a
`[[wikilink]]` followed by a one-line summary. Updated on every ingest.

## Summaries

- [[formal-methods-and-the-future-of-programming|Formal methods and the future of programming]] — Jane Street reverses course and embraces formal methods as agentic coding shifts the cost/benefit calculus.
- [[plotnine-a-grammar-of-graphics-for-python|Plotnine: a grammar of graphics for Python]] — a Python plotting library built on the grammar of graphics, modeled on R's ggplot2.
- [[karpathys-llm-wiki-pattern|Karpathy's LLM-Wiki pattern]] — the design basis for this project: an LLM incrementally builds and maintains a compounding Markdown wiki.
- [[satya-nadella-a-frontier-without-an-ecosystem-is-not-stable|Satya Nadella: A frontier without an ecosystem is not stable]] — firms must compound human capital and token capital via a learning loop, and build a frontier ecosystem rather than ceding value to a few models.
- [[how-llms-actually-work|How LLMs Actually Work]] — an intuition-first, math-light walkthrough of the transformer architecture behind modern LLMs, one forward pass end to end.
- [[why-janet|Why Janet?]] — a sales pitch for Janet, a small practical Lisp dialect, spanning simplicity, native binaries, PEGs, macros, and compile-time-to-run-time values.
- [[the-janet-programming-language|The Janet Programming Language]] — Janet's official homepage: use cases, feature list, C99 embeddability, the jpm build tool, and the library/editor ecosystem.
- [[bayesian-modeling-for-unknown-coordinates|Bayesian modeling for unknown coordinates]] — a Bayesian Gaussian-process model for spatial data whose point locations are observed with noise, worked in PyMC on the Walker Lake uranium data.

## Entities

- [[jane-street|Jane Street]] — trading firm known for its OCaml use and language tooling.
- [[yaron-minsky|Yaron Minsky]] — brought OCaml to Jane Street (2002); author of the formal-methods announcement.
- [[andrej-karpathy|Andrej Karpathy]] — AI researcher; author of the LLM-Wiki pattern.
- [[satya-nadella|Satya Nadella]] — Microsoft CEO; author of the human-capital/token-capital thread.
- [[microsoft|Microsoft]] — technology company led by Satya Nadella.
- [[0xkato|0xkato]] — writer/researcher; author of the "How LLMs Actually Work" explainer.
- [[ian-henry|Ian Henry]] — programmer/writer; author of *Janet for Mortals* and the "Why Janet?" pitch.
- [[christopher-krapu|Christopher Krapu]] — data scientist/writer on Bayesian modeling, Gaussian processes, and spatial statistics.

## Concepts

- [[formal-methods|Formal Methods]] — rigorous techniques for proving software properties; historically costly.
- [[type-systems|Type Systems]] — static checks as a lightweight formal method giving universal guarantees.
- [[agentic-coding|Agentic Coding]] — using LLM agents to write code; creates a verification bottleneck.
- [[ocaml|OCaml]] — statically-typed functional language; Jane Street's primary language.
- [[oxcaml|OxCaml]] — Jane Street's OCaml dialect and proving ground for advanced type features.
- [[plotnine|Plotnine]] — Python data-visualization library implementing the grammar of graphics.
- [[grammar-of-graphics|Grammar of Graphics]] — system for composing plots from data, layers, scales, and facets.
- [[ggplot2|ggplot2]] — R's grammar-of-graphics package; the model Plotnine mirrors.
- [[python|Python]] — general-purpose language widely used for data analysis; host for Plotnine.
- [[data-visualization|Data Visualization]] — representing data graphically for exploration and communication.
- [[llm-wiki|LLM Wiki]] — pattern where an LLM builds and maintains a compounding, interlinked Markdown wiki.
- [[retrieval-augmented-generation|Retrieval-Augmented Generation]] — query-time retrieval over raw documents; the approach the LLM-Wiki pattern contrasts against.
- [[personal-knowledge-management|Personal Knowledge Management]] — accumulating and connecting one's own knowledge over time.
- [[obsidian|Obsidian]] — local-first Markdown editor; the human's read-side IDE for the wiki.
- [[memex|Memex]] — Vannevar Bush's 1945 associative knowledge store; precursor to the LLM-Wiki idea.
- [[human-capital|Human Capital]] — the knowledge, judgment, and ingenuity of a firm's people; grows more valuable as AI capability grows.
- [[token-capital|Token Capital]] — the AI capability a firm builds and owns; compounds with human capital.
- [[learning-loop|Learning Loop]] — the compounding human+AI "hill climbing machine" that becomes a firm's new IP.
- [[transformer|Transformer]] — the stacked attention + feed-forward architecture most modern LLMs are built from.
- [[attention-mechanism|Attention Mechanism]] — how each token pulls information from the other tokens it can see, via Query/Key/Value.
- [[large-language-model|Large Language Model]] — a next-token predictor built on the transformer; base behavior plus post-training.
- [[janet|Janet]] — a small, practical Lisp dialect: easy to embed, compiles to self-contained native binaries, strong at text parsing.
- [[lisp|Lisp]] — the family of parenthesized, s-expression languages built on code-as-data and macros.
- [[bayesian-inference|Bayesian Inference]] — updating prior beliefs to posteriors given data; flexible model-building plus Monte Carlo estimation.
- [[gaussian-process|Gaussian Process]] — a kernel-defined distribution over functions used as a flexible regression prior.
- [[pymc|PyMC]] — a Python probabilistic-programming library for Bayesian modeling with MCMC.

## Analyses

- [[when-to-create-an-analysis-entry|When to create an analysis entry]] — per Karpathy, file a query answer back when it's a durable synthesis, comparison, or discovered connection worth keeping.
