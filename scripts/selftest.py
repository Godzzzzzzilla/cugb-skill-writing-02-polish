#!/usr/bin/env python3
"""Self-test for writing-02-polish."""
from __future__ import annotations
import json, os, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import armkit as ak
import run as skill
PASS = FAIL = 0
def check(n, c, d=""):
    global PASS, FAIL
    if c: PASS += 1; print(f"  ok {n}" + (f" — {d}" if d else ""))
    else: FAIL += 1; print(f"  FAIL {n}" + (f" — {d}" if d else ""))
def main():
    print("writing-02 selftest")
    check("armkit pinned", bool(ak.VERSION), ak.VERSION)
    log = []
    edited = skill.minimal_edit("In order to test this, we  ran two  runs.", log)
    check("wordy phrase removed", "in order to" not in edited.lower(), edited)
    check("double space collapsed", "  " not in edited)
    check("edit log written", bool(log), f"{len(log)} edits")
    with tempfile.TemporaryDirectory() as td:
        case = ak.CaseInput.load(os.path.join(ROOT, "examples", "case.json"))
        audit, res = ak.Audit("t"), ak.Result(td, "writing-02")
        ok = skill.solve(case, td, audit, res)
        doc = res.write(case, audit, ak.derive_status(audit, ok), "t", ak.utc_now(), ["selftest"])
        check("demo completes", ok)
        check("status success", doc["status"] == "success", doc["status"])
        check("numbers preserved", doc["result"]["preservation"]["ok"])
        check("mode is llm when a candidate exists", doc["result"]["mode"] == "llm")
        check("polished text written", os.path.isfile(os.path.join(td, "polished.md")))
        bad = [e for e in doc["evidence"] if not ak.verify_anchor(td, e["anchor"])[0]]
        check("anchors re-slice", not bad, f"{len(doc['evidence'])} anchors")
        check("no token class missing", not any(doc["result"]["preservation"]["missing"].values()))
    print(f"\n{PASS} passed, {FAIL} failed")
    return 0 if FAIL == 0 else 1
if __name__ == "__main__":
    raise SystemExit(main())
