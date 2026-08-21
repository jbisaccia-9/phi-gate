"""Score the detectors against the hand-labeled corpus.

Recall is the safety metric: a missed identifier reaches the LLM. Precision is
the usability metric: over-redaction destroys the text's value. The gate weighs
them accordingly (recall bar higher than precision bar).
"""
import json
import pathlib
from .patterns import detect

ROOT = pathlib.Path(__file__).resolve().parents[2]


def load_corpus():
    return [json.loads(l) for l in
            (ROOT / "data" / "corpus.jsonl").read_text().splitlines() if l.strip()]


def evaluate():
    tp = fp = fn = 0
    misses, extras = [], []
    for case in load_corpus():
        got = set(map(tuple, detect(case["text"])))
        want = set(map(tuple, case["expected"]))
        tp += len(got & want)
        for f in got - want: fp += 1; extras.append((case["id"], f))
        for f in want - got: fn += 1; misses.append((case["id"], f))
    recall = tp / (tp + fn) if tp + fn else 1.0
    precision = tp / (tp + fp) if tp + fp else 1.0
    report = {"cases": len(load_corpus()), "true_positives": tp,
              "false_positives": fp, "false_negatives": fn,
              "recall": round(recall, 4), "precision": round(precision, 4),
              "missed": [f"{c}: {t} {v}" for c, (t, v) in misses],
              "known_false_positives": [f"{c}: {t} {v}" for c, (t, v) in extras]}
    out = ROOT / "results"; out.mkdir(exist_ok=True)
    (out / "report.json").write_text(json.dumps(report, indent=2))
    return report
