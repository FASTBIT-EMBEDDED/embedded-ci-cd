from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "Core" / "drivers"

exts = {".c", ".h", ".cpp", ".hpp"}
files = sorted(str(p) for p in TARGET.rglob("*") if p.suffix in exts)

if not files:
    print("No source files found in Core/drivers")
    sys.exit(0)

cmd = ["clang-format", "-i", *files]
print("Running:", " ".join(cmd))
subprocess.run(cmd, check=True)

print("Formatting applied to Core/drivers.")