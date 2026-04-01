"""
pysqlsmcp Test Orchestrator
───────────────────────────
Runs the integration test suite against mcp_test_main / mcp_test_aux,
displays live progress, and generates a detailed report.

Usage:
    python run_tests.py [--server INSTANCE] [--report FILE]

Environment:
    PYSQLSMCP_TEST_SERVER  — SQL Server instance (default: localhost)
"""

import argparse
import json
import os
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TESTS_DIR = ROOT / "tests"
REPORT_DIR = ROOT / "reports"


# ── colours ──────────────────────────────────────────────────

def _enable_ansi() -> bool:
    """Try to enable ANSI escape codes on Windows; return True if supported."""
    if sys.platform != "win32":
        return True
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
        # STD_OUTPUT_HANDLE = -11, ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
        handle = kernel32.GetStdHandle(-11)
        mode = ctypes.c_ulong()
        kernel32.GetConsoleMode(handle, ctypes.byref(mode))
        kernel32.SetConsoleMode(handle, mode.value | 0x0004)
        return True
    except Exception:
        return False


_ANSI = _enable_ansi()


class C:
    GREEN  = "\033[92m" if _ANSI else ""
    RED    = "\033[91m" if _ANSI else ""
    YELLOW = "\033[93m" if _ANSI else ""
    CYAN   = "\033[96m" if _ANSI else ""
    BOLD   = "\033[1m"  if _ANSI else ""
    DIM    = "\033[2m"  if _ANSI else ""
    RESET  = "\033[0m"  if _ANSI else ""


def _colour(text: str, colour: str) -> str:
    if not colour:
        return text
    return f"{colour}{text}{C.RESET}"


# ── data types ───────────────────────────────────────────────

class TestResult:
    __slots__ = ("name", "classname", "file", "status", "duration", "message", "details")

    def __init__(self, name: str, classname: str, file: str, status: str,
                 duration: float, message: str = "", details: str = ""):
        self.name = name
        self.classname = classname
        self.file = file
        self.status = status          # passed | failed | error | skipped
        self.duration = duration
        self.message = message
        self.details = details

    @property
    def full_name(self) -> str:
        return f"{self.classname}::{self.name}"

    @property
    def status_icon(self) -> str:
        return {"passed": "✓", "failed": "✗", "error": "✗", "skipped": "○"}.get(self.status, "?")

    @property
    def status_colour(self) -> str:
        return {"passed": C.GREEN, "failed": C.RED, "error": C.RED, "skipped": C.YELLOW}.get(self.status, "")


# ── run pytest ───────────────────────────────────────────────

def run_pytest(server: str, impersonate: str) -> tuple[list[TestResult], float]:
    """Run pytest with JUnit XML output, parse results."""
    REPORT_DIR.mkdir(exist_ok=True)
    xml_path = REPORT_DIR / "junit.xml"

    env = os.environ.copy()
    env["PYSQLSMCP_TEST_SERVER"] = server
    env["PYSQLSMCP_TEST_IMPERSONATE"] = impersonate
    env["PYSQLSMCP_DBG"] = "1"

    print(f"\n{C.BOLD}{'═' * 68}{C.RESET}")
    print(f"  {C.CYAN}pysqlsmcp Integration Tests{C.RESET}")
    print(f"  Server:      {C.BOLD}{server}{C.RESET}")
    print(f"  Impersonate: {C.BOLD}{impersonate}{C.RESET}")
    print(f"  Time:        {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{C.BOLD}{'═' * 68}{C.RESET}\n")

    cmd = [
        sys.executable, "-m", "pytest",
        str(TESTS_DIR),
        f"--junitxml={xml_path}",
        "-v",
        "--tb=short",
        "-q",
    ]

    proc = subprocess.run(cmd, cwd=str(ROOT), env=env, capture_output=True, text=True)

    # Print live output
    if proc.stdout:
        for line in proc.stdout.splitlines():
            if "PASSED" in line:
                print(f"  {_colour('✓', C.GREEN)} {line}")
            elif "FAILED" in line:
                print(f"  {_colour('✗', C.RED)} {line}")
            elif "ERROR" in line:
                print(f"  {_colour('✗', C.RED)} {line}")
            elif "SKIPPED" in line or "SKIP" in line:
                print(f"  {_colour('○', C.YELLOW)} {line}")
            elif line.strip():
                print(f"  {C.DIM}{line}{C.RESET}")

    if proc.stderr:
        for line in proc.stderr.splitlines():
            if line.strip():
                print(f"  {C.DIM}{line}{C.RESET}")

    # Parse JUnit XML
    results: list[TestResult] = []
    total_time = 0.0

    if xml_path.exists():
        tree = ET.parse(xml_path)
        root = tree.getroot()
        total_time = float(root.attrib.get("time", 0))

        for testsuite in root.iter("testsuite"):
            for tc in testsuite.iter("testcase"):
                name = tc.attrib.get("name", "")
                classname = tc.attrib.get("classname", "")
                file = tc.attrib.get("file", "")
                duration = float(tc.attrib.get("time", 0))

                failure = tc.find("failure")
                error = tc.find("error")
                skipped = tc.find("skipped")

                if failure is not None:
                    status = "failed"
                    message = failure.attrib.get("message", "")
                    details = failure.text or ""
                elif error is not None:
                    status = "error"
                    message = error.attrib.get("message", "")
                    details = error.text or ""
                elif skipped is not None:
                    status = "skipped"
                    message = skipped.attrib.get("message", "")
                    details = ""
                else:
                    status = "passed"
                    message = ""
                    details = ""

                results.append(TestResult(name, classname, file, status, duration, message, details))

    return results, total_time


# ── report generation ────────────────────────────────────────

# Description map for every test
TEST_DESCRIPTIONS: dict[str, str] = {
    # ── VIEW DEFINITION — main ──
    "test_impersonation_succeeds": "Імперсонація mcp-server працює (USER_NAME())",
    "test_sys_tables": "sys.tables — список таблиць з схемами",
    "test_sys_columns": "sys.columns — колонки таблиці Customers",
    "test_sys_procedures": "sys.procedures — список збережених процедур",
    "test_sys_views": "sys.views — список view-ів",
    "test_sys_schemas": "sys.schemas — наявність dbo, sales, inventory",
    "test_object_definition_procedure": "OBJECT_DEFINITION для usp_SearchProducts",
    "test_object_definition_view": "OBJECT_DEFINITION для vw_CustomerOrders",
    "test_object_definition_function": "OBJECT_DEFINITION для fn_WarehouseTotalQty",
    "test_sys_foreign_keys": "sys.foreign_keys — зовнішні ключі",
    "test_sys_indexes": "sys.indexes — індекси таблиці Customers",
    "test_sys_synonyms": "sys.synonyms — синоніми та їх base_object_name",
    "test_sys_sql_expression_dependencies": "sys.sql_expression_dependencies — cross-db залежності",
    # ── VIEW DATABASE STATE ──
    "test_dm_exec_sessions": "dm_exec_sessions — активні сесії",
    "test_dm_exec_requests": "dm_exec_requests — активні запити",
    "test_dm_exec_connections": "dm_exec_connections — з'єднання",
    "test_dm_db_index_usage_stats": "dm_db_index_usage_stats — статистика індексів",
    # ── VIEW DATABASE PERFORMANCE STATE ──
    "test_dm_exec_query_stats": "dm_exec_query_stats — статистика запитів",
    "test_dm_os_wait_stats": "dm_os_wait_stats — статистика очікувань",
    # ── VIEW DATABASE SECURITY STATE ──
    "test_database_permissions": "sys.database_permissions — дозволи для mcp-test-* юзерів",
    "test_database_role_members": "sys.database_role_members — membership mcp-test-* юзерів",
    "test_database_principals": "sys.database_principals — ролі role_reader/writer/admin",
    # ── DENIED — user data main ──
    "test_denied_select_customers": "DENIED: SELECT з dbo.Customers",
    "test_denied_select_products": "DENIED: SELECT з inventory.Products",
    "test_denied_select_orders": "DENIED: SELECT з sales.Orders",
    "test_denied_select_view": "DENIED: SELECT з view (vw_CustomerOrders або vw_StockSummary)",
    "test_denied_insert": "DENIED: INSERT в таблицю",
    "test_denied_update": "DENIED: UPDATE таблиці Customers",
    "test_denied_delete": "DENIED: DELETE з таблиці",
    "test_denied_exec_procedure": "DENIED: EXEC збереженої процедури",
    "test_denied_select_function": "DENIED: виклик скалярної функції",
    "test_denied_select_audit_log": "DENIED: SELECT з AuditLog",
    # ── DENIED — user data aux ──
    "test_denied_select_warehouses": "DENIED: SELECT з dbo.Warehouses",
    "test_denied_select_warehouse_stock": "DENIED: SELECT з dbo.WarehouseStock",
    "test_denied_select_shipments": "DENIED: SELECT з dbo.Shipments",
    # ── explain_query ──
    "test_simple_select_plan": "SHOWPLAN_XML для простого SELECT * FROM Customers",
    "test_join_plan": "SHOWPLAN_XML для JOIN (Customers + Orders або WarehouseStock + Warehouses)",
    "test_cross_schema_join_plan": "SHOWPLAN_XML для cross-schema JOIN (sales + inventory)",
    "test_cross_db_view_plan": "SHOWPLAN_XML для cross-db view",
    "test_subquery_plan": "SHOWPLAN_XML для запиту з підзапитом",
    "test_invalid_table_returns_error": "SHOWPLAN_XML для неіснуючої таблиці — error",
    "test_invalid_syntax_returns_error": "SHOWPLAN_XML для некоректного SQL — error",
    "test_warehouse_plan": "SHOWPLAN_XML для SELECT * FROM Warehouses",
    "test_function_in_query_plan": "SHOWPLAN_XML для запиту з функцією",
    "test_cross_db_proc_plan": "SHOWPLAN_XML для cross-db процедури",
    # ── permissions ──
    "test_all_permissions_no_filter": "Всі permissions без фільтрів",
    "test_filter_by_user_reader": "Permissions: фільтр user=mcp-test-reader",
    "test_filter_by_user_writer": "Permissions: фільтр user=mcp-test-writer",
    "test_filter_by_user_admin": "Permissions: фільтр user=mcp-test-admin",
    "test_filter_by_object_customers": "Permissions: фільтр object=Customers",
    "test_filter_by_object_products": "Permissions: фільтр object=Products",
    "test_filter_by_object_warehouses": "Permissions: фільтр object=Warehouses",
    "test_filter_by_object_shipments": "Permissions: фільтр object=Shipments",
    "test_filter_by_object_nonexistent": "Permissions: неіснуючий об'єкт — 0 результатів",
    "test_combined_filter_admin_customers": "Permissions: комбо user=admin + object=Customers",
    "test_combined_filter_reader_orders": "Permissions: комбо user=reader + object=Orders",
    "test_all_permissions": "Всі permissions в mcp_test_aux",
    "test_list_databases_contains_test_dbs": "list_databases: mcp_test_main + mcp_test_aux присутні",
    "test_scan_all_with_admin_filter": "getAllDatabasePermission: скан всіх БД з user=admin",
    "test_scan_all_with_reader_filter": "getAllDatabasePermission: скан всіх БД з user=reader",
    "test_scan_all_with_nonexistent_user": "getAllDatabasePermission: неіснуючий user — 0 результатів",
    # ── required permissions — main ──
    "test_view_aux_warehouse_refs_aux": "Cross-db: vw_AuxWarehouse -> mcp_test_aux.dbo.Warehouses",
    "test_proc_product_warehouse_stock_refs_aux": "Cross-db: usp_ProductWarehouseStock -> mcp_test_aux",
    "test_synonym_warehouses": "Synonym: syn_Warehouses -> mcp_test_aux.dbo.Warehouses",
    "test_local_view_no_cross_deps": "Локальний view vw_CustomerOrders — 0 cross-db залежностей",
    "test_local_proc_search_products_no_deps": "Локальна процедура usp_SearchProducts — 0 залежностей",
    "test_cross_schema_proc": "Cross-schema: sales.usp_GetCustomerOrders -> dbo",
    "test_nonexistent_object": "Неіснуючий об'єкт — 0 рядків, без помилки",
    # ── required permissions — aux ──
    "test_view_stock_with_products_refs_main": "Cross-db: vw_StockWithProductNames -> mcp_test_main",
    "test_proc_stock_report_refs_main": "Cross-db: usp_StockReport -> mcp_test_main.inventory.Products",
    "test_synonym_products": "Synonym: syn_Products -> mcp_test_main.inventory.Products",
    "test_local_proc_get_warehouse_info_no_deps": "Локальна usp_GetWarehouseInfo — 0 залежностей",
    "test_local_view_stock_summary_no_deps": "Локальний vw_StockSummary — 0 залежностей",
    # ── recursive dependencies ──
    "test_recursive_from_product_warehouse_stock": "Рекурсивний обхід: usp_ProductWarehouseStock",
    "test_recursive_from_stock_report": "Рекурсивний обхід: usp_StockReport",
    "test_recursive_local_proc_zero_deps": "Рекурсивний обхід: локальна процедура — 0 залежностей",
    "test_recursive_nonexistent_object": "Рекурсивний обхід: неіснуючий об'єкт — 0",
    # ── security ──
    "test_revert_keyword_neutralised": "REVERT в запиті — нейтралізація через regex",
    "test_revert_as_string_literal": "Слово 'revert' як string literal — не ламає запит",
}


def generate_report(results: list[TestResult], total_time: float, server: str, impersonate: str, report_path: Path) -> None:
    """Generate Markdown report."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    passed = sum(1 for r in results if r.status == "passed")
    failed = sum(1 for r in results if r.status == "failed")
    errors = sum(1 for r in results if r.status == "error")
    skipped = sum(1 for r in results if r.status == "skipped")
    total = len(results)

    lines: list[str] = []
    w = lines.append

    w(f"# pysqlsmcp — Test Report")
    w(f"")
    w(f"| Parameter | Value |")
    w(f"|-----------|-------|")
    w(f"| Server | `{server}` |")
    w(f"| Impersonate | `{impersonate}` |")
    w(f"| Date | {now} |")
    w(f"| Duration | {total_time:.2f}s |")
    w(f"| Total | {total} |")
    w(f"| Passed | {passed} |")
    w(f"| Failed | {failed} |")
    w(f"| Errors | {errors} |")
    w(f"| Skipped | {skipped} |")
    w(f"")

    # Summary table
    w(f"## Summary")
    w(f"")
    w(f"| # | Status | Test | Duration | Description |")
    w(f"|--:|:------:|------|----------|-------------|")

    for i, r in enumerate(results, 1):
        icon = {"passed": "✅", "failed": "❌", "error": "❌", "skipped": "⏭️"}.get(r.status, "❓")
        desc = TEST_DESCRIPTIONS.get(r.name, "")
        w(f"| {i} | {icon} | `{r.full_name}` | {r.duration:.3f}s | {desc} |")

    w(f"")

    # Detailed: only non-passed tests + all tests with descriptions
    w(f"## Detailed Results")
    w(f"")

    # Group by file/class
    groups: dict[str, list[TestResult]] = {}
    for r in results:
        groups.setdefault(r.classname, []).append(r)

    for classname, class_results in groups.items():
        w(f"### {classname}")
        w(f"")

        for r in class_results:
            icon = {"passed": "✅", "failed": "❌", "error": "❌", "skipped": "⏭️"}.get(r.status, "❓")
            desc = TEST_DESCRIPTIONS.get(r.name, "—")
            w(f"#### {icon} `{r.name}` ({r.duration:.3f}s)")
            w(f"")
            w(f"**Description:** {desc}")
            w(f"")

            if r.status in ("failed", "error"):
                w(f"**Error:** {r.message}")
                w(f"")
                if r.details:
                    w(f"<details>")
                    w(f"<summary>Full traceback</summary>")
                    w(f"")
                    w(f"```")
                    w(r.details.rstrip())
                    w(f"```")
                    w(f"</details>")
                    w(f"")

        w(f"")

    report_path.parent.mkdir(exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")


def print_summary(results: list[TestResult], total_time: float) -> None:
    """Print coloured summary to terminal."""
    passed = sum(1 for r in results if r.status == "passed")
    failed = sum(1 for r in results if r.status == "failed")
    errors = sum(1 for r in results if r.status == "error")
    skipped = sum(1 for r in results if r.status == "skipped")
    total = len(results)

    print(f"\n{C.BOLD}{'═' * 68}{C.RESET}")
    print(f"  {C.BOLD}RESULTS{C.RESET}")
    print(f"{'═' * 68}")
    print(f"  Total:   {total}")
    print(f"  Passed:  {_colour(str(passed), C.GREEN)}")
    if failed:
        print(f"  Failed:  {_colour(str(failed), C.RED)}")
    if errors:
        print(f"  Errors:  {_colour(str(errors), C.RED)}")
    if skipped:
        print(f"  Skipped: {_colour(str(skipped), C.YELLOW)}")
    print(f"  Time:    {total_time:.2f}s")
    print(f"{'═' * 68}")

    if failed or errors:
        print(f"\n  {C.RED}{C.BOLD}FAILED TESTS:{C.RESET}")
        for r in results:
            if r.status in ("failed", "error"):
                print(f"    {_colour('✗', C.RED)} {r.full_name}")
                if r.message:
                    print(f"      {C.DIM}{r.message[:120]}{C.RESET}")

    print()


# ── main ─────────────────────────────────────────────────────

def _resolve_param(cli_value: str | None, env_var: str, prompt_label: str,
                   example: str, default: str | None = None) -> str:
    """Resolve a parameter: CLI arg > env var > interactive prompt."""
    if cli_value:
        return cli_value
    env = os.environ.get(env_var, "").strip()
    if env:
        return env
    # Interactive prompt
    hint = f" [{default}]" if default else ""
    value = input(f"  {prompt_label} (e.g. {example}){hint}: ").strip()
    if not value:
        if default:
            return default
        print(f"  {_colour(f'Aborted — {prompt_label} not provided.', C.RED)}")
        sys.exit(1)
    return value


def main():
    parser = argparse.ArgumentParser(description="pysqlsmcp test orchestrator")
    parser.add_argument("--server", default=None,
                        help="SQL Server instance (or set PYSQLSMCP_TEST_SERVER env var)")
    parser.add_argument("--impersonate", default=None,
                        help="Login to impersonate (default: mcp-server, or PYSQLSMCP_TEST_IMPERSONATE env var)")
    parser.add_argument("--report", default=str(REPORT_DIR / "test-report.md"),
                        help="Path to output report (default: reports/test-report.md)")
    args = parser.parse_args()

    server = _resolve_param(args.server, "PYSQLSMCP_TEST_SERVER",
                            "SQL Server instance", "localhost, .\\SQLEXPRESS")
    impersonate = _resolve_param(args.impersonate, "PYSQLSMCP_TEST_IMPERSONATE",
                                 "Impersonate login", "mcp-server", default="mcp-server")
    results, total_time = run_pytest(server, impersonate)

    print_summary(results, total_time)

    report_path = Path(args.report)
    generate_report(results, total_time, server, impersonate, report_path)
    print(f"  Report saved to: {report_path}\n")

    # Exit code
    failed = sum(1 for r in results if r.status in ("failed", "error"))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
