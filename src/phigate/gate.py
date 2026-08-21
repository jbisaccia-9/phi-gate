"""Redaction gate: this scrubber may sit in front of an LLM only if it clears
the corpus. Recall >= 0.95 (a miss is leaked PHI-shaped data) and precision
>= 0.90 (over-redaction destroys the document). Exit 1 otherwise."""
import sys

RECALL_MIN, PRECISION_MIN = 0.95, 0.90


def check(report):
    checks = [("recall", report["recall"], RECALL_MIN),
              ("precision", report["precision"], PRECISION_MIN)]
    failed = False
    for name, value, minimum in checks:
        ok = value >= minimum
        print(f"  {'PASS' if ok else 'FAIL'}  {name}: {value} (min {minimum})")
        failed |= not ok
    for line in report["missed"]:
        print(f"    MISSED: {line}")
    for line in report["known_false_positives"]:
        print(f"    known FP: {line}")
    if failed:
        print("GATE: FAILED - do not put this redactor in front of an LLM.")
        return 1
    print("GATE: PASSED - redactor cleared the corpus.")
    return 0


if __name__ == "__main__":
    from .eval import evaluate
    sys.exit(check(evaluate()))
