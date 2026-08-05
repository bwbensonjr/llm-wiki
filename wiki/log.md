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

## [2026-08-05] ingest: RABBIT: A Compiler for Scheme

- source: https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html (converter: jina)
- run: **unattended** (`ingest-inbox`, queue entry with curator note "Seminal Scheme compiler paper by co-inventor of Scheme")
- summary: [[rabbit-a-compiler-for-scheme|RABBIT: A Compiler for Scheme]]
- hubs touched: [[guy-steele|Guy L. Steele Jr.]], [[lambda-papers|Lambda Papers]], [[lambda-calculus|Lambda Calculus]], [[tail-recursion|Tail Recursion]], [[closure-conversion|Closure Conversion]] (created, all `status: provisional`); [[scheme|Scheme]], [[lisp|Lisp]], [[continuation-passing-style|Continuation-Passing Style]] (existing, left `status: reviewed`; appended to Sources and given an origin note)
- images: none (Jina route localized no content images; the source is a text transcription)
- tags minted: **none** — reused programming-languages, language-implementation, scheme, lisp, continuations
- note: source is Roger Turner's abridged CC BY-NC transcription of Steele 1978 (MIT AI-TR-474), covering the chapter "Compiler Optimization Based on Viewing LAMBDA as RENAME plus GOTO". Gerald Jay Sussman named in prose (no entity page). Titled by the dissertation's name rather than the transcription's page title.

## [2026-08-05] ingest: ORBIT: An Optimizing Compiler for Scheme

- source: https://www.ccs.neu.edu/home/shivers/cs6983/papers/kranz-diss-tr632.pdf (converter: docling)
- run: **unattended** (`ingest-inbox`, queue entry with curator note "Motivation and details of closure analysis and CPS transformation")
- summary: [[orbit-an-optimizing-compiler-for-scheme|ORBIT: An Optimizing Compiler for Scheme]]
- hubs touched: [[david-kranz|David A. Kranz]], [[escape-analysis|Escape Analysis]], [[t-programming-language|T (Programming Language)]] (created, all `status: provisional`); [[closure-conversion|Closure Conversion]], [[tail-recursion|Tail Recursion]] (existing but `provisional` from this run's earlier RABBIT ingest; enriched and appended to Sources); [[continuation-passing-style|Continuation-Passing Style]], [[scheme|Scheme]], [[lisp|Lisp]] (existing, left `status: reviewed`; appended to Sources)
- images: none (PDF route — image localization is scoped to the web/Jina route; the twin carries one `<!-- image -->` placeholder for a closure-layout diagram that was not extracted)
- tags minted: **none** — reused programming-languages, language-implementation, scheme, lisp, continuations
- note: **conversion artifacts** — docling rendered this 1988 PDF's ligatures and digits as escape sequences (`/#0C`→fi, `/#0E`→ffi, `/#2F`→/, digits prefixed by `/`). The text is systematically decodable and the summary reads through it, but the raw twin is noisy; worth a spot-check at review. Kranz builds directly on [[rabbit-a-compiler-for-scheme|RABBIT]], ingested earlier in this same run — the RABBIT ingest's new hubs were available to link, which is the sequential-processing rule working as intended.

## [2026-08-05] ingest: An Incremental Approach to Compiler Construction

- source: http://scheme2006.cs.uchicago.edu/11-ghuloum.pdf (converter: docling)
- run: **unattended** (`ingest-inbox`, queue entry with curator note "Introduces the nanopass idea of incremental compiler transformations")
- summary: [[an-incremental-approach-to-compiler-construction|An Incremental Approach to Compiler Construction]]
- hubs touched: [[abdulaziz-ghuloum|Abdulaziz Ghuloum]] (created, `status: provisional`); [[closure-conversion|Closure Conversion]], [[tail-recursion|Tail Recursion]] (provisional from earlier in this run; enriched with Ghuloum's minimal formulations and appended to Sources); [[scheme|Scheme]], [[lisp|Lisp]] (existing, left `status: reviewed`; appended to Sources)
- images: none (PDF route; the twin carries `<!-- image -->` placeholders for the tail-call frame diagram and one undecoded formula)
- tags minted: **none** — reused programming-languages, language-implementation, scheme, lisp, and education (previously used only by [[choosing-to-stay-human|Choosing to Stay Human]]; applied here for the paper's explicit CS-education framing)
- note: **the curator note does not match the source.** The note calls this the origin of "the nanopass idea," but the paper never mentions nanopass and is not about it: Ghuloum's incrementality is 24 *progressively larger source-language subsets*, each yielding a working compiler, whereas nanopass (Sarkar, Waddell, Dybvig) decomposes a single compiler into many tiny passes. The two share the Indiana/Dybvig lineage — Ghuloum thanks Dybvig and cites Waddell/Sarkar/Dybvig's "Fixing letrec" — which likely explains the association. The drafted `## Why this matters` honors the curator's interest while drawing the distinction explicitly rather than repeating the claim. **Flagged for `curate`:** confirm the framing, and consider whether nanopass warrants its own concept hub (deliberately not minted here, since no ingested source covers it).
