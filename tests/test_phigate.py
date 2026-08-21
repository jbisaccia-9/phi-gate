from phigate.patterns import detect, redact
from phigate.eval import evaluate, load_corpus
from phigate.gate import check


def test_context_rules_hold():
    # Bare 9 digits: not an SSN. With SSN context: is one.
    assert detect("order 123456789 shipped") == []
    assert ("SSN", "123456789") in detect("SSN 123456789 on file")
    # A date alone is not PHI; a DOB-anchored date is.
    assert detect("see you 4/17/2026") == []
    assert ("DOB", "4/17/2026") in detect("DOB 4/17/2026")


def test_redaction_replaces_with_typed_placeholders():
    text, findings = redact("Call 480-555-0142 or email a@b.test")
    assert "[PHONE]" in text and "[EMAIL]" in text
    assert "480-555-0142" not in text and "a@b.test" not in text
    assert len(findings) == 2


def test_corpus_integrity():
    cases = load_corpus()
    assert len(cases) == 24
    assert len({c["id"] for c in cases}) == 24


def test_gate_on_current_corpus():
    report = evaluate()
    assert report["recall"] >= 0.95, report["missed"]
    assert check(report) == 0


def test_gate_refuses_bad_metrics():
    assert check({"recall": 0.80, "precision": 0.99, "missed": [], "known_false_positives": []}) == 1
    assert check({"recall": 1.0, "precision": 0.5, "missed": [], "known_false_positives": []}) == 1
