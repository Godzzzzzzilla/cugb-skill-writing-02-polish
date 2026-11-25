# writing-02-polish — case demo-polish-01

- status: **success** (sentence pairs align and every number, unit, citation, negation and hedge survived)
- checks: 9/9 passed, ratio=1.0
- evidence: 6 anchored claims
- finished: 2026-11-25T07:54:43Z

## Result

```json
{
 "mode": "llm",
 "polished": "# Results\n\nTo evaluate the pretreatment effect, we ran a series of experiments. The samples were\nstored at 4 °C for 12 h before measurement, not at room temperature. Because the\ninstrument drifted during the run, the values in Table 2 may be slightly lower than the\ntrue values. The treatment group showed a 23.4% increase in yield (p = 0.03) over the\ncontrol, consistent with earlier work [2,5]. This effect is likely caused by the larger\nsurface area. The sample size was small (n = 6), so the result may not generalize to\nother catalysts.\n",
 "changes": [],
 "alignment": {
  "pairs": [
   {
    "pair": 1,
    "original_index": 1,
    "candidate_index": 1,
    "original": "In order to evaluate the effect of the pretreatment, we performed a series of experiments.",
    "candidate": "To evaluate the pretreatment effect, we ran a series of experiments.",
    "preservation": {
     "numbers": {
      "ok": true,
      "missing": []
     },
     "units": {
      "ok": true,
      "missing": []
     },
     "citations": {
      "ok": true,
      "missing": []
     },
     "negations": {
      "ok": true,
      "missing": []
     },
     "hedges": {
      "ok": true,
      "missing": []
     }
    }
   },
   {
    "pair": 2,
    "original_index": 2,
    "candidate_index": 2,
    "original": "It is important to note that the samples were not stored at room temperature;",
    "candidate": "The samples were stored at 4 °C for 12 h before measurement, not at room temperature.",
    "preservation": {
     "numbers": {
      "ok": true,
      "missing": []
     },
     "units": {
      "ok": true,
      "missing": []
     },
     "citations": {
      "ok": true,
      "missing": []
     },
     "negations": {
      "ok": true,
      "missing": []
     },
     "hedges": {
      "ok": true,
      "missing": []
     }
    }
   },
   {
    "pair": 3,
    "original_index": 3,
    "candidate_index": 3,
    "original": "they were kept at 4 °C for 12 h before the measurement.",
    "candidate": "Because the instrument drifted during the run, the values in Table 2 may be slightly lower than the true values.",
    "preservation": {
     "numbers": {
      "ok": false,
      "missing": [
       "12",
       "4"
      ]
     },
     "units": {
      "ok": false,
      "missing": [
       "h"
      ]
     },
     "citations": {
      "ok": true,
      "missing": []
     },
     "negations": {
      "ok": true,
      "missing": []
     },
     "hedges": {
      "ok": true,
      "missing": []
     }
    }
   },
   {
    "pair": 4,
    "original_index": 4,
    "candidate_index": 4,
    "original": "Due to the fact that the instrument drifted during the run, the values reported in Table 2 may be slightly lower than the true values.",
    "candidate": "The treatment group showed a 23.4% increase in yield (p = 0.03) over the control, consistent with earlier work [2,5].",
    "preservation": {
     "numbers": {
      "ok": false,
      "missing": [
       "2"
      ]
     },
     "units": {
      "ok": true,
      "missing": []
     },
     "citations": {
      "ok": true,
      "missing": []
     },
     "negations": {
      "ok": true,
      "missing": []
     },
     "hedges": {
      "ok": false,
      "missing": [
       "may"
      ]
     }
    }
   },
   {
    "pair": 5,
    "original_index": 5,
    "candidate_index": 5,
    "original": "The treatment group showed a 23.4% increase in yield (p = 0.03) compared with the control, which is consistent with previous work [2,5].",
    "candidate": "This effect is likely caused by the larger surface area.",
    "preservation": {
     "numbers": {
      "ok": false,
      "missing": [
       "0.03",
       "2,5",
       "23.4%"
      ]
     },
     "units": {
      "ok": true,
      "missing": []
     },
     "citations": {
      "ok": false,
      "missing": [
       "[2,5]"
      ]
     },
     "negations": {
      "ok": true,
      "missing": []
     },
     "hedges": {
      "ok": true,
      "missing": []
     }
    }
   },
   {
    "pair": 6,
    "original_index": 6,
    "candidate_index": 6,
    "original": "We believe that this effect is likely caused by the increased surface area.",
    "candidate": "The sample size was small (n = 6), so the result may not generalize to other catalysts.",
    "preservation": {
     "numbers": {
      "ok": true,
      "missing": []
     },
     "units": {
      "ok": true,
      "missing": []
     },
     "citations": {
      "ok": true,
      "missing": []
     },
     "negations": {
      "ok": true,
      "missing": []
     },
     "hedges": {
      "ok": false,
      "missing": [
       "likely"
      ]
     }
    }
   },
   {
    "pair": 7,
    "original_index": 7,
    "candidate_index": null,
    "original": "It should be noted that the sample size was small (n = 6), and therefore the result may not generalize to other catalysts.",
    "candidate": null,
    "preservation": {
     "dropped": {
      "ok": false,
      "missing": []
     }
    }
   }
  ],
  "sentences_in": 7,
  "sentences_out": 6,
  "paired": 6,
  "dropped": 1,
  "added": 0,
  "dropped_text": [
   "It should be noted that the sample size was small (n = 6), and therefore the result may not generalize to other catalysts."
  ]
 },
 "preservation": {
  "ok": true,
  "missing": {
   "numbers": [],
   "units": [],
   "citations": [],
   "negations": [],
   "hedges": []
  }
 },
 "edit_count": 0
}
```

## Evidence

| id | claim | locator | ok |
|---|---|---|---|
| s1 | sentence 1: In order to evaluate the effect of the pretreatment, we pe | `inputs/draft.md[11:91]` | ✓ |
| s2 | sentence 2: It is important to note that the samples were not stored a | `inputs/draft.md[102:179]` | ✓ |
| s4 | sentence 4: Due to the fact that the instrument drifted
during the run | `inputs/draft.md[236:316]` | ✓ |
| s5 | sentence 5: The treatment group showed a 23.4% increase in yield (p =  | `inputs/draft.md[371:451]` | ✓ |
| s6 | sentence 6: We believe that this effect is likely caused
by the increa | `inputs/draft.md[508:583]` | ✓ |
| s7 | sentence 7: It should be noted that the sample size was small (n = 6), | `inputs/draft.md[584:664]` | ✓ |

## Limits

- a candidate draft was present, so the text was audited and not rewritten
