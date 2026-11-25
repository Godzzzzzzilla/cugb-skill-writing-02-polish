---
name: academic-polish
description: Polish academic prose without moving its meaning — tightens wordy phrasing and spacing, then proves with a recomputable audit that every number, unit, citation, negation and hedge survived. Use when asked to edit, tighten or "improve the language" of a paper section, or to check someone else's polish.
---

# Academic polish with a preservation audit

Editing is where meaning quietly moves. A model asked to "polish" will happily
delete the `not`, round the p-value, or drop a hedge that the claim depends on.
This skill separates the two jobs: a small, closed edit engine does the
rewriting, and an audit compares tokens before and after. If a candidate draft
already exists, the skill **audits it and does not touch it**.

## One command

**Where to run it.** The scripts resolve their own paths, so they work from
any working directory. If your shell starts in `/app/work` (the contract's work
directory), call the absolute path of the script —
`python3 /skills/weekly-skill/scripts/run.py --input /input/case.json --output /app/output`
— or `cd` into the folder holding this `SKILL.md` first and use the relative form
below.

```bash
python3 scripts/run.py --input /input/case.json --output /app/output
python3 scripts/verify.py --result /app/output/result.json
```

## Mode is decided by the input

| input | mode | behaviour |
|---|---|---|
| one draft | `minimal-edit` | closed-list phrase edits + spacing; nothing that carries a claim is touched |
| draft + a second text | `llm` | the second text is audited against the draft; it is **not** rewritten |

## What it writes

`polished.md`, `changes.json` (every edit with before/after), `result.json`
(`mode`, `polished`, `changes`, `alignment`, `preservation`), `audit.json`,
`evidence.jsonl`, `report.md`.

## What is preserved, exactly

| class | rule |
|---|---|
| numbers | multiset must be identical; `23.4%`, `p = 0.03`, `n = 6` may not change |
| units | identical multiset (`°C`, `h`, `mg/L`, …) |
| citations | identical multiset of `[n]` and `(Author, year)` |
| negations | identical multiset — adding or removing a negation is a meaning change |
| hedges | identical multiset (`may`, `likely`, `suggest`, …) |

These are computed on the whole document, not by pairing sentences: a candidate
that merges two sentences is legitimate, and index pairing would report a
false failure. Sentence pairing is used only to show *where* a change landed,
and merged/dropped sentences are listed in `alignment.dropped_text`.

## Why minimal edit rather than a rewrite

A rewrite optimises prose and optimises away evidence. The closed list in
`PHRASES` only removes words that carry no claim ("in order to" → "to",
"due to the fact that" → "because"). Anything not on the list stays, and the
audit proves it.

## Failure handling

| situation | behaviour |
|---|---|
| candidate is empty | `partial`, reason recorded, nothing written as polished |
| candidate drops a number | `numbers-preserved` fails, the missing token is listed, status `partial` |
| draft is a table or code block | passed through verbatim, counted as verbatim in `alignment` |
| no text file at all | `cannot_determine` |

## Limits

- The edit engine is deliberately conservative: it will not restructure
  sentences, and it does not fix grammar beyond spacing and duplication.
- Hedges are matched from a fixed vocabulary; a synonym outside it is invisible
  to the audit.
- Multilingual text is handled by the same rules; the hedge list is
  English-heavy.
