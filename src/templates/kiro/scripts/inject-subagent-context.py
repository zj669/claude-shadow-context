#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-Agent Pipeline Context Injection Hook

Core Design Philosophy:
- Dispatch becomes a pure dispatcher, only responsible for "calling subagents"
- Hook is responsible for injecting all context, subagent works autonomously with complete info
- Each agent has a dedicated jsonl file defining its context
- No resume needed, no segmentation, behavior controlled by code not prompt

Trigger: PreToolUse (before Task tool call)

Context Source: .bwflow/.current-task points to task directory
- implement.jsonl - Implement agent dedicated context
- check.jsonl     - Check agent dedicated context
- debug.jsonl     - Debug agent dedicated context
- research.jsonl  - Research agent dedicated context (optional, usually not needed)
- cr.jsonl        - Code review dedicated context
- prd.md          - Requirements document
- info.md         - Technical design
- codex-review-output.txt - Code Review results
"""

# IMPORTANT: Suppress all warnings FIRST
import warnings
warnings.filterwarnings("ignore")

import json
import os
import sys
from pathlib import Path

# IMPORTANT: Force stdout to use UTF-8 on Windows
# This fixes UnicodeEncodeError when outputting non-ASCII characters
if sys.platform == "win32":
    import io as _io
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    elif hasattr(sys.stdout, "detach"):
        sys.stdout = _io.TextIOWrapper(sys.stdout.detach(), encoding="utf-8", errors="replace")  # type: ignore[union-attr]

# =============================================================================
# Path Constants (change here to rename directories)
# =============================================================================

DIR_WORKFLOW = ".bwflow"
DIR_WORKSPACE = "workspace"
DIR_TASKS = "tasks"
DIR_SPEC = "spec"
FILE_CURRENT_TASK = ".current-task"
FILE_TASK_JSON = "task.json"

# Agents that don't update phase (can be called at any time)
AGENTS_NO_PHASE_UPDATE = {"debug", "research"}

# =============================================================================
# Subagent Constants (change here to rename subagent types)
# =============================================================================

AGENT_IMPLEMENT = "implement"
AGENT_CHECK = "check"
AGENT_DEBUG = "debug"
AGENT_RESEARCH = "research"

# Agents that require a task directory
AGENTS_REQUIRE_TASK = (AGENT_IMPLEMENT, AGENT_CHECK, AGENT_DEBUG)
# All supported agents
AGENTS_ALL = (AGENT_IMPLEMENT, AGENT_CHECK, AGENT_DEBUG, AGENT_RESEARCH)


def find_repo_root(start_path: str) -> str | None:
    """
    Find git repo root from start_path upwards

    Returns:
        Repo root path, or None if not found
    """
    current = Path(start_path).resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return str(current)
        current = current.parent
    return None


def get_current_task(repo_root: str) -> str | None:
    """
    Read current task directory path from .bwflow/.current-task

    Returns:
        Task directory relative path (relative to repo_root)
        None if not set
    """
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
            if normalized.startswith("tasks/"):
                normalized = f".bwflow/{normalized}"
            return normalized
    except Exception:
        return None


def update_current_phase(repo_root: str, task_dir: str, subagent_type: str) -> None:
    """
    Update current_phase in task.json based on subagent_type.

    This ensures phase tracking is always accurate, regardless of whether
    dispatch agent remembers to update it.

    Logic:
    - Read next_action array from task.json
    - Find the next phase whose action matches subagent_type
    - Only move forward, never backward
    - Some agents (debug, research) don't update phase
    """
    if subagent_type in AGENTS_NO_PHASE_UPDATE:
        return

    task_json_path = os.path.join(repo_root, task_dir, FILE_TASK_JSON)
    if not os.path.exists(task_json_path):
        return

    try:
        with open(task_json_path, "r", encoding="utf-8") as f:
            task_data = json.load(f)

        current_phase = task_data.get("current_phase", 0)
        next_actions = task_data.get("next_action", [])

        # Map action names to subagent types
        # "implement" -> "implement", "check" -> "check", "finish" -> "check"
        action_to_agent = {
            "implement": "implement",
            "check": "check",
            "finish": "check",  # finish uses check agent
        }

        # Find the next phase that matches this subagent_type
        new_phase = None
        for action in next_actions:
            phase_num = action.get("phase", 0)
            action_name = action.get("action", "")
            expected_agent = action_to_agent.get(action_name)

            # Only consider phases after current_phase
            if phase_num > current_phase and expected_agent == subagent_type:
                new_phase = phase_num
                break

        if new_phase is not None:
            task_data["current_phase"] = new_phase

            with open(task_json_path, "w", encoding="utf-8") as f:
                json.dump(task_data, f, indent=2, ensure_ascii=False)
    except Exception:
        # Don't fail the hook if phase update fails
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
    """
    Read all .md files in a directory

    Args:
        base_path: Base path (usually repo_root)
        dir_path: Directory relative path
        max_files: Max files to read (prevent huge directories)

    Returns:
        [(file_path, content), ...]
    """
    full_path = os.path.join(base_path, dir_path)
    if not os.path.exists(full_path) or not os.path.isdir(full_path):
        return []

    results = []
    try:
        # Only read .md files, sorted by filename
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
    """
    Read all file/directory contents referenced in jsonl file

    Schema:
        {"file": "path/to/file.md", "reason": "..."}
        {"file": "path/to/dir/", "type": "directory", "reason": "..."}

    Returns:
        [(path, content), ...]
    """
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
                        # Read all .md files in directory
                        dir_contents = read_directory_contents(base_path, file_path)
                        results.extend(dir_contents)
                    else:
                        # Read single file
                        content = read_file_content(base_path, file_path)
                        if content:
                            results.append((file_path, content))
                except json.JSONDecodeError:
                    continue
    except Exception:
        pass

    return results


def get_agent_context(repo_root: str, task_dir: str, agent_type: str) -> str:
    """
    Get complete context for specified agent

    Prioritize agent-specific jsonl, fallback to spec.jsonl if not exists
    """
    context_parts = []

    # 1. Try agent-specific jsonl
    agent_jsonl = f"{task_dir}/{agent_type}.jsonl"
    agent_entries = read_jsonl_entries(repo_root, agent_jsonl)

    # 2. If agent-specific jsonl doesn't exist or empty, fallback to spec.jsonl
    if not agent_entries:
        agent_entries = read_jsonl_entries(repo_root, f"{task_dir}/spec.jsonl")

    # 3. Add all files from jsonl
    for file_path, content in agent_entries:
        context_parts.append(f"=== {file_path} ===\n{content}")

    return "\n\n".join(context_parts)


def get_implement_context(repo_root: str, task_dir: str) -> str:
    """
    Complete context for Implement Agent

    Read order:
    1. All files in implement.jsonl (dev specs)
    2. prd.md (requirements)
    3. info.md (technical design)
    """
    context_parts = []

    # 1. Read implement.jsonl (or fallback to spec.jsonl)
    base_context = get_agent_context(repo_root, task_dir, "implement")
    if base_context:
        context_parts.append(base_context)

    # 2. Requirements document
    prd_content = read_file_content(repo_root, f"{task_dir}/prd.md")
    if prd_content:
        context_parts.append(f"=== {task_dir}/prd.md (Requirements) ===\n{prd_content}")

    # 3. Technical design
    info_content = read_file_content(repo_root, f"{task_dir}/info.md")
    if info_content:
        context_parts.append(
            f"=== {task_dir}/info.md (Technical Design) ===\n{info_content}"
        )

    return "\n\n".join(context_parts)


def get_check_context(repo_root: str, task_dir: str) -> str:
    """
    Complete context for Check Agent

    Read order:
    1. All files in check.jsonl (check specs + dev specs)
    2. prd.md (for understanding task intent)
    """
    context_parts = []

    # 1. Read check.jsonl (or fallback to spec.jsonl + hardcoded check files)
    check_entries = read_jsonl_entries(repo_root, f"{task_dir}/check.jsonl")

    if check_entries:
        for file_path, content in check_entries:
            context_parts.append(f"=== {file_path} ===\n{content}")
    else:
        # Fallback: use hardcoded check files + spec.jsonl
        check_files = [
            (".claude/commands/bwflow/finish-work/finish-work.CMD.md", "Finish work checklist"),
            (".claude/commands/bwflow/check/check.CMD.md", "Code quality check spec"),
        ]
        for file_path, description in check_files:
            content = read_file_content(repo_root, file_path)
            if content:
                context_parts.append(f"=== {file_path} ({description}) ===\n{content}")

        # Add spec.jsonl
        spec_entries = read_jsonl_entries(repo_root, f"{task_dir}/spec.jsonl")
        for file_path, content in spec_entries:
            context_parts.append(f"=== {file_path} ===\n{content}")

    prd_content = read_file_content(repo_root, f"{task_dir}/prd.md")
    if prd_content:
        context_parts.append(f"=== {task_dir}/prd.md (Requirements) ===\n{prd_content}")

    return "\n\n".join(context_parts)


def get_debug_context(repo_root: str, task_dir: str) -> str:
    """Complete context for Debug Agent"""
    context_parts = []

    debug_entries = read_jsonl_entries(repo_root, f"{task_dir}/debug.jsonl")
    for file_path, content in debug_entries:
        context_parts.append(f"=== {file_path} ===\n{content}")

    return "\n\n".join(context_parts)


def get_research_context(repo_root: str, task_dir: str) -> str:
    """Complete context for Research Agent"""
    context_parts = []

    research_entries = read_jsonl_entries(repo_root, f"{task_dir}/research.jsonl")
    for file_path, content in research_entries:
        context_parts.append(f"=== {file_path} ===\n{content}")

    prd_content = read_file_content(repo_root, f"{task_dir}/prd.md")
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
        return get_debug_context(repo_root, task_dir)
    else:
        return get_implement_context(repo_root, task_dir)


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    # Get hook configuration
    hook_name = input_data.get("hook_name", "")
    hook_full_name = input_data.get("hook_full_name", "")

    # Get subagent type from arguments
    # Claude Code uses "subagent_type" in Task tool arguments
    tool_args = input_data.get("args") or {}
    subagent_type = (
        tool_args.get("subagent_type", "")
        or tool_args.get("name", "")
        or tool_args.get("type", "")
    )

    # Get cwd from environment or input
    cwd = os.environ.get("CLAUDE_PROJECT_DIR") or input_data.get("cwd") or os.getcwd()

    # Only handle Task tool with valid subagent type
    if tool_args.get("tool", "") != "Task":
        sys.exit(0)

    if not subagent_type or subagent_type not in AGENTS_ALL:
        sys.exit(0)

    # Find repo root
    repo_root = find_repo_root(cwd)
    if not repo_root:
        sys.exit(0)

    # Get current task
    task_dir = get_current_task(repo_root)
    if not task_dir:
        # No active task, allow but don't inject context
        sys.exit(0)

    # Update phase
    update_current_phase(repo_root, task_dir, subagent_type)

    # Get context
    context = get_context_for_agent(repo_root, task_dir, subagent_type)
    if not context:
        sys.exit(0)

    # For Claude Code, we output a JSON with the context to prepend
    # Claude Code will prepend this to the subagent prompt
    result = {
        "subagent_prompt_prepend": context
    }
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
