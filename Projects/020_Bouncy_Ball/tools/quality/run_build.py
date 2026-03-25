import sys
from pathlib import Path

from common import ROOT, load_config, print_header, print_status, run_command, write_report


def ensure_build_configured(build_dir: Path) -> int:
    build_ninja = build_dir / "build.ninja"
    compile_db = build_dir / "compile_commands.json"

    if build_ninja.exists() or compile_db.exists():
        return 0

    print_status("Configure", "WARN", f"Build directory not configured: {build_dir}")

    build_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        "cube-cmake",
        "-S",
        str(ROOT),
        "-B",
        str(build_dir),
        "-G",
        "Ninja",
    ]
    code, output = run_command(cmd)
    write_report("configure.log", output)

    if code == 0:
        print_status("Configure", "PASS", "Build directory configured")
        return 0

    print_status("Configure", "FAIL", "Configuration failed")
    if output.strip():
        print(output)
    return code


def main() -> int:
    cfg = load_config()
    build_dir = ROOT / cfg.get("build_dir", "build/Debug")

    print_header("BUILD")

    cfg_code = ensure_build_configured(build_dir)
    if cfg_code != 0:
        return cfg_code

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