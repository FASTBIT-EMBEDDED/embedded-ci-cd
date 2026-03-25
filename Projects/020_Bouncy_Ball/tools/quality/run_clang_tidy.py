import argparse, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def get_sources(cfg_path: Path):
    import json
    cfg = json.loads(cfg_path.read_text())
    inc  = [ROOT / p for p in cfg.get("include_dirs", [])]
    exc  = {p for p in cfg.get("exclude_dirs", [])}
    srcs = []
    for d in inc:
        for f in d.rglob("*.c"):
            rel = str(f.relative_to(ROOT)).replace("\\", "/")
            if not any(rel.startswith(e) for e in exc):
                srcs.append(f)
    return srcs

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--build-dir", required=True)
    args = p.parse_args()

    cfg_path = ROOT / "project.cfg"
    sources  = get_sources(cfg_path)
    build_db = Path(args.build_dir) / "compile_commands.json"

    if not build_db.exists():
        print(f"[FAIL] compile_commands.json not found in {args.build_dir}")
        sys.exit(1)

    failed = []
    for src in sources:
        r = subprocess.run(
            ["clang-tidy", f"-p={args.build_dir}", str(src)],
            capture_output=True, text=True
        )
        if r.returncode != 0:
            print(r.stdout + r.stderr)
            failed.append(src.name)

    if failed:
        print(f"[FAIL] clang-tidy: {len(failed)} file(s) failed")
        sys.exit(1)
    print(f"[PASS] clang-tidy: {len(sources)} file(s) clean")

if __name__ == "__main__":
    main()