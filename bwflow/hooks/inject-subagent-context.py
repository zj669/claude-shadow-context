#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-Agent Pipeline Context Injection Hook for bwflow

Trigger: PreToolUse (before Task tool call)

Context Source: bwflow/.current-task points to task directory
- implement.jsonl - Implement agent dedicated context
- check.jsonl     - Check agent dedicated context
- debug.jsonl     - Debug agent dedicated context
- prd.md          - Requirements document
"""

# IMPORTANT: Suppress all warnings FIRST
import warnings
warnings.filterwarnings("ignore")

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

DIR_WORKFLOW = "bwflow"
FILE_CURRENT_TASK = ".current-task"
FILE_TASK_JSON = "task.json"

AGENTS_NO_PHASE_UPDATE = {"debug", "research"}

AGENT_IMPLEMENT = "implement"
AGENT_CHECK = "check"
AGENT_DEBUG = "debug"
AGENT_RESEARCH = "research"

AGENTS_REQUIRE_TASK = (AGENT_IMPLEMENT, AGENT_CHECK, AGENT_DEBUG)
AGENTS_ALL = (AGENT_IMPLEMENT, AGENT_CHECK, AGENT_DEBUG, AGENT_RESEARCH)


def find_repo_root(start_path: str) -> str | None:
    """Find git repo root from start_path upwards"""
    current = Path(start_path).resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return str(current)
        current = current.parent
    return None


def get_current_task(repo_root: str) -> str | None:
    """Read current task directory path from bwflow/.current-task"""
    current_task_file = os.path.join(repo_root, DIR_WORKFLOW, FILE_CURRENT_TASK)
    if not os.path.exists(current_task_file):
        return None

    try:
        with open(current_task_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
            return content if content else None
    except Exception:
        return None


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
                    if file_path:
                        content = read_file_content(base_path, file_path)
                        if content:
                            results.append((file_path, content))
                except json.JSONDecodeError:
                    continue
    except Exception:
        pass

    return results


def get_context_for_agent(repo_root: str, task_dir: str, agent_type: str) -> str:
    """Get complete context for specified agent"""
    context_parts = []

    # Try agent-specific jsonl first
    jsonl_path = f"{task_dir}/{agent_type}.jsonl"
    entries = read_jsonl_entries(repo_root, jsonl_path)

    # Fallback to spec.jsonl if agent-specific doesn't exist
    if not entries:
        entries = read_jsonl_entries(repo_root, f"{task_dir}/spec.jsonl")

    for file_path, content in entries:
        context_parts.append(f"=== {file_path} ===\n{content}")

    # Add prd.md if exists
    prd_content = read_file_content(repo_root, f"{task_dir}/prd.md")
    if prd_content:
        context_parts.append(f"=== {task_dir}/prd.md (Requirements) ===\n{prd_content}")

    return "\n\n".join(context_parts)


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    hook_event = input_data.get("hook_event_name", "")
    if hook_event != "PreToolUse":
        sys.exit(0)

    tool_name = input_data.get("tool_name", "")
    if tool_name != "Task":
        sys.exit(0)

    tool_input = input_data.get("tool_input", {})
    subagent_type = tool_input.get("subagent_type", "")

    if subagent_type not in AGENTS_ALL:
        sys.exit(0)

    cwd = input_data.get("cwd", os.getcwd())
    repo_root = find_repo_root(cwd)
    if not repo_root:
        sys.exit(0)

    # Get current task
    task_dir = get_current_task(repo_root)
    if not task_dir and subagent_type in AGENTS_REQUIRE_TASK:
        sys.exit(0)

    # Get context
    if subagent_type == AGENT_IMPLEMENT:
        context = get_context_for_agent(repo_root, task_dir, "implement")
    elif subagent_type == AGENT_CHECK:
        context = get_context_for_agent(repo_root, task_dir, "check")
    elif subagent_type == AGENT_DEBUG:
        context = get_context_for_agent(repo_root, task_dir, "debug")
    else:
        context = ""

    if context:
        result = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "additionalContext": context,
            }
        }
        print(json.dumps(result, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
