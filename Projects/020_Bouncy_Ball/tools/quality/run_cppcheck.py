import sys

from common import (
    ROOT,
    get_source_files,
    load_config,
    print_header,
    print_status,
    run_command,
    write_report,
)

def main() -> int:
    cfg = load_config()
    include_dirs = [str(ROOT / p) for p in cfg.get("include_dirs", [])]
    suppressions = ROOT / "cppcheck" / "suppressions.txt"

    print_header("CPPCHECK")

    cmd = [
        "cppcheck",
        "--enable=warning,style,performance,portability",
        "--inconclusive",
        "--force",
        "--quiet",
        "--language=c",
        "--std=c11",
        "--inline-suppr",
        f"--suppressions-list={suppressions}",
        "--xml",
        "--xml-version=2",
        *include_dirs,
    ]

    code, output = run_command(cmd)
    write_report("cppcheck.xml", output)

    if code == 0 and not output.strip():
        print_status("Cppcheck", "PASS", "No findings")
        return 0

    if code in (0, 1):
        print_status("Cppcheck", "WARN", "Findings present, see reports/cppcheck.xml")
        if output.strip():
            print(output)
        return 0

    print_status("Cppcheck", "FAIL", "cppcheck execution failed")
    if output.strip():
        print(output)
    return code


if __name__ == "__main__":
    sys.exit(main())