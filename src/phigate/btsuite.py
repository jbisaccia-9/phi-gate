"""Braintrust-shaped eval suite: data -> task -> scorers.

Data is the labeled corpus, the task is detection, and the scorers mirror the
gate's two axes plus a per-case exactness score. The known lot-code false
positive (c17) keeps case_exact below 1.0 permanently - the suite pins that
honesty as a number instead of a footnote.
"""
from .eval import load_corpus, evaluate
from .patterns import detect


def task(case):
    return {"findings": sorted(map(tuple, detect(case["text"])))}


def case_exact(case, out):
    return 1.0 if out["findings"] == sorted(map(tuple, case["expected"])) else 0.0


def run_local():
    cases = load_corpus()
    exact = round(sum(case_exact(c, task(c)) for c in cases) / len(cases), 4)
    rep = evaluate()
    scores = {"case_exact": exact, "recall": rep["recall"], "precision": rep["precision"]}
    for k, v in scores.items():
        print(f"  {k}: {v}")
    ok = rep["recall"] >= 0.95 and rep["precision"] >= 0.90
    print("SUITE: PASS - detection holds." if ok else "SUITE: FAIL - detection regressed.")
    return 0 if ok else 1


def push_braintrust():
    import braintrust  # optional extra
    braintrust.Eval("phi-gate",
                    data=lambda: [{"input": c, "expected": c["expected"]} for c in load_corpus()],
                    task=task,
                    scores=[lambda input, expected, output:
                            braintrust.Score(name="case_exact",
                                             score=case_exact(input, output))])
