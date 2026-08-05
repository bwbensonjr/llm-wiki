## Context

The wiki's two layers age differently. A `raw/` twin is immutable and a `wiki/` page is
written once and revised rarely, but the corpus around them grows continuously and
unattended. Any sentence whose truth depends on corpus membership is therefore written
against a moving target, and nothing catches it when it goes stale: the page still
parses, its front-matter is valid, and its wikilinks resolve.

The concrete trigger was `wiki/entities/william-clinger.md`. It was written stating that
his macro work was not an ingested source; hours later the HOPL macro paper landed and
the sentence was false. It was corrected, and the replacement said his
continuation-strategies work was not an ingested source; that paper landed in the next
run and the sentence was false again. Two instances of one sentence pattern, both
falsified within a day, on a page that had been curator-endorsed in between.

Surveying the corpus found the hard pattern is rare — two live occurrences — but a
softer form is widespread: roughly nineteen pages carry corpus-dependent superlatives
and counts ("the corpus's only measurement of that trade-off", "several pages here
mentioned him before he had a page of his own"). These fail identically, just less
visibly.

## Goals / Non-Goals

**Goals:**

- State a rule that makes a page's prose true independent of what else the corpus holds.
- Draw the boundary precisely enough that an unattended run can apply it without a
  reviewer, since that is the path that generates most prose.
- Preserve sibling orientation, which is stable under growth and is much of a hub's
  value.
- Give `curate` explicit standing to fix violations, including on `reviewed` pages.
- Remediate existing occurrences.

**Non-Goals:**

- A `lint` check. Distinguishing a banned claim from permitted orientation requires
  reading for meaning; a phrase matcher would fire on the sentences this change
  protects.
- Removing the wiki's voice. Pages may still compare, contrast, and cross-reference —
  the constraint is on claims about *corpus membership*, not on relating ideas.
- Touching `wiki/log.md`. Log entries are dated, append-only records of what was true at
  a moment; "no ingested source covered it" is *correct* there and must stay.
- Any change to `wiki_ingest/` or to `raw/`.

## Decisions

**1. The test is falsifiability-by-ingest, not a phrase blacklist.**

A sentence is disallowed when ingesting some plausible future source would make it
false. This gives the unattended path a decision procedure rather than a list to pattern
match, and it explains why the two classes are the same bug: "X is not in the corpus" and
"X is the corpus's only Y" both fail on the next ingest.

*Alternative considered:* enumerate banned phrasings ("not an ingested source", "the only",
"the first"). Rejected — it is simultaneously too narrow (novel phrasings slip through)
and too broad (it would flag "the only strategy in the paper that is zero-overhead",
which is a claim about the source, not the corpus).

**2. Sibling orientation is permitted, and the distinction is stability under growth.**

"Sits in this wiki's collection of Scheme implementations alongside libscheme and
Racket" survives any future ingest — a new sibling adds to the collection without
falsifying the sentence. "The corpus's only measurement of that trade-off" does not. The
rule is therefore not "avoid mentioning the wiki" but "do not assert something a later
ingest can overturn."

*Alternative considered:* ban all corpus self-reference. Rejected — it would strip hubs
of the orientation that justifies them, and the failure mode it prevents is already
covered by the stability test.

**3. Say what *is* true rather than what is absent.**

The repair for "his Scheme 311 compiler is not itself an ingested source" is to name the
work and stop. The absence claim adds nothing a reader wants: they can see which pages
exist. This makes remediation mechanical — delete the clause, keep the subject.

**4. The rule lives in `CLAUDE.md`; the skills reference it rather than restate it.**

`CLAUDE.md` is binding on every operation that reads or writes wiki content, so it is the
single place the rule can be stated once. The three skills get a pointer and the specific
obligation each has (author under it / correct under it), following the precedent set by
the `log.md` wikilink convention and the asset-embed rule.

**5. Remediating summaries is an authorized exception to write-once.**

`CLAUDE.md` says a summary is written once at ingest. Fixing corpus-dependent prose in an
existing summary contradicts that, so this change authorizes it explicitly and narrowly:
only to remove or rephrase a corpus-dependent claim, never to revise the distillation.

**6. Superlatives about the *source* stay.**

"The paper's only measurement of compile-time cost" is a claim about the paper and is
stable. Only superlatives scoped to the corpus are affected. Remediation must read each
site rather than rewriting by pattern.

## Risks / Trade-offs

- **The boundary is judgment, and the unattended path applies it unsupervised** → the
  stability test is stated as a one-sentence question ("would ingesting another source
  make this false?"), with worked examples of both permitted and banned sentences in
  `CLAUDE.md`, so the common cases need no deliberation.
- **Prose gets blander if the rule is over-applied** → the rule is explicitly paired with
  the preserved case, and the specs carry a scenario asserting that sibling orientation
  is *not* a violation, so over-application is itself a spec violation.
- **Remediating ~21 sites risks collateral edits** → the sweep is scoped to the offending
  clause; each edit removes or rephrases a claim about the corpus and changes nothing
  else. Summary edits are further limited by decision 5.
- **No automated enforcement, so drift can recur** → accepted. `curate` reviews every
  provisional page, which is where machine-drafted prose surfaces; a false-positive-prone
  `lint` check would cost more than the drift.
- **The two flagged pages are already `reviewed`** → `curate` gains explicit standing to
  edit a reviewed page for this, rather than the correction happening informally as it
  did twice today.

## Migration Plan

1. Land the `CLAUDE.md` convention and the three skill updates — this stops new
   violations at the source.
2. Fix the two hard presence/absence claims.
3. Sweep the ~19 superlative and count sites, reading each to confirm it is scoped to the
   corpus rather than to a source.
4. Re-run `lint` to confirm no structural regression from the sweep. No behavior change is
   expected, since only prose is touched.

Rollback is `git revert`; nothing here is stateful and no `raw/` content is involved.

## Open Questions

- Should `wiki/index.md` one-line descriptions be held to the same rule? They are
  bookkeeping rather than knowledge pages, and are rewritten on every ingest, so staleness
  self-corrects. Treated as out of scope unless review disagrees.
