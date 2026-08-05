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

## [2026-08-05] ingest: inbox run summary (1 entry parked)

- run: **unattended** (`ingest-inbox`), 4 queue entries — 3 ingested, 1 parked
- parked: http://foo.bar.baz/bad-link — 2026-08-05: capture failed, DNS could not resolve host `foo.bar.baz`. No `raw/` twin and no `wiki/` page were written; the entry is marked `- [!]` in `inbox.md` so later runs skip it. Failure isolation held: the three preceding entries were already committed and were unaffected.

## [2026-08-05] curate: first review of the unattended compiler-lineage batch

- queue drained: 12 provisional pages (3 summaries, 6 concepts, 3 entities), all from today's `ingest-inbox` run — 0 days of review debt
- **endorsed as written** (status flip only): [[rabbit-a-compiler-for-scheme|RABBIT: A Compiler for Scheme]], [[orbit-an-optimizing-compiler-for-scheme|ORBIT: An Optimizing Compiler for Scheme]], [[an-incremental-approach-to-compiler-construction|An Incremental Approach to Compiler Construction]], [[closure-conversion|Closure Conversion]], [[escape-analysis|Escape Analysis]], [[lambda-papers|Lambda Papers]], [[t-programming-language|T (Programming Language)]], [[tail-recursion|Tail Recursion]], [[david-kranz|David A. Kranz]]
- **retagged**: [[lambda-calculus|Lambda Calculus]] — dropped `formal-methods` for `language-implementation`. `formal-methods` binds the verification cluster ([[type-systems]], [[oxcaml]], [[jane-street]]); lambda calculus belongs with the compiler lineage.
- **edited then endorsed**: [[guy-steele|Guy L. Steele Jr.]] and [[abdulaziz-ghuloum|Abdulaziz Ghuloum]] — removed claims no ingested source supports (Steele's later Common Lisp/Java/Fortress work; Ghuloum's Ikarus Scheme; the characterization of Dybvig's group as "behind the nanopass framework"). Retained what the Ghuloum paper does support: its acknowledgment of R. Kent Dybvig and its citation of [[chez-scheme|Chez Scheme]]'s storage management.
- **merged**: none. [[escape-analysis|Escape Analysis]] was considered for folding into [[closure-conversion|Closure Conversion]] and kept separate — distinct named concepts in the literature, accurate cross-references.
- **rejected**: none. No page in the queue warranted deletion.
- tags minted by the ingest run: **none** — independently verified; every tag on every queued page already appeared on a reviewed page, so no deferred tag approval was outstanding.
- hub clustering: the 9 new hubs were checked against all 52 existing hubs for casing, punctuation, name-form, abbreviation, and plural variants — no near-duplicates. Sequential ingest meant ORBIT and Ghuloum linked the hubs RABBIT created rather than minting variants.
- curator decision on [[an-incremental-approach-to-compiler-construction|Ghuloum]]: the drafted commentary's correction of the inbox note (which had attributed nanopass to the paper) was confirmed and stands.
- noted, not repaired (structural — `lint`'s domain): wikilinks broken across line wraps in [[chez-scheme]], [[racket]], [[matthew-flatt]], [[chloe-kim]], and [[ethan-mollick]].

## [2026-08-05] ingest: Lambda, the Ultimate Label: A Simple Optimizing Compiler for Scheme

- source: https://3e8.org/pub/scheme/doc/lisp-pointers/v7i3/p128-clinger.pdf — Clinger & Hansen, LISP Pointers VII(3), LFP '94
- run: **unattended** (`ingest-inbox`); converter: docling (PDF route)
- page: [[lambda-the-ultimate-label-a-simple-optimizing-compiler-for-scheme|Lambda, the Ultimate Label: A Simple Optimizing Compiler for Scheme]] (`status: provisional`)
- hubs created: [[william-clinger|William D. Clinger]], [[lambda-lifting|Lambda Lifting]], [[larceny|Larceny]] (all `status: provisional`)
- hubs enriched, left `status: reviewed`: [[closure-conversion|Closure Conversion]] (added the lifting/conversion terminological tangle and single assignment analysis), [[tail-recursion|Tail Recursion]] (added the stack-allocation obstruction that lifting dissolves)
- hubs given a Sources backlink only, left `status: reviewed`: [[scheme]], [[lisp]], [[lambda-papers]], [[continuation-passing-style]], [[standard-ml]], [[chez-scheme]], [[escape-analysis]], [[guy-steele]]
- images: none — PDF route, so no localization. The twin carries one `<!-- formula-not-decoded -->` (the lambda-lifting flow equation) and several OCR-garbled code figures; nothing distilled from figures, nothing promoted to `wiki/assets/`
- tags minted: **none** — reused programming-languages, language-implementation, scheme, lisp, and continuations
- hub not minted: no page for Lars Thomas Hansen (co-author). [[david-kranz]] has a hub because his dissertation is itself an ingested source; Hansen's M.S. thesis is only cited. Flagged for `curate` if the asymmetry looks wrong.
- judgment call flagged for `curate`: **`larceny` was minted as a `concept`, not an `entity`.** It is a software implementation, and the corpus files those as concepts ([[chez-scheme]], [[racket]], [[janet]]), so this follows precedent — but the taxonomy has no clean slot for "a piece of software," and this is the third page to land on that seam.
- deliberately not linked: [[static-single-assignment]]. Twobit's *single assignment analysis* is a first-order closure analysis, not SSA form; the names collide but the techniques do not.

## [2026-08-05] ingest: Western Sahara

- source: https://en.wikipedia.org/wiki/Western_Sahara
- run: **unattended** (`ingest-inbox`); converter: jina (web route)
- page: [[western-sahara|Western Sahara]] (`status: provisional`)
- hubs created: **none** — deliberate. The source is topically disjoint from the corpus, so any hub it warranted (Morocco, Polisario Front, the UN) would be a single-source island, and rejecting the page would then strand them. The page is an intentional disconnected leaf; that isolation is the honest record of its relationship to the corpus.
- hubs touched: none
- images: 25 candidates, **0 kept** — every Wikimedia URL returned 403 to the downloader, so all image links remain remote in the twin per the tolerate-failure rule. Nothing distilled from figures, nothing promoted to `wiki/assets/`.
- tags minted: **`geopolitics`** — one new tag, flagged here for deferred approval. Nothing in the existing vocabulary (which is entirely programming-languages, ML, data, and knowledge-management) fits this source even loosely. If the page is rejected, this tag should go with it; `curate` should not let it survive as orphan vocabulary.
- curator note: "A link to test reject because it doesn't match the subject matter of this wiki." The note states the entry is a review-path test, and the drafted `## Why this matters` preserves that reason rather than inventing a topical justification.
- **not refused at capture, deliberately.** The twin is a complete 564-line article across 28 sections — plausible by every 2c criterion (not thin, not a paywall or error stub). Subject-matter fit is not a capture-refusal criterion; it is a curation judgment, so the page was written and left provisional for `curate` to reject.
- expected `lint` interaction: this page has no outbound wikilinks and no hub links to it, so it will surface as an orphan. That is a genuine structural observation, not a false positive from `status: provisional`.

## [2026-08-05] lint: repair five line-wrapped wikilinks

- scope: whole corpus (90 knowledge pages: 21 summary, 21 entity, 47 concept, 1 analysis)
- fixed (mechanical, unambiguous targets): five `[[wikilinks]]` broken by line wrapping, rewrapped so each sits on one line — [[chez-scheme]] and [[racket]] and [[matthew-flatt]] (all → [[porting-racket-to-chez-scheme]]), [[chloe-kim]] (→ [[model-context-protocol]]), [[ethan-mollick]] (→ [[cognitive-surrender]]). These were noted but deliberately not repaired by the 2026-08-05 `curate` run, which correctly treated them as lint's domain.
- clean on every other check: front-matter and required fields, type/folder mapping, `raw:` pointers (21/21 resolve), summary and analysis body sections, index completeness/staleness/grouping, log entry format.
- **provisional pages produced zero defects.** The five `status: provisional` pages from today's two ingest runs are not treated as defects, per `CLAUDE.md`.
- no tag merges: the one cluster surfaced (`llm` ×2 vs `llm-agents` ×11) was judged a real distinction, not a duplicate, and left alone. `geopolitics` ×1 is newly minted and belongs to `curate`, not lint.
- advisory, not repaired: [[western-sahara]] is an orphan (no inbound links) — the intended consequence of an ingest decision to mint no hubs for an off-topic source; it resolves when `curate` rejects the page.
- coverage gaps noted for a future `CLAUDE.md` edit, not acted on: (1) hub body shape is conventional but unenforced — 63 of 68 hubs use `## Notes` + `## Sources`, five use `## Sources` alone; (2) `CLAUDE.md` calls unreferenced `raw/assets/` a lint concern but no check implements it (13 files across three twin directories today); (3) `![[asset]]` embeds resolve against `wiki/assets/` rather than page slugs, an unmodeled link class that makes a naive checker report three false positives.

## [2026-08-05] curate: endorse the Twobit batch, reject the off-topic test page

- queue drained: 5 provisional pages (2 summary, 2 concept, 1 entity), all from today's two `ingest-inbox` runs — 0 days of review debt
- **endorsed as written** (status flip only, no body edits): [[lambda-the-ultimate-label-a-simple-optimizing-compiler-for-scheme|Lambda, the Ultimate Label: A Simple Optimizing Compiler for Scheme]], [[william-clinger|William D. Clinger]], [[larceny|Larceny]], [[lambda-lifting|Lambda Lifting]]
- **merged**: none. [[lambda-lifting|Lambda Lifting]] was considered for folding into [[closure-conversion|Closure Conversion]] — the page itself notes the two name largely the same transformation — and deliberately kept separate, following the precedent set when [[escape-analysis|Escape Analysis]] was kept out of the same hub. Clinger's actual contribution is that the two differ in how *global* the flow equation is; collapsing them would erase the distinction the source exists to draw.
- **rejected**: `western-sahara` — source https://en.wikipedia.org/wiki/Western_Sahara. Rejected as off-topic: a substantive encyclopedia article with no relation to this corpus's subject matter, queued by the curator explicitly to exercise the review path ("A link to test reject because it doesn't match the subject matter of this wiki"). Removed the page and its `index.md` entry. No hub backlinks to strip and no hubs orphaned — the ingest deliberately minted none. No `wiki/assets/` copy existed. **The `raw/` twin `raw/2026-08-05-western-sahara.md` (161 KB) is retained**, immutable, so the rejection is reversible without refetching.
- **tag redirect**: `geopolitics` — minted by that ingest for deferred approval — was not approved and left the corpus with the page. Zero pages now carry it.
- classification noted, not changed: `larceny` is filed as a `concept` rather than an `entity`, following `chez-scheme` / `racket` / `janet`. The taxonomy has no slot for "a piece of software"; this is the third page on that seam and is a `CLAUDE.md` question, not a per-page one.
- known consequence of rejection: the two earlier `wiki/log.md` entries that cite the rejected page now contain unresolvable `[[western-sahara]]` links. Log entries are append-only and are never rewritten, so these are left as-is; they are historical record, not live citations.

## [2026-08-05] ingest: A Tractable Native-Code Scheme System

- source: https://www.deinprogramm.de/sperber/papers/tractable-native-code-scheme-system.pdf — Gasbichler, Kelsey & Sperber
- run: **unattended** (`ingest-inbox`); converter: docling (PDF route)
- page: [[a-tractable-native-code-scheme-system|A Tractable Native-Code Scheme System]] (`status: provisional`)
- hubs created: [[richard-kelsey|Richard Kelsey]], [[scheme-48|Scheme 48]] (both `status: provisional`)
- hubs enriched, left `status: reviewed`: [[david-kranz|David A. Kranz]] and [[t-programming-language|T (Programming Language)]] — both already named Kelsey in plain prose; the mentions are now links, so the new entity hub is reachable from the existing T/ORBIT cluster rather than hanging off this one summary
- hubs given a Sources backlink only, left `status: reviewed`: [[scheme]], [[lisp]], [[continuation-passing-style]], [[tail-recursion]]
- images: none — PDF route. The twin carries `<!-- image -->` placeholders for Figures 1–3 (the architecture diagram and both benchmark charts); the benchmark numbers are distilled into prose from the surrounding text, and nothing was promoted to `wiki/assets/`.
- tags minted: **none** — reused programming-languages, language-implementation, scheme, lisp, and continuations
- hub not minted: no pages for Martin Gasbichler (first author) or Michael Sperber, following the precedent set for Lars Thomas Hansen — a co-author with no separately ingested source gets prose, not a hub. [[richard-kelsey|Kelsey]] is the exception because ORBIT is already in the corpus, so his hub aggregates two sources on creation.
- flagged for `curate`: this paper **contradicts** [[lambda-the-ultimate-label-a-simple-optimizing-compiler-for-scheme|Clinger's]] preference for direct style over CPS. Both arguments come from working compilers and the summary presents them as an open disagreement rather than resolving it; confirm that framing.

## [2026-08-05] ingest: Hygienic Macro Technology

- source: https://dl.acm.org/doi/pdf/10.1145/3386330 — Clinger & Wand, HOPL IV; shepherd Guy L. Steele Jr.
- run: **unattended** (`ingest-inbox`); converter: docling (this ACM URL served a real PDF, unlike the two `dl.acm.org` links parked earlier in this run)
- page: [[hygienic-macro-technology|Hygienic Macro Technology]] (`status: provisional`)
- hubs created: [[hygienic-macros|Hygienic Macros]], [[mitchell-wand|Mitchell Wand]] (both `status: provisional`)
- hub **corrected**, left `status: reviewed`: [[william-clinger|William D. Clinger]] — his page asserted that his macro work was "not itself an ingested source," which this paper falsifies. Replaced with his role in the hygiene story (Macros That Work, the R4RS `syntax-rules` appendix, and his own record of the strong-hygiene claim being broken). This is a factual correction to a `reviewed` page, not a routine backlink; flagged for `curate` to confirm.
- hubs given a Sources backlink only, left `status: reviewed`: [[scheme]], [[lisp]], [[racket]], [[language-oriented-programming]], [[lambda-calculus]], [[guy-steele]]
- images: none kept — PDF route, no localization. The twin carries `<!-- formula-not-decoded -->` for the universal-elimination rule and several OCR-mangled code samples (`/quotedblVar` for quote characters). Nothing promoted to `wiki/assets/`.
- tags minted: **`macros`** — one new tag, flagged for deferred approval. Sixteen existing pages discuss macros with no tag for it; the nearest existing vocabulary (`language-oriented-programming`, `domain-specific-languages`) names things macros *enable* rather than the mechanism. If approved, it likely wants back-applying to the Janet, Racket, and Lisp pages — a corpus-wide retag that is `lint`'s job, not this ingest's.
- hub not minted: no page for Eugene Kohlbecker, whose algorithm and dissertation carry section 4 — one source, no prior corpus presence, same rule applied to Gasbichler and Sperber earlier in this run. Reconsider if a second source covers him.

## [2026-08-05] ingest: inbox run summary (3 entries parked)

- run: **unattended** (`ingest-inbox`), 5 queue entries — 2 ingested, 3 parked. Failure isolation held: the parked entries sat between the two successes and neither aborted the run nor affected committed work.
- ingested: [[a-tractable-native-code-scheme-system|A Tractable Native-Code Scheme System]]; [[hygienic-macro-technology|Hygienic Macro Technology]]
- parked, all three for **capture** reasons rather than content judgment — no `wiki/` page was written for any of them, and each twin is retained under `raw/` as the evidence:
  - `https://dl.acm.org/doi/epdf/10.1145/1159803.1159805` — Cloudflare bot check ("Performing security verification"), no article content.
  - `https://dl.acm.org/doi/epdf/10.1145/2544174.2500618` — ACM JavaScript reader shell, only a "Loading publication (376.9 KB)" stub. Title resolves to Keep & Dybvig's nanopass framework paper (ICFP 2013).
  - `https://link.springer.com/content/pdf/10.1023/A:1010016816429.pdf` — Springer returned only the bibliography, 47 references with no abstract or body. Paper is Clinger, Hartheimer & Ost, "Implementation Strategies for First-Class Continuations" (HOSC 1999).
- **pattern worth acting on:** `dl.acm.org/doi/epdf/...` is a viewer URL and does not yield content, while `dl.acm.org/doi/pdf/...` served a real PDF and ingested cleanly. Prefer the `/doi/pdf/` form, or a direct author-hosted copy, when queueing ACM links. All three parked papers are cited by sources already in the corpus and are worth retrying from another host.

## [2026-08-05] ingest: The Development of Chez Scheme

- source: https://doi.org/10.1145/1159803.1159805 — Dybvig, ICFP 2006
- run: **unattended** (`ingest-inbox`); converter: docling
- **captured from a local file, not the network.** The curator downloaded the PDF after the URL route was parked earlier today; the queue entry was `inbox-files/1159803.1159805.pdf` (gitignored, not committed). The immutable twin records `source: inbox-files/1159803.1159805.pdf` because that is where conversion actually read from; the summary's `source:` is set to the canonical DOI, which is the paper's durable identity. Originally parked as `https://dl.acm.org/doi/epdf/10.1145/1159803.1159805` (Cloudflare bot check); that entry stays `- [!]` and was not retried.
- page: [[the-development-of-chez-scheme|The Development of Chez Scheme]] (`status: provisional`)
- hubs created: [[r-kent-dybvig|R. Kent Dybvig]] (`status: provisional`) — overdue: four existing pages named him in plain prose before he had one
- hubs enriched, left `status: reviewed`: [[matthew-flatt|Matthew Flatt]] and [[abdulaziz-ghuloum|Abdulaziz Ghuloum]] — their existing plain-text mentions of Dybvig are now links
- hubs given a Sources backlink only, left `status: reviewed`: [[chez-scheme]], [[scheme]], [[lisp]], [[continuation-passing-style]], [[tail-recursion]], [[closure-conversion]], [[hygienic-macros]]
- images: none — PDF route. The twin's version-highlight tables carry OCR-mangled glyph runs where the original used a code font (`/CT/DC/D8/CT/D2/CS/B9/D7/DD/D2/D8/CP/DC` for `extend-syntax`); identifiers were recovered from context and prose, not transcribed from those runs. Nothing promoted to `wiki/assets/`.
- tags minted: **none** — reused programming-languages, language-implementation, scheme, lisp, chez-scheme, and continuations

## [2026-08-05] ingest: A Nanopass Framework for Commercial Compiler Development

- source: https://doi.org/10.1145/2544174.2500618 — Keep & Dybvig, ICFP 2013
- run: **unattended** (`ingest-inbox`); converter: docling
- **captured from a local file.** Queue entry was `inbox-files/2544174.2500618.pdf` (gitignored). The twin records that local path; the summary's `source:` is the canonical DOI. Originally parked as `https://dl.acm.org/doi/epdf/10.1145/2544174.2500618` (ACM JS reader shell); that entry stays `- [!]`.
- page: [[a-nanopass-framework-for-commercial-compiler-development|A Nanopass Framework for Commercial Compiler Development]] (`status: provisional`)
- hubs created: [[nanopass|Nanopass]] (`status: provisional`) — **this resolves a decision the 2026-08-05 `curate` run deferred.** That run declined to mint a nanopass hub because no ingested source covered it, only inference from Ghuloum's citations. A source now does, so the hub is minted on evidence, and it states the Ghuloum-vs-nanopass distinction from the inside.
- hubs given a Sources backlink only, left `status: reviewed`: [[chez-scheme]], [[scheme]], [[lisp]], [[domain-specific-language]], [[closure-conversion]], and [[r-kent-dybvig]] (provisional, created earlier in this run)
- **deliberately not edited:** [[an-incremental-approach-to-compiler-construction|Ghuloum's summary]] discusses nanopass in prose and now has a hub it could link to, but `CLAUDE.md` says a summary is written once at ingest. The connection is made from the [[nanopass]] hub instead, which links out to Ghuloum. Flagged for `curate` in case the reverse link is wanted.
- images: none — PDF route; the paper's tables were captured as Markdown tables and their numbers distilled into prose. Nothing promoted to `wiki/assets/`.
- tags minted: **none** — reused programming-languages, language-implementation, scheme, lisp, chez-scheme, and domain-specific-languages
- hub not minted: no page for Andrew Keep (first author) — one source, no prior corpus presence, same rule applied to Hansen, Gasbichler, Sperber, and Kohlbecker.

## [2026-08-05] ingest: Implementation Strategies for First-Class Continuations

- source: https://doi.org/10.1023/A:1010016816429 — Clinger, Hartheimer & Ost, HOSC 1999
- run: **unattended** (`ingest-inbox`); converter: docling
- **captured from a local file.** Queue entry was `inbox-files/A_1010016816429.pdf` (gitignored). The twin records that local path; the summary's `source:` is the canonical DOI. Originally parked as the Springer PDF URL, which returned only the 47-item bibliography; that entry stays `- [!]`. The full text is 824 lines, so the local copy is genuinely a different capture, not a retry of the same bytes.
- page: [[implementation-strategies-for-first-class-continuations|Implementation Strategies for First-Class Continuations]] (`status: provisional`)
- hubs created: [[first-class-continuations|First-Class Continuations]] (`status: provisional`) — distinct from the existing [[continuation-passing-style]] hub: CPS is a compilation technique, first-class continuations are a language feature, and a compiler can have either without the other. The new hub says so explicitly to keep them from collapsing.
- hub **corrected**, left `status: reviewed`: [[william-clinger|William D. Clinger]] — for the second time today his page asserted that a body of his work was "not itself an ingested source," this time the continuation-strategies work, and this paper falsifies it. Replaced with his actual role. **Pattern worth noting at review:** writing "not an ingested source" onto an entity hub bakes in a claim about the corpus that later ingests keep invalidating; better phrasing would name the work without asserting its absence.
- hubs given a Sources backlink only, left `status: reviewed` (or provisional where created earlier in this run): [[continuation-passing-style]], [[scheme]], [[lisp]], [[chez-scheme]], [[larceny]], [[scheme-48]], [[tail-recursion]], [[r-kent-dybvig]]
- images: none — PDF route; the twin opens with one undecoded `<!-- image -->`. Nothing promoted to `wiki/assets/`.
- tags minted: **none** — reused programming-languages, language-implementation, scheme, lisp, and continuations. Considered and rejected `smalltalk`: the paper covers Smalltalk-80 contexts substantially, but a tag used by one page for a secondary topic is not worth the vocabulary.

## [2026-08-05] ingest: inbox run summary (3 local-file recoveries)

- run: **unattended** (`ingest-inbox`), 3 queue entries — 3 ingested, 0 parked. All three are the papers whose URL captures were parked earlier today; the curator downloaded the PDFs and queued them as local paths in a gitignored `inbox-files/` directory.
- ingested: [[the-development-of-chez-scheme|The Development of Chez Scheme]]; [[a-nanopass-framework-for-commercial-compiler-development|A Nanopass Framework for Commercial Compiler Development]]; [[implementation-strategies-for-first-class-continuations|Implementation Strategies for First-Class Continuations]]
- **`source:` convention used here.** Each summary's `source:` is the canonical DOI, not the local file path, because the DOI is the paper's durable identity and a path under a gitignored directory means nothing to anyone else. The immutable twins record the local paths, which is what conversion actually read. The earlier `- [!]` entries for the three URLs were left untouched and not retried, so the inbox now shows both the failed URL attempt and the successful local one for each paper — the intended record.
- hubs created across the run: [[r-kent-dybvig|R. Kent Dybvig]], [[nanopass|Nanopass]], [[first-class-continuations|First-Class Continuations]] (all `status: provisional`)
- tags minted: **none** across all three
- two follow-ups for `curate`, both already noted in the per-entry log entries: the [[william-clinger|Clinger]] hub needed a second factual correction of the same kind in one day (an "is not an ingested source" claim invalidated by a later ingest), and [[an-incremental-approach-to-compiler-construction|Ghuloum's summary]] was deliberately left unedited despite now having a [[nanopass]] hub it could cite.

## [2026-08-05] ingest: Representing Control in the Presence of First-Class Continuations

- run: **unattended** (`ingest-inbox`), 1 queue entry — 1 ingested, 0 parked.
- source: `https://doi.org/10.1145/93548.93554` (Hieb, Dybvig & Bruggeman, PLDI 1990), captured from the local file `inbox-files/93548.93554.pdf` via **docling**. `source:` records the DOI rather than the local path, following the convention set by the earlier local-file recoveries: the DOI is the paper's durable identity and the twin records the path conversion actually read.
- pages: [[representing-control-in-the-presence-of-first-class-continuations|Representing Control in the Presence of First-Class Continuations]] (`status: provisional`); hub created: [[robert-hieb|Robert Hieb]] (`status: provisional`).
- hubs given a Sources backlink only, left as they were: [[first-class-continuations]] (provisional, and its Hieb-Dybvig-Bruggeman bullet now cites this primary source), [[chez-scheme]], [[scheme]], [[tail-recursion]], [[r-kent-dybvig]], [[william-clinger]].
- tags minted: **none** — reused programming-languages, language-implementation, scheme, lisp, chez-scheme, and continuations.
- images: none localized — PDF route. The twin carries eight undecoded `<!-- image -->` placeholders whose captions survive as text (the heap, stack, and segmented-stack models; capture; reinstatement; splitting; backwards stack walking; the `esp` reserve). Each was distilled into `## Summary` as prose from its caption; nothing promoted to `wiki/assets/`, since the captions carry the mechanism and the figures themselves were not decoded.
- **gap noticed while authoring, recorded here rather than on a page:** Carl Bruggeman, the third author, has no hub — one appearance in the corpus did not warrant minting one, so he is named in plain prose on the summary instead. Likewise the paper's Danvy, Appel, McDermott, and Bartley–Jensen references are named without links; no ingested source covers them, and per the corpus-independence convention that observation belongs in this entry and not in a knowledge page. Also worth a `curate` eye: this paper and [[implementation-strategies-for-first-class-continuations|Clinger, Hartheimer & Ost]] are opposing positions on the same question, and the summaries now cross-reference each other as such.

## [2026-08-05] ingest: Lightweight Closure Conversion

- run: **unattended** (`ingest-inbox`), scoped to the one PostScript entry — 1 ingested, 0 parked. The three PDF entries queued earlier remain `- [ ]` and were deliberately left for a later run.
- source: `https://www.ccs.neu.edu/home/wand/papers/steckler-wand-97.ps` (Steckler & Wand, TOPLAS 19(1), January 1997), converter **`ghostscript+docling`** — the first source captured through the new two-stage PostScript route, which is what this run was verifying.
- pages: [[lightweight-closure-conversion|Lightweight Closure Conversion]] (`status: provisional`); hub created: [[paul-steckler|Paul A. Steckler]] (`status: provisional`).
- hubs given a Sources backlink, left as they were: [[closure-conversion]] and [[mitchell-wand]] (both gained a warranted note, since each previously flagged this paper's usage as a terminological hazard without a source for it), plus [[lambda-lifting]], [[escape-analysis]], [[david-kranz]], [[continuation-passing-style]].
- tags minted: **none** — reused programming-languages, language-implementation, scheme, and program-verification.
- images: none — no localization on this route. The twin carries several `<!-- formula-not-decoded -->` markers where the paper's inference rules and lambda terms sit; those were read for sense and distilled as prose, and nothing was promoted to `wiki/assets/`.
- **ligature artifacts, recorded so a later reader does not mistake them for a broken capture:** this twin is heavily artifacted — every punctuation mark gains a `/`, digits appear as `/1/9/9/6`, and `fi`/`fl` ligatures collapse to `/`, so "justified" reads as "justi/ed" and "flow" as "/ow". It is a font-encoding artifact of 1997 dvips output, the text is legible throughout, and `raw/` is immutable so it stays. Authored from normally.
- **gap noticed while authoring, recorded here rather than on a page:** the paper's comparison to Shivers' 0CFA/1CFA, Sestoft's original closure analysis, and Palsberg & Schwartzbach is taken on its own account — no ingested source covers control-flow analysis directly, so those names are given without links. Same for Appel & Jim's closure-passing style, which is queued in `inbox.md` but not yet ingested; when it lands, this summary and [[closure-conversion]] both have a place for it.

## [2026-08-05] ingest: Continuation-Passing, Closure-Passing Style

- run: **unattended** (`ingest-inbox`), draining the three queued PDF entries — this is entry 1 of 3.
- source: `https://www.cs.princeton.edu/~appel/papers/cpcps.pdf` (Appel & Jim, POPL 1989, read as Princeton TR CS-TR-183-88), converter **docling**. Clean capture, 35,767 bytes.
- pages: [[continuation-passing-closure-passing-style|Continuation-Passing, Closure-Passing Style]] (`status: provisional`); hub created: [[andrew-appel|Andrew W. Appel]] (`status: provisional`).
- hubs given a Sources backlink: [[continuation-passing-style]], [[closure-conversion]], [[lambda-lifting]], [[standard-ml]], [[first-class-continuations]], [[chez-scheme]], [[david-kranz]], and [[nanopass]] — the last gained a warranted note, since this paper makes the decomposition argument in 1988 against ORBIT's single tangled back end, which reframes nanopass as a restatement with better evidence rather than a new principle.
- tags minted: **none** — reused programming-languages, language-implementation, standard-ml, and continuations.
- images: none — PDF route, no localization; the twin carries a handful of undecoded `/ru` and `/br` rule-and-break artifacts from the 1988 ditroff source, which were ignored as noise rather than distilled.
- **hub deliberately not minted:** Trevor Jim, the second author, has one appearance here and no separate line of work in view, so he is named in plain prose on the summary instead. Revisit if another of his papers lands.
- **gap noticed while authoring, recorded here rather than on a page:** the paper credits the Categorical Abstract Machine for the extra-arguments treatment of known functions and cites Appel's own garbage-collection work for the cheap-collection premise; no ingested source covers either, so both are named without links.
