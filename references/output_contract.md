# result.json

`result` carries:

- `mode` — `llm` when a candidate draft was supplied, else `minimal-edit`.
- `polished` — the deliverable text.
- `changes[]` — `{kind, from, to[, context]}` for every edit the engine made
  (`kind` ∈ `phrase`, `duplicate-word`, `spacing`).
- `alignment` — `{pairs[], sentences_in, sentences_out, paired, dropped, added, dropped_text[]}`;
  each pair carries its own `preservation` map.
- `preservation` — `{ok, missing{numbers, units, citations, negations, hedges}}`
  computed on the whole document.
- `edit_count`.

`status: success` requires every token class to be preserved and every sentence
anchor to re-slice. A merged sentence is reported, not penalised.
