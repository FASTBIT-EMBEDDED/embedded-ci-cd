# Quality Workflow for `020_Bouncy_Ball`

This project uses a small quality system for:

- formatting
- build verification
- static analysis
- CI/CD reuse

The goal is to keep the setup:

- clean
- scalable
- easy to change
- usable both locally and in CI

---

# Folder Structure

```text
020_Bouncy_Ball/
├── .clang-format
├── .clang-tidy
├── config/
│   └── quality_targets.json
├── cppcheck/
│   └── suppressions.txt
├── tools/
│   └── quality/
│       ├── common.py
│       ├── format_apply.py
│       ├── format_check.py
│       ├── run_cppcheck.py
│       ├── run_clang_tidy.py
│       ├── run_build.py
│       └── run_quality_gate.py
├── reports/
├── .vscode/
│   ├── settings.json
│   └── tasks.json
└── .github/
    └── workflows/
        └── ci.yml