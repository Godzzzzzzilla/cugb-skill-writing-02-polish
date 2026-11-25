#!/usr/bin/env python3
"""writing-02-polish — minimal-edit rewriting with a machine-recomputable audit.

    python scripts/run.py --input /input/case.json --output /app/output

Two modes, decided by the input, not by us:

  llm      a second file is present that looks like a polished draft.  We audit it
           against the original and change nothing.  Editing a model's draft is how
           meaning quietly moves.
  minimal  no second file.  A conservative rule engine edits the draft: spacing,
           duplicated words, a closed list of wordy phrases.  Anything that could
           shift meaning is left alone, and said so.

Either way the audit compares the two texts sentence by sentence and token by
token: numbers, units, citations, negations and hedges must survive.
"""
from __future__ import annotations

import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import armkit as ak  # noqa: E402

SKILL = "writing-02-polish"
VERSION = "1.0.0"

# closed list: phrase -> replacement.  Nothing here changes a claim.
PHRASES = {
    r"\bin order to\b": "to",
    r"\bdue to the fact that\b": "because",
    r"\bit is important to note that\b": "",
    r"\bit should be noted that\b": "",
    r"\bwe believe that\b": "we",
    r"\bwas found to be\b": "was",
    r"\bthe majority of\b": "most",
    r"\ba large number of\b": "many",
    r"\bin spite of the fact that\b": "although",
    r"\bat this point in time\b": "now",
    r"\bprior to\b": "before",
    r"\bsubsequent to\b": "after",
}
FILLERS = re.compile(r"\b(very|really|quite|rather|somewhat)\s+", re.I)


def split_units(text: str):
    """Paragraphs of (prefix, sentences) so headings and code survive untouched."""
    out = []
    for para in re.split(r"\n\s*\n", text):
        if not para.strip():
            out.append(("blank", []))
            continue
        if para.lstrip().startswith("#") or para.lstrip().startswith(("```", "|", "-", "*")):
            out.append(("verbatim", [para]))
            continue
        out.append(("prose", ak.sentence_split(para)))
    return out


def minimal_edit(text: str, log: list) -> str:
    def apply_phrases(s: str) -> str:
        for pat, rep in PHRASES.items():
            for m in re.finditer(pat, s, re.I):
                log.append({"kind": "phrase", "from": m.group(0), "to": rep,
                            "context": ak.clip(s[max(0, m.start() - 40):m.end() + 40], 120)})
            s = re.sub(pat, rep, s, flags=re.I)
        return s

    def dedupe_words(s: str) -> str:
        def repl(m):
            log.append({"kind": "duplicate-word", "from": m.group(0), "to": m.group(1)})
            return m.group(1)
        return re.sub(r"\b(\w+)(\s+\1)\b", repl, s, flags=re.I)

    def tidy(s: str) -> str:
        before = s
        s = re.sub(r"[ \t]{2,}", " ", s)
        s = re.sub(r"\s+([,.;:!?])", r"\1", s)
        s = re.sub(r"([,;:])(?=[^\s])", r"\1 ", s)
        s = re.sub(r"\(\s+", "(", s)
        s = re.sub(r"\s+\)", ")", s)
        if s != before:
            log.append({"kind": "spacing", "from": ak.clip(before, 80), "to": ak.clip(s, 80)})
        return s

    out_paras = []
    for kind, units in split_units(text):
        if kind == "verbatim":
            out_paras.append(units[0])
        elif kind == "blank":
            out_paras.append("")
        else:
            edited = []
            for s in units:
                e = tidy(dedupe_words(apply_phrases(s)))
                if not e:
                    continue
                if e[0].islower():
                    e = e[0].upper() + e[1:]
                edited.append(e)
            out_paras.append(" ".join(edited))
    return "\n\n".join(out_paras)


def audit_texts(original: str, candidate: str, audit: ak.Audit, res: ak.Result):
    """Document-level token preservation plus sentence pairing for the report.

    Index pairing is wrong as soon as a candidate merges two sentences, so the
    preservation checks run on the whole document's token multisets, and the
    sentence alignment is only used to show where a change happened.
    """
    import difflib

    orig_s = [s for k, us in split_units(original) if k == "prose" for s in us]
    cand_s = [s for k, us in split_units(candidate) if k == "prose" for s in us]

    # ---- global token preservation -------------------------------------
    tok_o, tok_c = ak.tokens_of(original), ak.tokens_of(candidate)
    missing = {k: ak._multiset_missing(sorted(tok_o[k]), sorted(tok_c[k])) for k in tok_o}
    for key, label, critical in (("numbers", "numbers-preserved", True),
                                 ("units", "units-preserved", True),
                                 ("citations", "citations-preserved", True),
                                 ("negations", "negations-preserved", True),
                                 ("hedges", "hedges-preserved", False)):
        ok = not missing[key]
        audit.check(label, ok, f"{len(tok_o[key])} in, {len(tok_c[key])} out"
                               + (f"; missing {missing[key][:6]}" if missing[key] else ""),
                    weight=1.0, critical=critical)

    # ---- sentence pairing ----------------------------------------------
    o_keys = [ak.norm_key(x)[:80] for x in orig_s]
    c_keys = [ak.norm_key(x)[:80] for x in cand_s]
    sm = difflib.SequenceMatcher(a=o_keys, b=c_keys, autojunk=False)
    pairs, dropped, added = [], [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                pairs.append((i1 + k, j1 + k))
        elif tag == "replace":
            span = min(i2 - i1, j2 - j1)
            for k in range(span):
                pairs.append((i1 + k, j1 + k))
            dropped.extend(range(i1 + span, i2))
            added.extend(range(j1 + span, j2))
        elif tag == "delete":
            dropped.extend(range(i1, i2))
        elif tag == "insert":
            added.extend(range(j1, j2))
    audit.check("sentences-paired", len(pairs) >= max(1, int(0.7 * len(orig_s))),
                f"{len(pairs)}/{len(orig_s)} source sentences paired, {len(dropped)} dropped, {len(added)} added",
                weight=0.8, critical=False)

    rows = []
    for oi, ci in pairs:
        a, b = orig_s[oi], cand_s[ci]
        pres = ak.preserved(a, b)
        rows.append({"pair": len(rows) + 1, "original_index": oi + 1, "candidate_index": ci + 1,
                     "original": ak.clip(a, 220), "candidate": ak.clip(b, 220),
                     "preservation": {k: {"ok": v["ok"], "missing": v["missing"][:6]} for k, v in pres.items()}})
    for oi in dropped:
        rows.append({"pair": len(rows) + 1, "original_index": oi + 1, "candidate_index": None,
                     "original": ak.clip(orig_s[oi], 220), "candidate": None,
                     "preservation": {"dropped": {"ok": False, "missing": []}}})
    counts = {"sentences_in": len(orig_s), "sentences_out": len(cand_s),
              "paired": len(pairs), "dropped": len(dropped), "added": len(added),
              "dropped_text": [ak.clip(orig_s[i], 160) for i in dropped]}
    return rows, missing, counts


def _merged(cand_s) -> bool:
    for s in cand_s:
        if len(ak.sentence_split(s)) > 3 and len(s) > 600:
            return True
    return False


def solve(case: ak.CaseInput, out: str, audit: ak.Audit, res: ak.Result) -> bool:
    docs = [p for p in case.discover() if p.lower().endswith((".md", ".txt"))]
    audit.check("input-found", bool(docs), f"{len(docs)} text file(s)", critical=True)
    if not docs:
        return False
    docs.sort(key=lambda p: 0 if re.search(r"draft|original|source|manuscript", os.path.basename(p), re.I) else 1)
    original, _ = ak.read_text(docs[0])
    polished_src = next((p for p in docs[1:] if p != docs[0]), None)
    mode = "llm" if polished_src else "minimal-edit"
    res.meta["mode"] = mode
    res.meta["source"] = os.path.basename(docs[0])
    if polished_src:
        res.meta["candidate"] = os.path.basename(polished_src)
    ak.write_text(os.path.join(out, "inputs", os.path.basename(docs[0])), original)
    res.add_artifact(f"inputs/{os.path.basename(docs[0])}", "data", "source draft, copied verbatim")
    if polished_src:
        cand_text, _ = ak.read_text(polished_src)
        ak.write_text(os.path.join(out, "inputs", os.path.basename(polished_src)), cand_text)
        changes = []
    else:
        changes = []
        cand_text = minimal_edit(original, changes)

    rows, worst, counts = audit_texts(original, cand_text, audit, res)
    audit.check("edited-or-audited", bool(cand_text.strip()), f"mode={mode}")

    ak.write_text(os.path.join(out, "polished.md"), cand_text)
    res.add_artifact("polished.md", "data", "the deliverable text")
    ak.write_json(os.path.join(out, "changes.json"), {"mode": mode, "changes": changes})

    for i, row in enumerate(rows, start=1):
        a = original.find(row["original"][:40]) if row["original"] else -1
        if a < 0:
            continue
        quote = original[a:a + min(80, len(row["original"]))]
        anchor = ak.Anchor(f"inputs/{os.path.basename(docs[0])}", a, a + len(quote), quote)
        ok, why = ak.verify_anchor(out, anchor.as_dict())
        res.add_evidence(f"s{i}", f"sentence {i}: {ak.clip(quote, 70)}", anchor, ok, why)

    verified = sum(1 for e in res.evidence if e["verified"])
    audit.check("anchors-verified", verified == len(res.evidence) and verified > 0,
                f"{verified}/{len(res.evidence)} sentence ranges re-slice", critical=True)

    res.set("mode", mode)
    res.set("polished", cand_text)
    res.set("changes", changes)
    res.set("alignment", {"pairs": rows, **counts})
    res.set("preservation", {
        "ok": not any(worst.values()) if isinstance(worst, dict) else not worst,
        "missing": worst if isinstance(worst, dict) else {},
    })
    res.set("edit_count", len(changes))
    if mode == "llm":
        res.limits.append("a candidate draft was present, so the text was audited and not rewritten")
    if isinstance(worst, dict):
        for cls, items in worst.items():
            if items:
                res.add_uncertainty(f"{cls} not preserved", f"missing: {items[:8]}",
                                    "restore the token, or record the change as deliberate")
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="/input/case.json")
    ap.add_argument("--output", default="/app/output")
    args = ap.parse_args()
    ak.safe_stdout()
    started = ak.utc_now()
    os.makedirs(args.output, exist_ok=True)
    case = ak.CaseInput.load(args.input, work_dir=args.output)
    audit, res = ak.Audit("writing-02"), ak.Result(args.output, SKILL, VERSION)
    try:
        ok = solve(case, args.output, audit, res)
    except Exception as exc:
        import traceback
        traceback.print_exc()
        ok = False
        audit.check("pipeline-completed", False, f"{type(exc).__name__}: {exc}", critical=True)
        res.add_uncertainty("pipeline exception", str(exc), "read audit.json before trusting the text")
    res.meta["case_notes"] = case.notes
    status = ak.derive_status(audit, ok)
    if not ok and status == "success":
        status = "partial"
    res.write(case, audit, status, {
        "success": "sentence pairs align and every number, unit, citation, negation and hedge survived",
        "partial": "a preservation check failed; see preservation.violations",
        "cannot_determine": "no draft could be read",
    }.get(status, status), started, sys.argv)
    a = audit.as_dict()
    print(f"wrote result.json status={status} checks={a['passed']}/{a['total']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
