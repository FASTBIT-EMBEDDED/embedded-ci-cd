import subprocess, sys, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    cfg  = json.loads((ROOT / "project.cfg").read_text())
    dirs = [str(ROOT / d) for d in cfg.get("include_dirs", [])]
    exc  = [f"--suppress=*:{ROOT}/{e}/*" for e in cfg.get("exclude_dirs", [])]
    supp = ROOT / "cppcheck" / "suppressions.txt"

    cmd = [
        "cppcheck", "--enable=all", "--error-exitcode=1",
        f"--suppressions-list={supp}",
        "--inline-suppr",
        *exc,
        *dirs,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(r.stdout + r.stderr)
    if r.returncode != 0:
        print("[FAIL] cppcheck")
        sys.exit(1)
    print("[PASS] cppcheck")

if __name__ == "__main__":
    main()