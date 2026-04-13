#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kiro Agent Context Injection Script

Unlike Claude/Cursor hooks, this script is called INSIDE the agent prompt
via agentSpawn hook and outputs context directly to stdout.

Usage:
    python3 get_agent_context.py --agent implement --format markdown --update-phase
    python3 get_agent_context.py --agent check --format json
"""

# IMPORTANT: Suppress all warnings FIRST
import warnings
warnings.filterwarnings("ignore")

import argparse
import json
import os
import sys
from pathlib import Path

# IMPORTANT: Force stdout to use UTF-8 on Windows
if sys.platform == "win32":
    import io as _io
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    elif hasattr(sys.stdout, "detach"):
        sys.stdout = _io.TextIOWrapper(sys.stdout.detach(), encoding="utf-8", errors="replace")

# =============================================================================
# Path Constants
# =============================================================================

DIR_WORKFLOW = ".bwflow"
FILE_CURRENT_TASK = ".current-task"
FILE_TASK_JSON = "task.json"

# Agents that don't update phase
AGENTS_NO_PHASE_UPDATE = {"debug", "research"}

# =============================================================================
# Core Functions (imported from .bwflow/scripts/common via sys.path)
# =============================================================================

def find_repo_root(start_path: str) -> str | None:
    """Find git repo root from start_path upwards"""
    current = Path(start_path).resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return str(current)
        current = current.parent
    return None


def get_current_task(repo_root: str) -> str | None:
    """Read current task directory path from .bwflow/.current-task"""
    current_task_file = os.path.join(repo_root, DIR_WORKFLOW, FILE_CURRENT_TASK)
    if not os.path.exists(current_task_file):
        return None

    try:
        with open(current_task_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return None
            normalized = content.replace("\\", "/")
            while normalized.startswith("./"):
                normalized = normalized[2:]
            # If it's just a task name (e.g., "04-14-test-feature"), prepend the full path
            if not normalized.startswith(".bwflow/") and not normalized.startswith("tasks/"):
                normalized = f".bwflow/tasks/{normalized}"
            elif normalized.startswith("tasks/"):
                normalized = f".bwflow/{normalized}"
            return normalized
    except Exception:
        return None


def update_current_phase(repo_root: str, task_dir: str, agent_type: str) -> None:
    """Update current_phase in task.json based on agent_type"""
    if agent_type in AGENTS_NO_PHASE_UPDATE:
        return

    task_json_path = os.path.join(repo_root, task_dir, FILE_TASK_JSON)
    if not os.path.exists(task_json_path):
        return

    try:
        with open(task_json_path, "r", encoding="utf-8") as f:
            task_data = json.load(f)

        current_phase = task_data.get("current_phase", 0)
        next_actions = task_data.get("next_action", [])

        # Map action names to agent types
        action_to_agent = {
            "implement": "implement",
            "check": "check",
            "finish": "check",
        }

        # Find the next phase that matches this agent_type
        new_phase = None
        for action in next_actions:
            phase_num = action.get("phase", 0)
            action_name = action.get("action", "")
            expected_agent = action_to_agent.get(action_name)

            if phase_num > current_phase and expected_agent == agent_type:
                new_phase = phase_num
                break

        if new_phase is not None:
            task_data["current_phase"] = new_phase
            with open(task_json_path, "w", encoding="utf-8") as f:
                json.dump(task_data, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


def read_file_content(base_path: str, file_path: str) -> str | None:
    """Read file content, return None if file doesn't exist"""
    full_path = os.path.join(base_path, file_path)
    if os.path.exists(full_path) and os.path.isfile(full_path):
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return None
    return None


def read_directory_contents(
    base_path: str, dir_path: str, max_files: int = 20
) -> list[tuple[str, str]]:
    """Read all .md files in a directory"""
    full_path = os.path.join(base_path, dir_path)
    if not os.path.exists(full_path) or not os.path.isdir(full_path):
        return []

    results = []
    try:
        md_files = sorted(
            [
                f
                for f in os.listdir(full_path)
                if f.endswith(".md") and os.path.isfile(os.path.join(full_path, f))
            ]
        )

        for filename in md_files[:max_files]:
            file_full_path = os.path.join(full_path, filename)
            relative_path = os.path.join(dir_path, filename)
            try:
                with open(file_full_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    results.append((relative_path, content))
            except Exception:
                continue
    except Exception:
        pass

    return results


def read_jsonl_entries(base_path: str, jsonl_path: str) -> list[tuple[str, str]]:
    """Read all file/directory contents referenced in jsonl file"""
    full_path = os.path.join(base_path, jsonl_path)
    if not os.path.exists(full_path):
        return []

    results = []
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    item = json.loads(line)
                    file_path = item.get("file") or item.get("path")
                    entry_type = item.get("type", "file")

                    if not file_path:
                        continue

                    if entry_type == "directory":
                        dir_contents = read_directory_contents(base_path, file_path)
                        results.extend(dir_contents)
                    else:
                        content = read_file_content(base_path, file_path)
                        if content:
                            results.append((file_path, content))
                except json.JSONDecodeError:
                    continue
    except Exception:
        pass

    return results


def get_implement_context(repo_root: str, task_dir: str) -> list[tuple[str, str]]:
    """Get context for Implement Agent"""
    context = []

    # 1. implement.jsonl (or fallback to spec.jsonl)
    entries = read_jsonl_entries(repo_root, f"{task_dir}/implement.jsonl")
    if not entries:
        entries = read_jsonl_entries(repo_root, f"{task_dir}/spec.jsonl")
    context.extend(entries)

    # 2. prd.md
    prd_content = read_file_content(repo_root, f"{task_dir}/prd.md")
    if prd_content:
        context.append((f"{task_dir}/prd.md", prd_content))

    # 3. info.md
    info_content = read_file_content(repo_root, f"{task_dir}/info.md")
    if info_content:
        context.append((f"{task_dir}/info.md", info_content))

    return context


def get_check_context(repo_root: str, task_dir: str) -> list[tuple[str, str]]:
    """Get context for Check Agent"""
    context = []

    # check.jsonl
    entries = read_jsonl_entries(repo_root, f"{task_dir}/check.jsonl")
    if entries:
        context.extend(entries)
    else:
        # Fallback: hardcoded check files + spec.jsonl
        check_files = [
            ".kiro/steering/commands/finish-work.md",
            ".kiro/steering/commands/check.md",
        ]
        for file_path in check_files:
            content = read_file_content(repo_root, file_path)
            if content:
                context.append((file_path, content))

        # Add spec.jsonl
        spec_entries = read_jsonl_entries(repo_root, f"{task_dir}/spec.jsonl")
        context.extend(spec_entries)

    # prd.md
    prd_content = read_file_content(repo_root, f"{task_dir}/prd.md")
    if prd_content:
        context.append((f"{task_dir}/prd.md", prd_content))

    return context


def get_debug_context(repo_root: str, task_dir: str) -> list[tuple[str, str]]:
    """Get context for Debug Agent"""
    entries = read_jsonl_entries(repo_root, f"{task_dir}/debug.jsonl")
    return entries


def format_markdown(context: list[tuple[str, str]]) -> str:
    """Format context as markdown"""
    if not context:
        return "## Task Context\n\nNo context files found."

    parts = ["## Task Context\n"]
    for file_path, content in context:
        parts.append(f"### {file_path}\n\n```\n{content}\n```\n")
    return "\n".join(parts)


def format_json(context: list[tuple[str, str]]) -> str:
    """Format context as JSON"""
    return json.dumps(
        [{"file": fp, "content": c} for fp, c in context],
        indent=2,
        ensure_ascii=False
    )


def main():
    parser = argparse.ArgumentParser(
        description="Get agent context for Kiro IDE"
    )
    parser.add_argument(
        "--agent",
        required=True,
        choices=["implement", "check", "debug"],
        help="Agent type"
    )
    parser.add_argument(
        "--format",
        default="markdown",
        choices=["markdown", "json"],
        help="Output format"
    )
    parser.add_argument(
        "--update-phase",
        action="store_true",
        help="Update current_phase in task.json"
    )

    args = parser.parse_args()

    # Find repo root
    repo_root = find_repo_root(os.getcwd())
    if not repo_root:
        print("Error: Not in a git repository", file=sys.stderr)
        sys.exit(1)

    # Get current task
    task_dir = get_current_task(repo_root)
    if not task_dir:
        print("Error: No active task. Run task.py to create a task first.", file=sys.stderr)
        sys.exit(1)

    # Update phase if requested
    if args.update_phase:
        update_current_phase(repo_root, task_dir, args.agent)

    # Get context based on agent type
    if args.agent == "implement":
        context = get_implement_context(repo_root, task_dir)
    elif args.agent == "check":
        context = get_check_context(repo_root, task_dir)
    elif args.agent == "debug":
        context = get_debug_context(repo_root, task_dir)
    else:
        context = []

    # Format and output
    if args.format == "json":
        print(format_json(context))
    else:
        print(format_markdown(context))


if __name__ == "__main__":
    main()
