"""PHI-shaped pattern detectors for the regex tier.

Scope is stated honestly: this tier catches STRUCTURED identifiers (SSNs, phone
numbers, emails, MRNs, member IDs, keyword-anchored birth dates). Free-text
names and addresses need an NER tier and are explicitly out of scope here —
a redactor that overstates its coverage is worse than one that states it.

Two context-anchored rules keep precision honest:
  * a bare 9-digit number is NOT an SSN unless SSN context is nearby
    (invoice and order numbers are 9 digits too);
  * a date is NOT a birth date unless DOB context is nearby
    (appointment dates are not PHI by themselves).
"""
import re

DETECTORS = {
    "SSN": re.compile(r"\b\d{3}[- ]\d{2}[- ]\d{4}\b"),
    "SSN_CONTEXT": re.compile(r"(?i)\bssn\b[^\d]{0,12}(\d{9})\b"),
    "PHONE": re.compile(r"\(?\b\d{3}\)?[-. ]\d{3}[-. ]\d{4}\b"),
    "EMAIL": re.compile(r"\b[\w.+-]+@[\w-]+\.[A-Za-z]{2,}\b"),
    "MRN": re.compile(r"(?i)\bmrn[:# ]*\d{6,10}\b"),
    "MEMBER_ID": re.compile(r"\b[A-Z]{3}\d{9}\b"),
    "DOB": re.compile(r"(?i)\b(?:dob|date of birth|born)\b[^\d]{0,10}(\d{1,2}/\d{1,2}/\d{4})"),
}
# Which label each detector's hits report as (context detectors fold into their type).
CANON = {"SSN_CONTEXT": "SSN"}


def detect(text):
    """Return a list of (type, matched_value) findings, deduplicated."""
    found = []
    for name, rx in DETECTORS.items():
        for m in rx.finditer(text):
            value = m.group(1) if m.groups() else m.group(0)
            found.append((CANON.get(name, name), value))
    return sorted(set(found))


def redact(text):
    """Replace every finding with a typed placeholder, longest match first."""
    findings = detect(text)
    for kind, value in sorted(findings, key=lambda f: -len(f[1])):
        text = text.replace(value, f"[{kind}]")
    return text, findings
