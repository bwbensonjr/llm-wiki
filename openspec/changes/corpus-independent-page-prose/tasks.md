## 1. State the convention

- [x] 1.1 Add a **corpus independence** passage to `CLAUDE.md`, in the page-taxonomy /
      front-matter area where the other page-content conventions live. State the
      falsifiability-by-ingest test as a single question the author can apply ("would
      ingesting another source make this false?"), name the two banned classes
      (presence/absence, corpus-scoped superlatives and counts), and state the repair
      shape (say what is true of the subject; drop the claim about the corpus).
- [x] 1.2 In the same passage, state the two preserved cases explicitly, each with a
      worked example: sibling orientation (stable under growth) and superlatives scoped
      to a source rather than the corpus. Over-application is a violation, so the
      permitted cases must be as concrete as the banned ones.
- [x] 1.3 State the `wiki/log.md` exemption in the same passage, cross-referencing the
      existing append-only wikilink convention, which already establishes that log
      entries record what was true when written.

## 2. Bind the authoring paths

- [x] 2.1 Update `.claude/skills/ingest-inbox/SKILL.md` step 2d (authoring) and 2f
      (drafting `## Why this matters`) to reference the convention and apply it at the
      point of writing, since this path has no reviewer.
- [x] 2.2 Add to `.claude/skills/ingest-inbox/SKILL.md` step 2g the rule that a noticed
      corpus gap — a work that cannot be linked, a hub deliberately not minted — is
      recorded in the `wiki/log.md` entry and never in a knowledge page. Confirm the
      existing log-entry requirements already accommodate this.
- [x] 2.3 Update `.claude/skills/file/SKILL.md` to apply the same constraint on the
      interactive path, so a page's conformance does not depend on which path wrote it.

## 3. Give curate standing to correct

- [x] 3.1 Update `.claude/skills/curate/SKILL.md` to list a corpus-membership claim as
      something correctable under edit-then-endorse.
- [x] 3.2 Document in that skill that such a correction may be applied to a page already
      carrying `status: reviewed`, that the page stays `reviewed`, and why this is a
      deliberate exception — the claim was true when endorsed and became false later.
- [x] 3.3 Document the narrow summary exception: correcting one of these claims in a
      `summary` is permitted despite write-once, and extends only to the offending
      clause, never to the distillation.

## 4. Remediate the existing corpus

- [x] 4.1 Fix the two presence/absence claims:
      `wiki/entities/william-clinger.md` ("neither of which is itself an ingested
      source") and
      `wiki/summaries/a-nanopass-framework-for-commercial-compiler-development.md`
      ("no ingested source covered it").
- [x] 4.2 Re-survey the corpus for corpus-scoped superlatives and counts rather than
      working from a stale list — the phrasings vary and the earlier grep was
      indicative, not exhaustive. Known sites include `wiki/concepts/nanopass.md`
      ("the corpus's evidence"), `wiki/concepts/closure-conversion.md` ("the corpus's
      clearest source"),
      `wiki/summaries/lambda-the-ultimate-label-a-simple-optimizing-compiler-for-scheme.md`
      ("the corpus's most explicit statement"),
      `wiki/summaries/a-nanopass-framework-for-commercial-compiler-development.md`
      ("the corpus's only measurement"), and `wiki/entities/r-kent-dybvig.md`
      ("several pages here mentioned him").
- [x] 4.3 Fix each site found, reading it first to confirm the claim is scoped to the
      corpus and not to a source — a source-scoped superlative is conformant and must be
      left alone. Scope each edit to the offending clause.
- [x] 4.4 Confirm no sibling-orientation sentence was removed by the sweep; spot-check
      `wiki/concepts/chez-scheme.md` and `wiki/concepts/scheme-48.md`, whose "sits
      alongside" phrasing is the case the change exists to protect.

## 5. Verification

- [x] 5.1 Re-run the falsifiability test by hand against every page touched in section
      4: for each remaining corpus reference, confirm no plausible future ingest
      falsifies it.
- [x] 5.2 Run `lint` and confirm no structural regression from the prose sweep — no
      broken or line-split wikilinks introduced, sections intact.
- [x] 5.3 Confirm `wiki/log.md` was not edited by the sweep, and that its existing
      "no ingested source covered it" entry is intact.
- [x] 5.4 Exercise the rule on a real ingest: run `ingest-inbox` on at least one source
      and confirm the drafted page carries no corpus-membership claim, and that any gap
      noticed during authoring appears in the log entry instead.
- [x] 5.5 Reread `CLAUDE.md` end to end for statements the new passage contradicts,
      since it is binding on every operation that reads or writes wiki content.
- [x] 5.6 Build the site and confirm the remediated pages render unchanged apart from
      the edited prose.
