from pathlib import Path
import sys

from common import get_source_files, print_header, print_status, run_command, write_report

def main() -> int:
    files = get_source_files()
    if not files:
        print_status("Format apply", "WARN", "No source files found")
        return 0

    print_header("FORMAT APPLY")
    cmd = ["clang-format", "-i", *[str(p) for p in files]]
    code, output = run_command(cmd)

    write_report("format_apply.log", output)

    if code == 0:
        print_status("Format apply", "PASS", f"Formatted {len(files)} files")
        return 0

    print_status("Format apply", "FAIL", "clang-format failed")
    if output.strip():
        print(output)
    return code


if __name__ == "__main__":
    sys.exit(main())