"""
pysqlsmcp — agent config registration
  - registers the MCP server in agent config files (VS Code, Claude Desktop, etc.)
"""

import json
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent  # Project root

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


def _server_entry(server_script: str) -> dict:
    python = sys.executable
    return {
        "command": python,
        "args": [str(ROOT / server_script)],
    }


def _find_mcp_servers() -> list[str]:
    """Find all *mcp.py files in the root directory."""
    mcp_servers = []
    for file in ROOT.glob("*mcp.py"):
        mcp_servers.append(file.name)
    return sorted(mcp_servers)


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


def _patch_vscode_mcp(config_path: Path, server_script: str, server_name: str) -> None:
    data = json.loads(config_path.read_text(encoding="utf-8")) if config_path.exists() else {}
    servers = data.setdefault("servers", {})
    servers[server_name] = _server_entry(server_script)
    if "inputs" not in data:
        data["inputs"] = []
    config_path.write_text(json.dumps(data, indent="\t", ensure_ascii=False) + "\n", encoding="utf-8")


def _patch_claude_config(config_path: Path, server_script: str, server_name: str) -> None:
    data = json.loads(config_path.read_text(encoding="utf-8")) if config_path.exists() else {}
    servers = data.setdefault("mcpServers", {})
    servers[server_name] = _server_entry(server_script)
    config_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def setup_agent_integration(use_defaults: bool = False) -> None:
    _heading("Agent Integration")
    if not use_defaults and not _ask_yes_no("Register pysqlsmcp in an agent config?"):
        return

    # Find available MCP servers
    mcp_servers = _find_mcp_servers()
    if not mcp_servers:
        print("  No MCP servers (*mcp.py) found in the project root.")
        return

    print("  Available MCP servers:")
    for i, server in enumerate(mcp_servers, 1):
        print(f"    {i}. {server}")

    # Select MCP servers to register
    if use_defaults:
        selected_servers = mcp_servers
        print(f"  Using --default: registering all {len(selected_servers)} servers")
    else:
        server_selection = input("  Which servers to register? (comma-separated numbers, or 'all'): ").strip().lower()
        if server_selection == "all":
            selected_servers = mcp_servers
        else:
            indices = [int(x.strip()) - 1 for x in server_selection.split(",") if x.strip().isdigit()]
            selected_servers = [mcp_servers[i] for i in indices if 0 <= i < len(mcp_servers)]

    if not selected_servers:
        print("  No servers selected.")
        return

    # Find config files
    if use_defaults:
        home = Path.home()
        search_root = home
        print(f"  Using --default: searching in home directory ({home})")
    else:
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

    # Select config files to patch
    if use_defaults:
        selected_configs = configs
        print(f"  Using --default: patching all {len(selected_configs)} configs")
    else:
        config_selection = input("  Which to patch? (comma-separated numbers, or 'all'): ").strip().lower()
        if config_selection == "all":
            selected_configs = configs
        else:
            indices = [int(x.strip()) - 1 for x in config_selection.split(",") if x.strip().isdigit()]
            selected_configs = [configs[i] for i in indices if 0 <= i < len(configs)]

    # Patch selected configs with selected servers
    for config_path in selected_configs:
        for server_script in selected_servers:
            # Extract server name from filename (e.g., "sqlsmcp.py" -> "pysqlsmcp")
            server_name = server_script.replace(".py", "").replace("_", "-")
            if not server_name.startswith("py"):
                server_name = "py" + server_name

            try:
                if config_path.name == "mcp.json":
                    _patch_vscode_mcp(config_path, server_script, server_name)
                elif config_path.name == "claude_desktop_config.json":
                    _patch_claude_config(config_path, server_script, server_name)
                else:
                    print(f"! Unknown config format: {config_path.name} — skipped.")
                    continue
                print(f"+ Patched {config_path} with {server_name} ({server_script})")
            except Exception as e:
                print(f"- Failed to patch {config_path} with {server_script}: {e}")


# ── main ─────────────────────────────────────────────────────

def main() -> None:
    _heading("pysqlsmcp — agent config registration")

    # Check for --default flag
    use_defaults = "--default" in sys.argv

    if use_defaults:
        print("  Running in default mode: auto-selecting all servers and configs")

    setup_agent_integration(use_defaults)
    print("\n  Done.\n")


if __name__ == "__main__":
    main()
