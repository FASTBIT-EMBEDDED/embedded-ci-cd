import argparse, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def get_sources():
    import json
    cfg = json.loads((ROOT / "project.cfg").read_text())
    inc = [ROOT / p for p in cfg.get("include_dirs", [])]
    srcs = []
    for d in inc:
        for ext in ("*.c", "*.h", "*.cpp", "*.hpp"):
            srcs.extend(d.rglob(ext))
    return srcs

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--fix",   action="store_true")
    p.add_argument("--check", action="store_true")
    args = p.parse_args()

    sources = get_sources()
    if args.fix:
        subprocess.run(["clang-format", "-i", *[str(s) for s in sources]])
        print(f"[PASS] format applied to {len(sources)} files")
    else:
        r = subprocess.run(
            ["clang-format", "--dry-run", "--Werror", *[str(s) for s in sources]],
            capture_output=True, text=True
        )
        if r.returncode != 0:
            print(r.stderr)
            print("[FAIL] format check")
            sys.exit(1)
        print(f"[PASS] format check: {len(sources)} files clean")

if __name__ == "__main__":
    main()