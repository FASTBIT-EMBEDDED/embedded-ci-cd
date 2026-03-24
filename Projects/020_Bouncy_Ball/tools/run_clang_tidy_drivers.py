from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "Core" / "drivers"
BUILD = ROOT / "build" / "Debug"

exts = {".c", ".cpp"}
files = sorted(p for p in TARGET.rglob("*") if p.suffix in exts)

# ANSI colors
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
BOLD = "\033[1m"

if not files:
    print(f"{YELLOW}No C/C++ files found in Core/drivers{RESET}")
    sys.exit(0)

passed = 0
failed = 0
warned = 0

for path in files:
    rel = path.relative_to(ROOT)

    cmd = [
        "clang-tidy",
        str(path),
        "-p",
        str(BUILD),
        "--quiet",
    ]

    result = subprocess.run(
        cmd,
        cwd=ROOT,
        capture_output=True,
        text=True
    )

    output = (result.stdout + "\n" + result.stderr).strip()

    print(f"\n{CYAN}{BOLD}=== {rel} ==={RESET}")

    if result.returncode == 0:
        if output:
            print(f"{YELLOW}WARNINGS{RESET}")
            print(output)
            warned += 1
            passed += 1
        else:
            print(f"{GREEN}PASS{RESET}")
            passed += 1
    else:
        print(f"{RED}FAIL{RESET}")
        if output:
            print(output)
        failed += 1

print(f"\n{BOLD}========== SUMMARY =========={RESET}")
print(f"Total files : {len(files)}")
print(f"{GREEN}Passed      : {passed}{RESET}")
print(f"{YELLOW}Warnings    : {warned}{RESET}")
print(f"{RED}Failed      : {failed}{RESET}")

sys.exit(1 if failed else 0)