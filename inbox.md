# Inbox

The queue of sources awaiting unattended ingest. Append links here from anywhere;
the `ingest-inbox` command drains it, checks off what it filed, and parks what it
could not.

This file is **committed mutable working state**, not a knowledge page. It lives
at the repo root deliberately: outside `wiki/`, so the site build does not publish
it and `lint` does not read it as an untyped page.

## Line format

Each entry is one Markdown checklist line: a checkbox, a URL or local path, and
an optional separator (` — ` or ` - `) followed by a free-text curator note.

| Checkbox | Meaning |
|----------|---------|
| `- [ ]`  | unprocessed — the next run will ingest it |
| `- [x]`  | ingested (or skipped as already ingested) — not retried |
| `- [!]`  | parked after a failure, annotated with the date and reason — not retried |

The note, when present, is the curator's reason for saving the link. It seeds the
drafted `## Why this matters` on the resulting summary page, so a provisional
page's significance is anchored to why the link was actually saved rather than
purely machine-inferred. It costs nothing to leave off.

Entries are never deleted — the checkbox carries the state, so the file stays a
legible, diffable record of what was queued. Re-running against a drained inbox
is a no-op.

```markdown
- [ ] https://example.com/paper.pdf — worth it for the CPS angle
- [ ] https://example.com/post
- [x] https://example.com/already-ingested
- [!] https://example.com/broken — 2026-08-05: docling failed, unparseable PDF
```

## Queue

<!-- Append new sources below as `- [ ] <url-or-path> — <optional note>`. -->
- [x] https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html - Seminal Scheme compiler paper by co-inventor of Scheme
- [x] https://www.ccs.neu.edu/home/shivers/cs6983/papers/kranz-diss-tr632.pdf - Motivation and details of closure analysis and CPS transformation
- [x] http://scheme2006.cs.uchicago.edu/11-ghuloum.pdf - Introduces the nanopass idea of incremental compiler transformations
- [!] http://foo.bar.baz/bad-link - Introduced for testing bad link handling — 2026-08-05: capture failed, DNS could not resolve host foo.bar.baz
- [x] https://3e8.org/pub/scheme/doc/lisp-pointers/v7i3/p128-clinger.pdf - Describes an approach to code transformation and lambda lifting
- [x] https://en.wikipedia.org/wiki/Western_Sahara - A link to test reject because it doesn't match the subject matter of this wiki 
- [x] https://www.deinprogramm.de/sperber/papers/tractable-native-code-scheme-system.pdf - Looks at going from virtual machine to native code
- [!] https://dl.acm.org/doi/epdf/10.1145/1159803.1159805 - An in-depth history of an important Scheme compiler — 2026-08-05: Cloudflare bot check, no article content (twin: raw/2026-08-05-just-a-moment.md)
- [!] https://dl.acm.org/doi/epdf/10.1145/2544174.2500618 - A particular framework for multi-pass compilers — 2026-08-05: ACM JS reader shell, only a loading stub, no article content. Title resolves to Keep & Dybvig, "A nanopass framework for commercial compiler development" (ICFP 2013); retry via a direct PDF host.
- [!] https://link.springer.com/content/pdf/10.1023/A:1010016816429.pdf - Compilation approaches for Scheme continuations — 2026-08-05: Springer served only the bibliography (47 references, no abstract or body). Paper is Clinger, Hartheimer & Ost, "Implementation Strategies for First-Class Continuations" (HOSC 1999); retry via a direct PDF host.
- [x] https://dl.acm.org/doi/pdf/10.1145/3386330 - A broad overview of hygenic macro technologies like those available in Scheme
- [x] inbox-files/1159803.1159805.pdf - Local version of failed to download Chez Scheme paper - An in-depth history of an important Scheme compiler
- [x] inbox-files/2544174.2500618.pdf - Local version of failed to download nanopass paper - A particular framework for multi-pass compilers
- [x] inbox-files/A_1010016816429.pdf - Local version of failed to download continuation paper - Compilation approaches for Scheme continuations
- [x] inbox-files/93548.93554.pdf - Representing control in the presence of first class continuations 
- [x] https://www.cs.princeton.edu/~appel/papers/cpcps.pdf - SML/NJ's own account of closure-passing style; the design Twobit contrasts its local lambda lifting against
- [x] https://andykeep.com/pubs/scheme-12a.pdf - The flat-closure optimization mechanism the nanopass paper alludes to but doesn't describe
- [x] https://www.cs.princeton.edu/~appel/papers/safe-closure.pdf - The safe-for-space closure conversion rule, proved
- [x] https://www.ccs.neu.edu/home/wand/papers/steckler-wand-97.ps - The third sense of "closure conversion" that the hub pages flag as a terminological hazard without describing
- [x] https://users.cs.utah.edu/plt/publications/macromod.pdf - Separating compile-time from run-time code so macro-using modules can be compiled separately; core source for why separate compilation is hard in Lisps with macros, and for how Emit Scheme might handle library phases
- [!] https://legacy.cs.indiana.edu/~dyb/pubs/implicit-phasing.pdf - 2026-10-31: could not reach source: DNS lookup for legacy.cs.indiana.edu failed (nodename nor servname provided); other hosts resolved in the same run, so likely a local network or sandbox restriction - retry by hand
- [!] https://legacy.cs.indiana.edu/~dyb/pubs/popl99.ps.gz - 2026-10-31: could not reach source: DNS lookup for legacy.cs.indiana.edu failed (nodename nor servname provided); other hosts resolved in the same run, so likely a local network or sandbox restriction - retry by hand
- [x] https://arxiv.org/pdf/2010.07516 - How eval and run-time redefinition block inlining, and Julia's world-age fix; the redefinition-versus-optimization tension behind separate compilation in dynamic languages
- [!] https://opendylan.org/books/drm/Sealing - 2026-10-31: implausible capture: chapter landing page holds only the DRM table of contents; the content is on subpages (Sealing_Overview, Explicitly_Known_Objects, Declaring_Characteristics_of_Classes, Declaring_Characteristics_of_Generic_Functions)
- [x] https://opendylan.org/books/drm/Define_Sealed_Domain - Partial sealing of generic functions across library boundaries; companion to the DRM sealing chapter for the separate-compilation analysis
- [x] https://lispworks.com/documentation/HyperSpec/Body/03_bbc.htm - What Common Lisp's compile-file may assume about definitions, redefinition, and calls when compiling a file; the standard's stance on separate compilation
- [x] https://cisco.github.io/ChezScheme/csug9.5/system.html - Chez's compile-whole-program and compile-whole-library: cross-library optimization, dead-code removal, and the libs-visible? trade-off with eval; a model for producing standalone executables
- [x] https://engineering.purdue.edu/~qobi/papers/fdlcc.pdf - Stalin's whole-program closure conversion: the performance a closed-world Scheme compiler gains by giving up separate compilation
- [x] https://docs.racket-lang.org/raco/exe.html - How Racket builds standalone executables by embedding modules in the runtime, and its limits around dynamically required modules
- [!] https://docs.racket-lang.org/rhombus/standalone.html - 2026-10-31: implausible capture: Jina received HTTP 403 and the twin is the Racket 'Page Not-Found' page (30 words); retry by hand or try https://docs.racket-lang.org/raco/demod.html
- [x] https://lispcookbook.github.io/cl-cookbook/scripting.html - Building Common Lisp executables by dumping an image with save-lisp-and-die; the image-based route to standalone executables
- [x] https://eprints-gro.gold.ac.uk/2336/1/sbcl.pdf - How a Common Lisp's build is entangled with its own image, and how SBCL bootstraps from other implementations; context for image-based delivery
- [!] https://mfleck.cs.illinois.edu/envision/scheme48/module/module.html - 2026-10-31: implausible capture: LaTeX2HTML front page only (title, abstract, table of contents, 235 words); the memo body is split across node1.html-node11.html - queue node6.html (Compiling and linking) and node10.html (Discussion), or find a single-file copy
- [x] inbox-files/1291151.1291197.pdf - Local version of failed to download Implicit Phasing paper - The opposing design to explicit phases: infer when imported bindings are needed at compile time vs run time; bears on separate compilation of macro-using libraries
- [x] inbox-files/292540.292559.pdf - Local version of failed to download Extending the Scope paper - Modules and lexically scoped macros with separate compilation, fully static; the Chez lineage of the library/macro separate-compilation problem
- [x] inbox-files/drm-sealing-chapter.md - Combined DRM Sealing chapter (Overview, Explicitly Known Objects, Declaring Characteristics of Classes and of Generic Functions), assembled locally because the chapter page (parked line 64) holds only a table of contents; sealing as a promise that lets a compiler treat classes and generic functions as closed across library boundaries, for the separate-compilation analysis
