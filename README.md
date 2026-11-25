# writing-02-polish

Meaning-preserving academic editing with a recomputable audit. Submission for
**写作02｜学术语言润色** (product-arena-02).

## The idea

Separate rewriting from proof. A closed edit list does the rewriting; a token
audit does the proving. When a candidate draft is supplied, the skill only
audits — editing someone else's polish is how a `not` disappears.

## Measured on the bundled demo (candidate-draft mode)

| check | result |
|---|---|
| numbers | 7 in, 7 out |
| units | 1 in, 1 out |
| citations | 1 in, 1 out |
| negations | 8 in, 8 out |
| hedges | 3 in, 3 out |
| sentences paired | 6 of 7 (one deliberate merge, listed in `alignment.dropped_text`) |
| anchors re-slicing | 6 of 6 |
| audit | 9/9, `status: success` |

The candidate in `examples/input/polished_llm.md` was written to be plausible but
lossy; running the skill on it shows which tokens it kept.

## Files

```
SKILL.md              what an agent loads
scripts/run.py        edit engine + audit
scripts/verify.py     independent anchor verifier
scripts/selftest.py   12 checks
scripts/armkit.py     shared core (token classes, anchors, audit)
examples/case.json    demo input (draft + candidate)
references/           contract and limits
run/                  a real run
```

## Failure handling

| input | behaviour |
|---|---|
| candidate drops a token class | that check fails, missing tokens listed, `status: partial` |
| no candidate | `minimal-edit` mode, edits logged in `changes.json` |
| tables/code in the draft | passed through verbatim |
| no text file | `cannot_determine` with the reason |

## Reproduce

```bash
python3 scripts/run.py --input examples/case.json --output /tmp/out
python3 scripts/verify.py --result /tmp/out/result.json
python3 scripts/selftest.py
```
