import sys
from pathlib import Path

from common import (
    ROOT,
    get_source_files,
    load_config,
    normalize_rel_path,
    print_header,
    print_status,
    run_command,
    write_report,
)

def main() -> int:
    cfg = load_config()
    build_dir = ROOT / cfg.get("build_dir", "build/Debug")

    files = [p for p in get_source_files() if p.suffix in {".c", ".cpp"}]

    if not files:
        print_status("Clang-tidy", "WARN", "No source files found")
        return 0

    print_header("CLANG-TIDY")

    total = len(files)
    clean = 0
    warned = 0
    failed = 0
    all_logs = []

    for path in files:
        rel = normalize_rel_path(path)
        cmd = [
            "clang-tidy",
            str(path),
            "-p",
            str(build_dir),
            "--quiet",
        ]
        code, output = run_command(cmd)

        if code == 0 and not output.strip():
            print_status(rel, "PASS")
            clean += 1
        elif code == 0 and output.strip():
            print_status(rel, "WARN")
            print(output)
            warned += 1
            all_logs.append(f"\n=== {rel} ===\n{output}")
        else:
            print_status(rel, "FAIL")
            if output.strip():
                print(output)
                all_logs.append(f"\n=== {rel} ===\n{output}")
            failed += 1

    summary = []
    summary.append(f"Total files : {total}")
    summary.append(f"Clean       : {clean}")
    summary.append(f"Warnings    : {warned}")
    summary.append(f"Failed      : {failed}")

    write_report("clang_tidy.log", "\n".join(summary) + "\n" + "\n".join(all_logs))

    if failed > 0:
        print_status("Clang-tidy summary", "FAIL", f"{failed} file(s) failed")
        return 1

    if warned > 0:
        print_status("Clang-tidy summary", "WARN", f"{warned} file(s) with warnings")
        return 0

    print_status("Clang-tidy summary", "PASS", f"All {total} files clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())