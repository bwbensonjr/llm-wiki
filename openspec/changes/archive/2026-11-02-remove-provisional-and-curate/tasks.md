# Tasks

## 1. Conventions and docs

- [x] 1.1 Update `CLAUDE.md`: drop `status` from the opening paragraph, page taxonomy, and every front-matter block; make `## Why this matters` simply curator-supplied (interactive) or LLM-drafted from the inbox note (unattended); remove `curate` from the log `<op>` vocabulary (noting old entries keep it) and from the log-wikilink rationale; delete the "`lint` vs `curate`" section; make the corpus-independence correction a curator edit; remove deferred-approval and `curate` wording from Tags, inbox, Image handling, and Publishing (drop the "Provisional pages publish" follow-up). Verify: `grep -n -i "provisional\|curate\b\|status:" CLAUDE.md` returns only intended historical mentions.
- [x] 1.2 Update `README.md`: remove the provisional/review principle, the `/curate` bullet, the `curate` command entry, and provisional wording in the inbox section and `ingest-inbox` entry. Verify: `grep -n -i "provisional\|curate" README.md` is empty.
- [x] 1.3 Update `inbox.md` header prose to drop "provisional page". Verify by grep.
- [x] 1.4 Remove the `status:` line and status guidance from `templates/summary.md`, `entity.md`, `concept.md`, `analysis.md`. Verify: `grep -n status templates/` is empty.
- [x] 1.5 Update the Purpose paragraphs of `openspec/specs/unattended-ingestion/spec.md` (drops "`status: provisional` so a later `curate` run...") and `openspec/specs/resource-ingestion/spec.md` if needed. Verify by grep.

## 2. Skills

- [x] 2.1 Delete `.claude/skills/curate/`. Verify: directory absent and `curate` no longer listed among skills.
- [x] 2.2 Edit `.claude/skills/ingest-inbox/SKILL.md`: drop `status: provisional` from the description, front-matter instructions, hub rules ("leave reviewed hubs reviewed"), validation, and invariants; reword `curate` references (near-duplicate hubs, log readers) to refer to the curator or `lint`. Keep logging of minted tags, figure decisions, and noticed gaps. Verify: `grep -n -i "provisional\|curate\|status" .claude/skills/ingest-inbox/SKILL.md` returns nothing that instructs writing or checking `status`.
- [x] 2.3 Edit `.claude/skills/lint/SKILL.md` line about `log.md` link skipping so it cites manual renames/deletions instead of `curate`. Confirm `lint` does not require a `status` field. Verify by grep.

## 3. Content migration

- [x] 3.1 Strip the `status: provisional` / `status: reviewed` line from the front-matter of every page under `wiki/` (excluding `wiki/log.md` and `wiki/index.md` body text) with a script that touches only that line in the front-matter block. Verify: `grep -rln "^status:" wiki/` is empty and `git diff --stat` shows one deleted line per page (about 135 files).
- [x] 3.2 Confirm front-matter still parses as YAML for every page (a short `uv run python` check with a YAML parser) and that `wiki/log.md` is unchanged. Verify: script reports zero parse errors; `git diff wiki/log.md` is empty.
- [x] 3.3 Run `scripts/build-site.sh` and confirm the Quartz build succeeds. Verify: build exits 0.

## 4. Specs and verification

- [x] 4.1 Run `mise exec -- openspec validate remove-provisional-and-curate --strict`. Verify: reports valid.
- [x] 4.2 Repo-wide check: `grep -rn -i "provisional\|curate" --exclude-dir=raw --exclude-dir=openspec --exclude-dir=.quartz --exclude-dir=node_modules .` returns only `wiki/log.md` history and the nanopass summary's account of a past `curate` run.

## Workflow follow-up

- Archive with `/opsx:archive`; then delete `openspec/specs/corpus-curation/` if archive leaves it with no requirements, and stage synced specs explicitly.
- Commit and push to `main`.
