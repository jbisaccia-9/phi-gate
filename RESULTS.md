# Results

Generated 2026-08-21 by `scripts/make_results.py` — every block below is captured command output, not prose.

## Unit tests

`python -m pytest -q` — exit 0, OK

```
.....                                                                    [100%]
5 passed in 0.01s
```

## Redaction gate on the labeled corpus

`python -m phigate gate` — exit 0, OK

```
PASS  recall: 1.0 (min 0.95)
  PASS  precision: 0.95 (min 0.9)
    known FP: c17: SSN 555-01-9999
GATE: PASSED - redactor cleared the corpus.
```

## Braintrust-shaped eval suite

`python -m phigate suite` — exit 0, OK

```
case_exact: 0.9583
  recall: 1.0
  precision: 0.95
SUITE: PASS - detection holds.
```
