"""Required tests may not disappear through skips or quarantine."""

import sys
import xml.etree.ElementTree as ET


def check(path):
    root = ET.parse(path).getroot()
    cases = list(root.iter("testcase"))
    return bool(cases) and not any(
        case.find(tag) is not None for case in cases for tag in ("skipped", "failure", "error")
    )


if __name__ == "__main__":
    raise SystemExit(0 if check(sys.argv[1]) else 1)
