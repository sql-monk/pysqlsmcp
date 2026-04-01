"""
run_tests.py — Test orchestrator for pysqlsmcp.

Usage:
    python run_tests.py --server localhost --database mcp_test_main --database-aux mcp_test_aux --impersonate mcp-server
    python run_tests.py            # interactive prompt for missing parameters

The script runs every pytest test in the tests/ directory, captures per-test
results via a custom pytest plugin, then writes a Markdown report to
  test_YYYYMMDDHHSS.md
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import textwrap
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).parent
TESTS_DIR = PROJECT_ROOT / "tests"

# ---------------------------------------------------------------------------
# Argument / interactive input
# ---------------------------------------------------------------------------

def _ask(prompt: str, default: str = "") -> str:
    """Ask the user interactively, returning stripped input."""
    suffix = f" [{default}]" if default else ""
    try:
        val = input(f"{prompt}{suffix}: ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        sys.exit(1)
    return val or default


def get_params() -> tuple[str, str, str, str]:
    parser = argparse.ArgumentParser(
        description="pysqlsmcp test orchestrator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--server",       help="SQL Server host/instance")
    parser.add_argument("--database",     help="Main test database")
    parser.add_argument("--database-aux", help="Auxiliary test database")
    parser.add_argument("--impersonate",  help="Login to impersonate")
    args, _ = parser.parse_known_args()

    server       = args.server       or _ask("SQL Server host/instance", "localhost")
    database     = args.database     or _ask("Main test database",       "mcp_test_main")
    database_aux = args.database_aux or _ask("Auxiliary test database",  "mcp_test_aux")
    impersonate  = args.impersonate  or _ask("Login to impersonate",     "mcp-server")

    if not server:
        print("ERROR: --server is required."); sys.exit(1)
    if not database:
        print("ERROR: --database is required."); sys.exit(1)
    if not database_aux:
        print("ERROR: --database-aux is required."); sys.exit(1)
    if not impersonate:
        print("ERROR: --impersonate is required."); sys.exit(1)

    return server, database, database_aux, impersonate


# ---------------------------------------------------------------------------
# Run pytest with JSON-line report plugin
# ---------------------------------------------------------------------------

_PLUGIN_SOURCE = textwrap.dedent("""\
import json, sys, time, pytest

class LineReporter:
    def __init__(self):
        self._start: dict[str, float] = {}

    def pytest_runtest_logstart(self, nodeid, location):
        self._start[nodeid] = time.monotonic()

    def pytest_runtest_logreport(self, report):
        if report.when != "call":
            if report.failed and report.when in ("setup", "teardown"):
                pass
            else:
                return
        elapsed = time.monotonic() - self._start.get(report.nodeid, 0)
        record = {
            "nodeid": report.nodeid,
            "outcome": report.outcome,
            "duration": round(elapsed, 3),
            "longrepr": str(report.longrepr) if report.longrepr else None,
        }
        print("##PYTEST_RECORD##" + json.dumps(record), flush=True)

def pytest_configure(config):
    config.pluginmanager.register(LineReporter(), "line_reporter")
""")

_PLUGIN_PATH = PROJECT_ROOT / "_tmp_reporter_plugin.py"


def run_pytest(server: str, database: str, database_aux: str, impersonate: str) -> tuple:
    """Run pytest, parse embedded JSON lines, return list of result dicts."""
    _PLUGIN_PATH.write_text(_PLUGIN_SOURCE, encoding="utf-8")
    try:
        cmd = [
            sys.executable, "-m", "pytest",
            str(TESTS_DIR),
            "-v",
            "--tb=short",
            f"--server={server}",
            f"--database={database}",
            f"--database-aux={database_aux}",
            f"--impersonate={impersonate}",
            "-p", "_tmp_reporter_plugin",
            "--override-ini=python_files=test_*.py",
        ]
        env = os.environ.copy()
        env["PYTHONPATH"] = str(PROJECT_ROOT) + os.pathsep + env.get("PYTHONPATH", "")
        env["PYTHONDONTWRITEBYTECODE"] = "1"

        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            env=env,
            cwd=str(PROJECT_ROOT),
        )
        records: list[dict] = []
        for line in proc.stdout.splitlines():
            if line.startswith("##PYTEST_RECORD##"):
                try:
                    records.append(json.loads(line[len("##PYTEST_RECORD##"):]))
                except json.JSONDecodeError:
                    pass
        return records, proc.stdout, proc.stderr, proc.returncode
    finally:
        try:
            _PLUGIN_PATH.unlink()
        except OSError:
            pass


# ---------------------------------------------------------------------------
# Module / group helpers
# ---------------------------------------------------------------------------

_GROUP_MAP = {
    "test_db_provider":                     "DbProvider",
    "test_execute_query":                   "executeQuery",
    "test_explain_query":                   "explainQuery",
    "test_get_database_permission":         "getDatabasePermission",
    "test_get_all_database_permission":     "getAllDatabasePermission",
    "test_required_additional_permission":  "requiredAdditionalPermission",
    "test_mcp_registration":               "MCP Registration",
}


def _group_from_nodeid(nodeid: str) -> str:
    path_part = nodeid.split("::")[0]
    stem = Path(path_part).stem
    return _GROUP_MAP.get(stem, stem)


def _test_id_from_nodeid(nodeid: str) -> str:
    """Extract the class::method or function from nodeid."""
    parts = nodeid.split("::")
    if len(parts) >= 3:
        return f"{parts[1]}::{parts[2]}"
    elif len(parts) == 2:
        return parts[1]
    return nodeid


def _extract_docstring(nodeid: str) -> str:
    """Attempt to extract the test docstring for a human-readable description."""
    parts = nodeid.split("::")
    file_path = PROJECT_ROOT / parts[0]
    if not file_path.exists():
        return ""
    try:
        source = file_path.read_text(encoding="utf-8")
    except Exception:
        return ""
    func_name = parts[-1] if len(parts) >= 2 else ""
    # search for def func_name ... """ docstring """
    pattern = rf'def\s+{re.escape(func_name)}\s*\(.*?\).*?:\s*\n\s*"""(.*?)"""'
    m = re.search(pattern, source, re.DOTALL)
    if m:
        return m.group(1).strip().split("\n")[0].strip()
    return func_name.replace("_", " ")


# ---------------------------------------------------------------------------
# Markdown report builder
# ---------------------------------------------------------------------------

_STATUS_ICON = {"passed": "✅", "failed": "❌", "error": "💥", "skipped": "⏭️"}


def _icon(outcome: str) -> str:
    return _STATUS_ICON.get(outcome, "❓")


def build_report(
    records: list[dict],
    server: str,
    database: str,
    database_aux: str,
    impersonate: str,
    started_at: datetime,
    finished_at: datetime,
    raw_stdout: str,
    raw_stderr: str,
) -> str:
    total = len(records)
    passed = sum(1 for r in records if r["outcome"] == "passed")
    failed = sum(1 for r in records if r["outcome"] in ("failed", "error"))
    skipped = sum(1 for r in records if r["outcome"] == "skipped")
    duration_total = sum(r["duration"] for r in records)

    overall = "✅ ALL PASSED" if failed == 0 and total > 0 else f"❌ {failed} FAILED"

    lines: list[str] = []

    # ── Header ────────────────────────────────────────────────────────────
    lines += [
        "# pysqlsmcp — Test Report",
        "",
        f"**Started:** {started_at.strftime('%Y-%m-%d %H:%M:%S')}  ",
        f"**Finished:** {finished_at.strftime('%Y-%m-%d %H:%M:%S')}  ",
        f"**Duration:** {duration_total:.2f}s  ",
        f"**Server:** `{server}`  ",
        f"**Database:** `{database}`  ",
        f"**Database (aux):** `{database_aux}`  ",
        f"**Impersonate:** `{impersonate}`  ",
        "",
        f"## Overall: {overall}",
        "",
        f"| Total | Passed | Failed | Skipped |",
        f"|------:|-------:|-------:|--------:|",
        f"| {total} | {passed} | {failed} | {skipped} |",
        "",
    ]

    # ── Summary table — one row per test ──────────────────────────────────
    lines += [
        "## Test Summary",
        "",
        "| # | Group | Test | Status | Duration |",
        "|--:|-------|------|--------|----------|",
    ]
    for i, r in enumerate(records, 1):
        group = _group_from_nodeid(r["nodeid"])
        test_id = _test_id_from_nodeid(r["nodeid"])
        desc = _extract_docstring(r["nodeid"])
        label = desc if desc else test_id
        icon = _icon(r["outcome"])
        dur = f"{r['duration']:.3f}s"
        lines.append(f"| {i} | {group} | {label} | {icon} {r['outcome']} | {dur} |")

    lines.append("")

    # ── Failures detail ───────────────────────────────────────────────────
    failures = [r for r in records if r["outcome"] in ("failed", "error")]
    if failures:
        lines += [
            "## Failures & Errors",
            "",
        ]
        for r in failures:
            group = _group_from_nodeid(r["nodeid"])
            test_id = _test_id_from_nodeid(r["nodeid"])
            desc = _extract_docstring(r["nodeid"])
            lines += [
                f"### {group} / {test_id}",
                "",
                f"**Description:** {desc}  " if desc else "",
                f"**Node:** `{r['nodeid']}`  ",
                f"**Outcome:** {_icon(r['outcome'])} {r['outcome']}  ",
                "",
                "```",
                (r["longrepr"] or "(no detail)").strip(),
                "```",
                "",
            ]
    else:
        lines += ["## Failures & Errors", "", "_No failures — all tests passed._", ""]

    # ── Per-test detail ───────────────────────────────────────────────────
    lines += [
        "## Test Details",
        "",
        "What every test validates and its result.",
        "",
    ]
    current_group = None
    for r in records:
        group = _group_from_nodeid(r["nodeid"])
        if group != current_group:
            current_group = group
            lines += [f"### {group}", ""]

        test_id = _test_id_from_nodeid(r["nodeid"])
        desc = _extract_docstring(r["nodeid"])
        icon = _icon(r["outcome"])
        lines += [
            f"- {icon} **{test_id}** — {desc}  ",
            f"  Result: {r['outcome']} ({r['duration']:.3f}s)",
            "",
        ]

    # ── Raw pytest output (collapsed) ─────────────────────────────────────
    lines += [
        "<details>",
        "<summary>Raw pytest output</summary>",
        "",
        "```",
        raw_stdout[:8000] if len(raw_stdout) > 8000 else raw_stdout,
        "```",
        "",
        "</details>",
        "",
    ]

    if raw_stderr.strip():
        lines += [
            "<details>",
            "<summary>stderr</summary>",
            "",
            "```",
            raw_stderr[:4000] if len(raw_stderr) > 4000 else raw_stderr,
            "```",
            "",
            "</details>",
            "",
        ]

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    server, database, database_aux, impersonate = get_params()

    print(f"\npysqlsmcp test runner")
    print(f"  Server      : {server}")
    print(f"  Database    : {database}")
    print(f"  Database aux: {database_aux}")
    print(f"  Impersonate : {impersonate}")
    print(f"  Tests dir   : {TESTS_DIR}\n")

    started_at = datetime.now()
    print("Running pytest …\n")
    records, stdout, stderr, returncode = run_pytest(server, database, database_aux, impersonate)
    finished_at = datetime.now()

    if not records:
        print("WARNING: No test records collected. Check that pytest ran correctly.")
        print(stdout[-2000:] if stdout else "(no stdout)")
        if stderr:
            print(stderr[-1000:])

    report_md = build_report(
        records, server, database, database_aux, impersonate,
        started_at, finished_at, stdout, stderr
    )

    timestamp = started_at.strftime("%Y%m%d%H%M")
    report_path = PROJECT_ROOT / f"test_{timestamp}.md"
    report_path.write_text(report_md, encoding="utf-8")

    total = len(records)
    passed = sum(1 for r in records if r["outcome"] == "passed")
    failed = sum(1 for r in records if r["outcome"] in ("failed", "error"))

    print(f"\nResults: {passed}/{total} passed, {failed} failed")
    print(f"Report : {report_path}")

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
