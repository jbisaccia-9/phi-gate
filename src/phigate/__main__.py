"""CLI:  python -m phigate scan  (eval report) | gate | redact "some text" """
import json
import sys
from . import eval as ev, gate
from .patterns import redact


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "scan"
    if cmd == "suite":
        from .btsuite import run_local
        sys.exit(run_local())
    if cmd == "scan":
        print(json.dumps(ev.evaluate(), indent=2))
    elif cmd == "gate":
        sys.exit(gate.check(ev.evaluate()))
    elif cmd == "redact":
        text, findings = redact(" ".join(sys.argv[2:]))
        print(text)
        for kind, value in findings:
            print(f"  redacted {kind}: {value}", file=sys.stderr)
    else:
        sys.exit(f"unknown command {cmd!r}")


if __name__ == "__main__":
    main()
