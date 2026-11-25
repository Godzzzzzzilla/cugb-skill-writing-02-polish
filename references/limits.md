# Limits

| condition | behaviour |
|---|---|
| hedge expressed with a synonym outside the vocabulary | invisible to the audit |
| number spelled out ("twenty-three percent") | not matched as a number |
| citation in a footnote marker (`¹`) | not matched |
| candidate substantially rewritten | pairs fall below 70% → `sentences-paired` fails, `partial` |
| CJK draft | token rules apply; the phrase list is English-only |
