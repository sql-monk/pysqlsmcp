"""
pysqlsmcp — agent config registration
  - registers the MCP server in agent config files (VS Code, Claude Desktop, etc.)
"""

import json
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent

# ── helpers ──────────────────────────────────────────────────

def _heading(text: str) -> None:
    print(f"\n{'=' * 60}\n  {text}\n{'=' * 60}")


def _ask_yes_no(prompt: str, default: bool = True) -> bool:
    hint = "Y/n" if default else "y/N"
    answer = input(f"{prompt} [{hint}]: ").strip().lower()
    if not answer:
        return default
    return answer in ("y", "yes")


# ── agent integration ────────────────────────────────────────

KNOWN_CONFIGS = {
    "VS Code (user)": {
        "relative": Path("Code", "User", "mcp.json"),
        "env": "APPDATA",
    },
    "Claude Desktop": {
        "relative": Path("Claude", "claude_desktop_config.json"),
        "env": "APPDATA",
    },
}


def _server_entry() -> dict:
    python = sys.executable
    return {
        "command": python,
        "args": [str(ROOT / "sqlsmcp.py")],
    }


def _find_config_files(search_root: Path) -> list[Path]:
    """Recursively search for known MCP config files."""
    found: list[Path] = []
    for label, info in KNOWN_CONFIGS.items():
        env_val = os.environ.get(info["env"], "")
        if env_val:
            candidate = Path(env_val) / info["relative"]
            if candidate.exists():
                found.append(candidate)
    # Also scan for mcp.json / claude_desktop_config.json under search_root
    if search_root.exists():
        for pattern in ("**/mcp.json", "**/claude_desktop_config.json"):
            for p in search_root.glob(pattern):
                if p not in found:
                    found.append(p)
    return found


def _patch_vscode_mcp(config_path: Path) -> None:
    data = json.loads(config_path.read_text(encoding="utf-8")) if config_path.exists() else {}
    servers = data.setdefault("servers", {})
    servers["pysqlsmcp"] = _server_entry()
    if "inputs" not in data:
        data["inputs"] = []
    config_path.write_text(json.dumps(data, indent="\t", ensure_ascii=False) + "\n", encoding="utf-8")


def _patch_claude_config(config_path: Path) -> None:
    data = json.loads(config_path.read_text(encoding="utf-8")) if config_path.exists() else {}
    servers = data.setdefault("mcpServers", {})
    servers["pysqlsmcp"] = _server_entry()
    config_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def setup_agent_integration() -> None:
    _heading("Agent Integration")
    if not _ask_yes_no("Register pysqlsmcp in an agent config?"):
        return

    home = Path.home()
    search_root_str = input(f"  Search for config files in [{home}]: ").strip()
    search_root = Path(search_root_str) if search_root_str else home

    configs = _find_config_files(search_root)
    if not configs:
        print("  No agent config files found.")
        return

    print("  Found config files:")
    for i, p in enumerate(configs, 1):
        print(f"    {i}. {p}")

    selection = input("  Which to patch? (comma-separated numbers, or 'all'): ").strip().lower()
    if selection == "all":
        selected = configs
    else:
        indices = [int(x.strip()) - 1 for x in selection.split(",") if x.strip().isdigit()]
        selected = [configs[i] for i in indices if 0 <= i < len(configs)]

    for config_path in selected:
        try:
            if config_path.name == "mcp.json":
                _patch_vscode_mcp(config_path)
            elif config_path.name == "claude_desktop_config.json":
                _patch_claude_config(config_path)
            else:
                print(f"! Unknown config format: {config_path.name} — skipped.")
                continue
            print(f"+ Patched {config_path}")
        except Exception as e:
            print(f"- Failed to patch {config_path}: {e}")


# ── main ─────────────────────────────────────────────────────

def main() -> None:
    _heading("pysqlsmcp — agent config registration")
    setup_agent_integration()
    print("\n  Done.\n")


if __name__ == "__main__":
    main()
