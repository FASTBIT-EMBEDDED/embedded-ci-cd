import subprocess
import sys

from common import ROOT, load_config, print_header, print_status, write_report


def main() -> int:
    cfg  = load_config()
    dirs = [str(ROOT / d) for d in cfg["include_dirs"]]
    supp = ROOT / "cppcheck" / "suppressions.txt"

    print_header("CPPCHECK")

    cmd = [
        "cppcheck", "--enable=all", "--error-exitcode=1",
        f"--suppressions-list={supp}",
        "--inline-suppr",
        *dirs,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    output = r.stdout + r.stderr
    write_report("cppcheck.log", output)

    if r.returncode != 0:
        print(output)
        print_status("cppcheck", "FAIL", "Errors found")
        return 1

    print_status("cppcheck", "PASS", "No errors found")
    return 0


if __name__ == "__main__":
    sys.exit(main())
