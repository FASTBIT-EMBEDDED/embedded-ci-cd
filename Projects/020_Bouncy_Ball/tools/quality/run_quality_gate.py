import subprocess
import sys
from pathlib import Path

from common import ROOT, print_header, print_status

TOOLS_DIR = Path(__file__).resolve().parent

STEPS = [
    ("Build", TOOLS_DIR / "run_build.py"),
    ("Format check", TOOLS_DIR / "format_check.py"),
    ("Cppcheck", TOOLS_DIR / "run_cppcheck.py"),
    ("Clang-tidy", TOOLS_DIR / "run_clang_tidy.py"),
]

def main() -> int:
    print_header("QUALITY GATE")

    failed = 0

    for label, script in STEPS:
        result = subprocess.run([sys.executable, str(script)], cwd=str(ROOT))
        if result.returncode != 0:
            failed += 1
            print_status(label, "FAIL", "Step failed")
            break
        else:
            print_status(label, "PASS", "Step completed")

    print()
    if failed:
        print_status("Quality gate", "FAIL", "One or more steps failed")
        return 1

    print_status("Quality gate", "PASS", "All steps completed")
    return 0


if __name__ == "__main__":
    sys.exit(main())