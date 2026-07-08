# Log

Append-only timeline of operations against the wiki (ingests now;
queries and lints later). Newest entries are appended at the bottom.

Each entry is a level-2 heading of the form:

```
## [<date>] <operation>: <subject>
```

so the log stays greppable by the stable `## [` prefix.

<!-- entries appended below this line -->

## [2026-06-22] ingest: Formal methods and the future of programming

- source: https://blog.janestreet.com/formal-methods-at-jane-street-index/ (converter: jina)
- summary: [[formal-methods-and-the-future-of-programming|Formal methods and the future of programming]]
- hubs touched: [[jane-street|Jane Street]], [[yaron-minsky|Yaron Minsky]], [[formal-methods|Formal Methods]], [[type-systems|Type Systems]], [[agentic-coding|Agentic Coding]], [[ocaml|OCaml]], [[oxcaml|OxCaml]] (all created)

## [2026-06-23] ingest: Plotnine: a grammar of graphics for Python

- source: https://plotnine.org/ (converter: jina)
- summary: [[plotnine-a-grammar-of-graphics-for-python|Plotnine: a grammar of graphics for Python]]
- hubs touched: [[plotnine|Plotnine]], [[grammar-of-graphics|Grammar of Graphics]], [[ggplot2|ggplot2]], [[python|Python]], [[data-visualization|Data Visualization]] (all created)

## [2026-06-23] ingest: Karpathy's LLM-Wiki pattern

- source: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f (converter: jina)
- summary: [[karpathys-llm-wiki-pattern|Karpathy's LLM-Wiki pattern]]
- hubs touched: [[andrej-karpathy|Andrej Karpathy]], [[llm-wiki|LLM Wiki]], [[retrieval-augmented-generation|Retrieval-Augmented Generation]], [[personal-knowledge-management|Personal Knowledge Management]], [[obsidian|Obsidian]], [[memex|Memex]] (all created)

## [2026-06-23] query: When to create an analysis entry

- question: What does Karpathy's llm-wiki article say about when to create an analysis entry?
- analysis: [[when-to-create-an-analysis-entry|When to create an analysis entry]]
- sources cited: [[karpathys-llm-wiki-pattern|Karpathy's LLM-Wiki pattern]], [[llm-wiki|LLM Wiki]]

## [2026-06-23] ingest: Satya Nadella: A frontier without an ecosystem is not stable

- source: https://x.com/satyanadella/status/2066182223213293753/ (converter: jina)
- summary: [[satya-nadella-a-frontier-without-an-ecosystem-is-not-stable|Satya Nadella: A frontier without an ecosystem is not stable]]
- hubs touched: [[satya-nadella|Satya Nadella]], [[microsoft|Microsoft]], [[human-capital|Human Capital]], [[token-capital|Token Capital]], [[learning-loop|Learning Loop]] (all created)

## [2026-06-23] ingest: How LLMs Actually Work

- source: https://www.0xkato.xyz/how-llms-actually-work/ (converter: jina, --images)
- summary: [[how-llms-actually-work|How LLMs Actually Work]]
- hubs touched: [[0xkato|0xkato]], [[transformer|Transformer]], [[attention-mechanism|Attention Mechanism]], [[large-language-model|Large Language Model]] (all created)
- images: 8 figures localized to raw/assets/2026-06-23-how-llms-actually-work/; 2 promoted to wiki/assets/ (transformer-pipeline.png, transformer-attention-heatmap.png)

## [2026-06-23] ingest: Why Janet?

- source: https://ianthehenry.com/posts/why-janet/ (converter: jina)
- summary: [[why-janet|Why Janet?]]
- hubs touched: [[ian-henry|Ian Henry]], [[janet|Janet]], [[lisp|Lisp]] (all created)
- images: none (text article)

## [2026-06-23] ingest: The Janet Programming Language

- source: https://janet-lang.org/ (converter: jina)
- summary: [[the-janet-programming-language|The Janet Programming Language]]
- hubs touched: [[janet|Janet]], [[lisp|Lisp]], [[ian-henry|Ian Henry]] (all existing; appended to Sources)
- images: none (text page)

## [2026-06-23] ingest: Bayesian modeling for unknown coordinates

- source: https://christopherkrapu.com/blog/2026/dont-know-where-your-data-is-from/ (converter: jina)
- summary: [[bayesian-modeling-for-unknown-coordinates|Bayesian modeling for unknown coordinates]]
- hubs touched: [[christopher-krapu|Christopher Krapu]], [[bayesian-inference|Bayesian Inference]], [[gaussian-process|Gaussian Process]], [[pymc|PyMC]] (all created)
- images: none (figure is code-generated, not in page markup)

## [2026-06-23] ingest: The Smallest Brain You Can Build

- source: https://ranpara.net/posts/perceptron-explained-from-scratch/ (converter: jina)
- summary: [[the-smallest-brain-you-can-build|The Smallest Brain You Can Build]]
- hubs touched: [[perceptron|Perceptron]], [[neural-network|Neural Network]] (both created)
- images: none (post uses interactive JS demos, no static figures)

## [2026-06-23] ingest: MCP is dead

- source: https://www.quandri.io/engineering-blog/mcp-is-dead (converter: jina)
- summary: [[mcp-is-dead|MCP is dead]]
- hubs touched: [[model-context-protocol|Model Context Protocol]], [[chloe-kim|Chloe Kim]], [[quandri|Quandri]] (created); [[large-language-model|Large Language Model]], [[agentic-coding|Agentic Coding]] (existing; appended to Sources)
- images: none (text post)

## [2026-06-23] ingest: Choosing to Stay Human

- source: https://www.oneusefulthing.org/p/choosing-to-stay-human (converter: jina)
- summary: [[choosing-to-stay-human|Choosing to Stay Human]]
- hubs touched: [[ethan-mollick|Ethan Mollick]], [[cognitive-surrender|Cognitive Surrender]] (both created)
- images: 4 localized to raw/assets/2026-06-23-choosing-to-stay-human/; img-1 (AI-writing parody) and img-2 (learning-mode screenshots) distilled to prose, img-3/img-4 (meta-joke) dropped; none promoted to wiki/assets/

## [2026-06-24] ingest: A Programmable Programming Language

- source: https://dl.acm.org/doi/10.1145/3127323 (converter: docling, from local PDF)
- summary: [[a-programmable-programming-language|A Programmable Programming Language]]
- hubs touched: [[racket|Racket]], [[language-oriented-programming|Language-Oriented Programming]], [[domain-specific-language|Domain-Specific Language]], [[matthias-felleisen|Matthias Felleisen]] (created); [[lisp|Lisp]], [[type-systems|Type Systems]] (existing; appended to Sources)
- images: none (PDF route; figures are code/diagrams, not localized)
- note: initial Jina capture of the ACM URL hit a Cloudflare bot wall; re-captured from a locally downloaded PDF via Docling. New tags: racket, language-oriented-programming, domain-specific-languages.

## [2026-06-29] ingest: libscheme: Scheme as a C Library

- source: https://github.com/bwbensonjr/libscheme/blob/main/src/doc/libscheme.md (raw URL fed to converter: https://raw.githubusercontent.com/bwbensonjr/libscheme/main/src/doc/libscheme.md; converter: markitdown, from text/plain Markdown)
- summary: [[libscheme-scheme-as-a-c-library|libscheme: Scheme as a C Library]]
- hubs touched: [[scheme|Scheme]], [[brent-benson|Brent W. Benson Jr.]] (created); [[lisp|Lisp]] (existing; appended to Sources)
- images: none (Markdown source; figures are inline code listings)
- note: source was already Markdown; the GitHub blob URL serves text/html (would route to Jina), so the raw.githubusercontent.com URL was used to get text/plain → MarkItDown passthrough. New tag: scheme.

## [2026-06-29] ingest: Porting Racket to Chez Scheme

- source: https://users.cs.utah.edu/~mflatt/tmp/rkt-on-chez.pdf (converter: docling, from PDF)
- summary: [[porting-racket-to-chez-scheme|Porting Racket to Chez Scheme]]
- hubs touched: [[chez-scheme|Chez Scheme]], [[matthew-flatt|Matthew Flatt]] (created); [[racket|Racket]], [[scheme|Scheme]], [[lisp|Lisp]], [[brent-benson|Brent W. Benson Jr.]] (existing; appended to Sources, strengthened Racket lineage note)
- images: none (PDF route; figures are diagrams/plots, not localized)
- note: source PDF is anonymized for review; attributed to Matthew Flatt et al. (ICFP 2019) per the user. This paper cites [[libscheme-scheme-as-a-c-library|libscheme]] (Benson 1994) as Racket's 1995 starting point. New tags: language-implementation, chez-scheme.

## [2026-07-08] ingest: Compiling with Continuations and LLVM

- source: https://arxiv.org/pdf/1805.08842 (converter: docling, arXiv PDF)
- summary: [[compiling-with-continuations-and-llvm|Compiling with Continuations and LLVM]]
- hubs touched: [[llvm|LLVM]], [[continuation-passing-style|Continuation-Passing Style]], [[standard-ml|Standard ML]], [[john-reppy|John Reppy]] (created); [[scheme|Scheme]] (existing; appended to Sources)
- images: none (PDF route; figures are code listings/diagrams, not localized)
- note: New tags: llvm, continuations, standard-ml. First author Kavon Farvardin named in prose (no entity page).

## [2026-07-08] ingest: The LLVM Compiler Infrastructure

- source: https://cacm.acm.org/federal-funding-of-academic-research/the-llvm-compiler-infrastructure/ (converter: jina)
- summary: [[the-llvm-compiler-infrastructure|The LLVM Compiler Infrastructure]]
- hubs touched: [[chris-lattner|Chris Lattner]], [[vikram-adve|Vikram Adve]], [[static-single-assignment|Static Single Assignment]] (created); [[llvm|LLVM]] (existing; enriched with origin/design/impact and appended to Sources)
- images: 1 localized to raw/assets/2026-07-08-the-llvm-compiler-infrastructure/; img-1 (LLVM architecture schematic) distilled to prose AND promoted to wiki/assets/llvm-compiler-architecture.jpg, embedded in the summary
- note: No new tags (reused llvm, language-implementation, programming-languages). Authors: Vikram Adve (1st), Chris Lattner (2nd).
