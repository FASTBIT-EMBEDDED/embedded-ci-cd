# quality_targets.json

This file controls which files and folders are included in the quality checks.

The same config is used by:
- formatting scripts
- format check scripts
- cppcheck
- clang-tidy
- quality gate flow

So if you want to change what gets checked, change this file first.

---

## Full example

```json
{
    "include_dirs": [
        "Core/drivers"
    ],
    "exclude_dirs": [
        "Core/Inc",
        "Core/Src",
        "Drivers",
        "build",
        ".git",
        ".github",
        ".vscode",
        "reports"
    ],
    "exclude_files": [],
    "source_extensions": [
        ".c",
        ".h",
        ".cpp",
        ".hpp"
    ],
    "build_dir": "build/Debug",
    "project_name": "020_Bouncy_Ball"
}