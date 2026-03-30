import argparse
import subprocess
import sys
from pathlib import Path

from common import get_source_files, print_header, print_status, write_report


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--build-dir", required=True,
                   help="Directory containing compile_commands.json")
    args = p.parse_args()

    build_db = Path(args.build_dir) / "compile_commands.json"
    if not build_db.exists():
        print_status("clang-tidy", "FAIL",
                     f"compile_commands.json not found in {args.build_dir}")
        return 1

    print_header("CLANG-TIDY")

    sources = [f for f in get_source_files() if f.suffix == ".c"]
    failed = []

    for src in sources:
        r = subprocess.run(
            ["clang-tidy", f"-p={args.build_dir}", str(src)],
            capture_output=True, text=True,
        )
        if r.returncode != 0:
            print(r.stdout + r.stderr)
            failed.append(src.name)

    report = "\n".join(f"FAIL: {n}" for n in failed) if failed else "All files clean"
    write_report("clang_tidy.log", report)

    if failed:
        print_status("clang-tidy", "FAIL", f"{len(failed)} file(s) failed")
        return 1

    print_status("clang-tidy", "PASS", f"{len(sources)} file(s) clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
