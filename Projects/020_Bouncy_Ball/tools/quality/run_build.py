import sys

from common import ROOT, load_config, print_header, print_status, run_command, write_report

def main() -> int:
    cfg = load_config()
    build_dir = ROOT / cfg.get("build_dir", "build/Debug")

    print_header("BUILD")

    cmd = ["cube-cmake", "--build", str(build_dir)]
    code, output = run_command(cmd)

    write_report("build.log", output)

    if code == 0:
        print_status("Build", "PASS", "Build completed successfully")
        return 0

    print_status("Build", "FAIL", "Build failed")
    if output.strip():
        print(output)
    return code


if __name__ == "__main__":
    sys.exit(main())