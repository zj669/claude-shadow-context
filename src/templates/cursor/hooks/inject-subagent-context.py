#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-Agent Pipeline Context Injection Hook for Cursor
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

DIR_WORKFLOW = ".bwflow"
FILE_CURRENT_TASK = ".current-task"
FILE_TASK_JSON = "task.json"

AGENTS_NO_PHASE_UPDATE = {"debug", "research"}

AGENT_IMPLEMENT = "implement"
AGENT_CHECK = "check"
AGENT_DEBUG = "debug"
AGENT_RESEARCH = "research"
AGENT_PLAN = "plan"
AGENT_DISPATCH = "dispatch"


def find_repo_root(start_path: str) -> str | None:
    """Find git repo root from start_path upwards"""
    current = Path(start_path).resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return str(current)
        current = current.parent
    return None


def get_current_task(repo_root: str) -> str | None:
    """Read current task directory path"""
    current_task_file = Path(repo_root) / DIR_WORKFLOW / FILE_CURRENT_TASK
    if not current_task_file.is_file():
        return None

    try:
        content = current_task_file.read_text(encoding="utf-8").strip()
        if not content:
            return None
        normalized = content.replace("\\", "/")
        while normalized.startswith("./"):
            normalized = normalized[2:]
        if normalized.startswith("tasks/"):
            normalized = normalized[7:]  # Remove "tasks/" prefix
        return normalized
    except Exception:
        return None


def update_current_phase(repo_root: str, task_dir: str, subagent_type: str) -> None:
    """Update current_phase in task.json based on subagent_type"""
    if subagent_type in AGENTS_NO_PHASE_UPDATE:
        return

    task_json_path = Path(repo_root) / DIR_WORKFLOW / "tasks" / task_dir / FILE_TASK_JSON
    if not task_json_path.is_file():
        return

    try:
        task_data = json.loads(task_json_path.read_text(encoding="utf-8"))

        current_phase = task_data.get("current_phase", 0)
        next_actions = task_data.get("next_action", [])

        action_to_agent = {
            "implement": "implement",
            "check": "check",
            "finish": "check",
        }

        new_phase = None
        for action in next_actions:
            phase_num = action.get("phase", 0)
            action_name = action.get("action", "")
            expected_agent = action_to_agent.get(action_name)

            if phase_num > current_phase and expected_agent == subagent_type:
                new_phase = phase_num
                break

        if new_phase is not None:
            task_data["current_phase"] = new_phase
            task_json_path.write_text(json.dumps(task_data, indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass


def read_file_content(base_path: str, file_path: str) -> str | None:
    """Read file content, return None if file doesn't exist"""
    full_path = Path(base_path) / file_path
    if full_path.is_file():
        try:
            return full_path.read_text(encoding="utf-8")
        except Exception:
            return None
    return None


def read_directory_contents(base_path: str, dir_path: str, max_files: int = 20) -> list[tuple[str, str]]:
    """Read all .md files in a directory"""
    full_path = Path(base_path) / dir_path
    if not full_path.is_dir():
        return []

    results = []
    try:
        md_files = sorted(
            f for f in os.listdir(full_path)
            if f.endswith(".md") and (full_path / f).is_file()
        )

        for filename in md_files[:max_files]:
            file_full_path = full_path / filename
            relative_path = str(Path(dir_path) / filename)
            try:
                content = file_full_path.read_text(encoding="utf-8")
                results.append((relative_path, content))
            except Exception:
                continue
    except Exception:
        pass

    return results


def read_jsonl_entries(base_path: str, jsonl_path: str) -> list[tuple[str, str]]:
    """Read all file/directory contents referenced in jsonl file"""
    full_path = Path(base_path) / jsonl_path
    if not full_path.is_file():
        return []

    results = []
    try:
        for line in full_path.read_text(encoding="utf-8").splitlines():
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


def get_agent_context(repo_root: str, task_dir: str, agent_type: str) -> str:
    """Get complete context for specified agent"""
    context_parts = []

    agent_jsonl = f"{task_dir}/{agent_type}.jsonl"
    agent_entries = read_jsonl_entries(repo_root, f"{DIR_WORKFLOW}/tasks/{agent_jsonl}")

    if not agent_entries:
        agent_entries = read_jsonl_entries(repo_root, f"{DIR_WORKFLOW}/tasks/{task_dir}/spec.jsonl")

    for file_path, content in agent_entries:
        context_parts.append(f"=== {file_path} ===\n{content}")

    return "\n\n".join(context_parts)


def get_implement_context(repo_root: str, task_dir: str) -> str:
    """Complete context for Implement Agent"""
    context_parts = []

    base_context = get_agent_context(repo_root, task_dir, "implement")
    if base_context:
        context_parts.append(base_context)

    prd_content = read_file_content(repo_root, f"{DIR_WORKFLOW}/tasks/{task_dir}/prd.md")
    if prd_content:
        context_parts.append(f"=== {task_dir}/prd.md (Requirements) ===\n{prd_content}")

    info_content = read_file_content(repo_root, f"{DIR_WORKFLOW}/tasks/{task_dir}/info.md")
    if info_content:
        context_parts.append(f"=== {task_dir}/info.md (Technical Design) ===\n{info_content}")

    return "\n\n".join(context_parts)


def get_check_context(repo_root: str, task_dir: str) -> str:
    """Complete context for Check Agent"""
    context_parts = []

    check_entries = read_jsonl_entries(repo_root, f"{DIR_WORKFLOW}/tasks/{task_dir}/check.jsonl")

    if check_entries:
        for file_path, content in check_entries:
            context_parts.append(f"=== {file_path} ===\n{content}")
    else:
        check_files = [
            (f".bwflow/commands/bwflow/check/check.CMD.md", "Check spec"),
        ]
        for file_path, description in check_files:
            content = read_file_content(repo_root, file_path)
            if content:
                context_parts.append(f"=== {file_path} ({description}) ===\n{content}")

        spec_entries = read_jsonl_entries(repo_root, f"{DIR_WORKFLOW}/tasks/{task_dir}/spec.jsonl")
        for file_path, content in spec_entries:
            context_parts.append(f"=== {file_path} ===\n{content}")

    prd_content = read_file_content(repo_root, f"{DIR_WORKFLOW}/tasks/{task_dir}/prd.md")
    if prd_content:
        context_parts.append(f"=== {task_dir}/prd.md (Requirements) ===\n{prd_content}")

    return "\n\n".join(context_parts)


def get_research_context(repo_root: str, task_dir: str) -> str:
    """Complete context for Research Agent"""
    context_parts = []

    research_entries = read_jsonl_entries(repo_root, f"{DIR_WORKFLOW}/tasks/{task_dir}/research.jsonl")
    for file_path, content in research_entries:
        context_parts.append(f"=== {file_path} ===\n{content}")

    prd_content = read_file_content(repo_root, f"{DIR_WORKFLOW}/tasks/{task_dir}/prd.md")
    if prd_content:
        context_parts.append(f"=== {task_dir}/prd.md (Requirements) ===\n{prd_content}")

    return "\n\n".join(context_parts)


def get_context_for_agent(repo_root: str, task_dir: str, agent_type: str) -> str:
    """Get context based on agent type"""
    if agent_type == AGENT_IMPLEMENT:
        return get_implement_context(repo_root, task_dir)
    elif agent_type == AGENT_CHECK:
        return get_check_context(repo_root, task_dir)
    elif agent_type == AGENT_RESEARCH:
        return get_research_context(repo_root, task_dir)
    elif agent_type == AGENT_DEBUG:
        return get_check_context(repo_root, task_dir)
    elif agent_type == AGENT_PLAN:
        return get_implement_context(repo_root, task_dir)
    else:
        return get_implement_context(repo_root, task_dir)


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = input_data.get("tool_name") or input_data.get("tool", "")

    if tool_name != "Task":
        sys.exit(0)

    tool_args = input_data.get("tool_args") or {}
    subagent_type = tool_args.get("subagent_type", "") or tool_args.get("name", "")

    if not subagent_type or subagent_type not in (AGENT_IMPLEMENT, AGENT_CHECK, AGENT_DEBUG, AGENT_RESEARCH, AGENT_PLAN, AGENT_DISPATCH):
        sys.exit(0)

    cwd = input_data.get("cwd") or os.getcwd()
    repo_root = find_repo_root(cwd)
    if not repo_root:
        sys.exit(0)

    task_dir = get_current_task(repo_root)
    if not task_dir:
        sys.exit(0)

    update_current_phase(repo_root, task_dir, subagent_type)

    context = get_context_for_agent(repo_root, task_dir, subagent_type)
    if not context:
        sys.exit(0)

    result = {
        "allow": True,
        "prompt_modifier": context
    }

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
