from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Iterable, List, Tuple

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config" / "quality_targets.json"
REPORTS_DIR = ROOT / "reports"

RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
BOLD = "\033[1m"


def supports_color() -> bool:
    return sys.stdout.isatty()


def color(text: str, code: str) -> str:
    if supports_color():
        return f"{code}{text}{RESET}"
    return text


def load_config() -> dict:
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def normalize_rel_path(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def get_source_files() -> List[Path]:
    cfg = load_config()

    include_dirs = [ROOT / p for p in cfg.get("include_dirs", [])]
    exclude_dirs = {p.replace("\\", "/") for p in cfg.get("exclude_dirs", [])}
    exclude_files = {p.replace("\\", "/") for p in cfg.get("exclude_files", [])}
    exts = set(cfg.get("source_extensions", []))

    results: List[Path] = []

    for inc_dir in include_dirs:
        if not inc_dir.exists():
            continue

        for p in inc_dir.rglob("*"):
            if not p.is_file():
                continue
            if p.suffix not in exts:
                continue

            rel = normalize_rel_path(p)

            if rel in exclude_files:
                continue

            skip = False
            for ex_dir in exclude_dirs:
                if rel == ex_dir or rel.startswith(ex_dir + "/"):
                    skip = True
                    break
            if skip:
                continue

            results.append(p)

    return sorted(results)


def ensure_reports_dir() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def write_report(name: str, content: str) -> None:
    ensure_reports_dir()
    report_path = REPORTS_DIR / name
    report_path.write_text(content, encoding="utf-8")


def run_command(
    cmd: List[str],
    cwd: Path | None = None,
    capture_output: bool = True,
) -> Tuple[int, str]:
    result = subprocess.run(
        cmd,
        cwd=str(cwd or ROOT),
        capture_output=capture_output,
        text=True,
    )
    output = ""
    if capture_output:
        output = (result.stdout or "") + (result.stderr or "")
    return result.returncode, output


def print_header(title: str) -> None:
    print()
    print(color("=" * 60, CYAN))
    print(color(title, BOLD))
    print(color("=" * 60, CYAN))


def print_status(label: str, status: str, detail: str = "") -> None:
    if status == "PASS":
        s = color("[PASS]", GREEN)
    elif status == "WARN":
        s = color("[WARN]", YELLOW)
    elif status == "FAIL":
        s = color("[FAIL]", RED)
    else:
        s = f"[{status}]"

    line = f"{s} {label}"
    if detail:
        line += f" - {detail}"
    print(line)


def rel_files(files: Iterable[Path]) -> List[str]:
    return [normalize_rel_path(p) for p in files]