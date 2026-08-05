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
- [[the-smallest-brain-you-can-build|The Smallest Brain You Can Build]] — a from-scratch, math-light Python build of a perceptron, showing weights, bias, the decision boundary, and the learning rule.
- [[mcp-is-dead|MCP is dead]] — Quandri argues MCP is over-engineered vs CLIs/Skills for connecting LLMs to tools, with token and reliability measurements.
- [[choosing-to-stay-human|Choosing to Stay Human]] — Ethan Mollick on intentional AI use and the risk of cognitive surrender, with evidence from AI-in-education and consulting studies.
- [[a-programmable-programming-language|A Programmable Programming Language]] — the Racket Manifesto (CACM 2018): the case for language-oriented programming, building and soundly composing domain-specific languages.
- [[libscheme-scheme-as-a-c-library|libscheme: Scheme as a C Library]] — USENIX 1994 VHLL paper: making Scheme an embeddable C library in the mold of Tcl, easily extended with new primitives, types, and syntax.
- [[porting-racket-to-chez-scheme|Porting Racket to Chez Scheme]] — ICFP 2019 experience report on Racket CS: rebuilding Racket atop Chez Scheme via linklets and schemify, with ~30 mismatches to reconcile.
- [[compiling-with-continuations-and-llvm|Compiling with Continuations and LLVM]] — ML Workshop 2018: an LLVM backend supporting heap-allocated first-class continuations via a new JWA calling convention, in the Manticore/PML compiler.
- [[the-llvm-compiler-infrastructure|The LLVM Compiler Infrastructure]] — CACM 2026: the origin, five-capability design, and vast industry/research impact of LLVM, framed as a case for federal research funding.
- [[rabbit-a-compiler-for-scheme|RABBIT: A Compiler for Scheme]] — Steele's 1977 MIT dissertation: LAMBDA as rename plus GOTO, a tiny basis set extended by macros, and CPS as a compiler IR.
- [[orbit-an-optimizing-compiler-for-scheme|ORBIT: An Optimizing Compiler for Scheme]] — Kranz's 1988 Yale dissertation: closure and escape analysis make Scheme match Pascal, and beat it wherever calls dominate.
- [[an-incremental-approach-to-compiler-construction|An Incremental Approach to Compiler Construction]] — Ghuloum (Scheme Workshop 2006): a Scheme-to-x86 compiler in 24 steps, each one a fully working compiler for a larger subset.
- [[lambda-the-ultimate-label-a-simple-optimizing-compiler-for-scheme|Lambda, the Ultimate Label: A Simple Optimizing Compiler for Scheme]] — Clinger & Hansen (LFP '94): heap-allocate everything, then lambda-lift it back into registers; a lifted lambda is an assembly label.
- [[western-sahara|Western Sahara]] — Wikipedia on the UN non-self-governing territory: the unresolved sovereignty dispute, the Berm, the stalled referendum. Off-topic for this corpus; queued as a review test.

## Entities

- [[jane-street|Jane Street]] — trading firm known for its OCaml use and language tooling.
- [[yaron-minsky|Yaron Minsky]] — brought OCaml to Jane Street (2002); author of the formal-methods announcement.
- [[andrej-karpathy|Andrej Karpathy]] — AI researcher; author of the LLM-Wiki pattern.
- [[satya-nadella|Satya Nadella]] — Microsoft CEO; author of the human-capital/token-capital thread.
- [[microsoft|Microsoft]] — technology company led by Satya Nadella.
- [[0xkato|0xkato]] — writer/researcher; author of the "How LLMs Actually Work" explainer.
- [[ian-henry|Ian Henry]] — programmer/writer; author of *Janet for Mortals* and the "Why Janet?" pitch.
- [[christopher-krapu|Christopher Krapu]] — data scientist/writer on Bayesian modeling, Gaussian processes, and spatial statistics.
- [[chloe-kim|Chloe Kim]] — backend engineer at Quandri; author of "MCP is dead."
- [[quandri|Quandri]] — software company; its engineering blog published "MCP is dead."
- [[ethan-mollick|Ethan Mollick]] — Wharton professor; author of *One Useful Thing* and *Co-Intelligence*, writing on practical AI use.
- [[matthias-felleisen|Matthias Felleisen]] — Northeastern professor; principal architect of Racket and lead author of the Racket Manifesto.
- [[brent-benson|Brent W. Benson Jr.]] — software engineer and curator of this wiki; author of libscheme.
- [[matthew-flatt|Matthew Flatt]] — University of Utah; principal architect of Racket; led the Racket-on-Chez-Scheme rebuild.
- [[john-reppy|John Reppy]] — University of Chicago; Concurrent ML, SML/NJ, and the Manticore project; co-author of the continuations-and-LLVM paper.
- [[chris-lattner|Chris Lattner]] — creator of LLVM's core (as a UIUC Ph.D. student); later built Clang, Swift, and MLIR at Apple.
- [[vikram-adve|Vikram Adve]] — UIUC professor and LLVM's faculty originator; his NSF CAREER grant funded the early work.
- [[guy-steele|Guy L. Steele Jr.]] — co-inventor of Scheme with Gerald Jay Sussman; author of RABBIT and the Lambda Papers.
- [[david-kranz|David A. Kranz]] — Yale T project; built the ORBIT compiler and its closure-analysis algorithms.
- [[abdulaziz-ghuloum|Abdulaziz Ghuloum]] — Scheme implementer (Ikarus); author of the incremental compiler-construction tutorial.
- [[william-clinger|William D. Clinger]] — designer of Twobit and Larceny; argues an optimizing Scheme compiler can be simple.

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
- [[perceptron|Perceptron]] — the simplest neural unit: weighted sum plus bias through a threshold, trained by the perceptron rule.
- [[neural-network|Neural Network]] — layered composition of neuron-like units; the perceptron is its smallest building block.
- [[model-context-protocol|Model Context Protocol]] — protocol connecting LLMs to external tools; critiqued for context bloat vs CLIs/Skills.
- [[cognitive-surrender|Cognitive Surrender]] — deferring one's thinking to an AI and accepting its output even when wrong; the antidote is intentional use.
- [[racket|Racket]] — a Lisp/Scheme-family language and 20-year research project built as a platform for language-oriented programming.
- [[language-oriented-programming|Language-Oriented Programming]] — paradigm of solving each problem aspect in a domain-specific language and composing the components into one system.
- [[domain-specific-language|Domain-Specific Language]] — a language specialized to a problem domain; the building block that language-oriented programming composes.
- [[scheme|Scheme]] — a small, lexically-scoped dialect of Lisp; the trunk from which Racket descends and the language libscheme embeds into C.
- [[chez-scheme|Chez Scheme]] — a high-performance, optimizing-compiler R6RS Scheme implementation; the target VM that modern Racket (Racket CS) runs on.
- [[llvm|LLVM]] — an SSA-based compiler backend infrastructure; a popular but C-biased target that functional-language compilers must work around.
- [[continuation-passing-style|Continuation-Passing Style]] — making control flow explicit so every call is a tail call; basis of the heap-allocated first-class continuation runtime model.
- [[standard-ml|Standard ML]] — a statically-typed ML-family functional language with a long line of compiler-implementation research (SML/NJ, MLton, Manticore).
- [[static-single-assignment|Static Single Assignment]] — an IR form where each variable is assigned once, with ϕ-operations at control-flow merges; the basis of LLVM IR.
- [[lambda-papers|Lambda Papers]] — the 1975–1980 MIT memos by Steele and Sussman in which Scheme was invented and its compilation worked out.
- [[lambda-calculus|Lambda Calculus]] — Church's formal system of function abstraction and application; alpha- and beta-conversion are the compiler's substitution rules.
- [[tail-recursion|Tail Recursion]] — a tail call consumes no control stack, so a call compiles to a GOTO that passes arguments; a defining requirement of Scheme.
- [[closure-conversion|Closure Conversion]] — turning nested lexical functions into code plus captured environment, and deciding which need a run-time closure at all.
- [[escape-analysis|Escape Analysis]] — deciding whether a closure outlives its creating context, and so whether it must go on the heap rather than the stack or registers.
- [[t-programming-language|T (Programming Language)]] — Yale's 1980s Scheme dialect, both the source and the implementation language of the ORBIT compiler.
- [[lambda-lifting|Lambda Lifting]] — turning a nested function's non-local variables into extra parameters so it can be hoisted to a top-level label.
- [[larceny|Larceny]] — Scheme implementation built on the Twobit compiler; a research vehicle for how programming style affects GC performance.

## Analyses

- [[when-to-create-an-analysis-entry|When to create an analysis entry]] — per Karpathy, file a query answer back when it's a durable synthesis, comparison, or discovered connection worth keeping.
