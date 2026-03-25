import sys

from common import get_source_files, print_header, print_status, run_command, write_report


def main() -> int:
    files = get_source_files()
    if not files:
        print_status("Format check", "WARN", "No source files found")
        return 0

    print_header("FORMAT CHECK")
    cmd = ["clang-format", "--dry-run", "--Werror", *[str(p) for p in files]]
    code, output = run_command(cmd)

    write_report("format_check.log", output)

    if code == 0:
        print_status("Format check", "PASS", f"All {len(files)} files are formatted")
        return 0

    print_status("Format check", "FAIL", "Formatting violations found")
    if output.strip():
        print(output)
    return code


if __name__ == "__main__":
    sys.exit(main())