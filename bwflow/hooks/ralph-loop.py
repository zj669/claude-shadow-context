#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ralph Loop - SubagentStop Hook for Check Agent Loop Control

Based on the Ralph Wiggum technique for autonomous agent loops.
Uses completion promises to control when the check agent can stop.

Mechanism:
- Intercepts when check subagent tries to stop (SubagentStop event)
- If verify commands configured in worktree.yaml, runs them to verify
- Otherwise, reads check.jsonl to get dynamic completion markers ({reason}_FINISH)
- Blocks stopping until verification passes or all markers found
- Has max iterations as safety limit

State file: bwflow/.ralph-state.json
"""

# IMPORTANT: Suppress all warnings FIRST
import warnings
warnings.filterwarnings("ignore")

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# IMPORTANT: Force stdout to use UTF-8 on Windows
if sys.platform == "win32":
    import io as _io
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    elif hasattr(sys.stdout, "detach"):
        sys.stdout = _io.TextIOWrapper(sys.stdout.detach(), encoding="utf-8", errors="replace")

# =============================================================================
# Configuration
# =============================================================================

MAX_ITERATIONS = 5
STATE_TIMEOUT_MINUTES = 30
STATE_FILE = "bwflow/.ralph-state.json"
WORKTREE_YAML = "bwflow/worktree.yaml"
DIR_WORKFLOW = "bwflow"
FILE_CURRENT_TASK = ".current-task"
TARGET_AGENT = "check"


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
    current_task_file = os.path.join(repo_root, DIR_WORKFLOW, FILE_CURRENT_TASK)
    if not os.path.exists(current_task_file):
        return None

    try:
        with open(current_task_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
            return content if content else None
    except Exception:
        return None


def get_verify_commands(repo_root: str) -> list[str]:
    """Read verify commands from worktree.yaml."""
    yaml_path = os.path.join(repo_root, WORKTREE_YAML)
    if not os.path.exists(yaml_path):
        return []

    try:
        with open(yaml_path, "r", encoding="utf-8") as f:
            content = f.read()

        lines = content.split("\n")
        in_verify_section = False
        commands = []

        for line in lines:
            stripped = line.strip()

            if stripped.startswith("verify:"):
                in_verify_section = True
                continue

            if (
                not line.startswith(" ")
                and not line.startswith("\t")
                and stripped.endswith(":")
                and stripped != ""
            ):
                in_verify_section = False
                continue

            if in_verify_section:
                if stripped.startswith("#") or stripped == "":
                    continue
                if stripped.startswith("- "):
                    cmd = stripped[2:].strip()
                    if cmd:
                        commands.append(cmd)

        return commands
    except Exception:
        return []


def run_verify_commands(repo_root: str, commands: list[str]) -> tuple[bool, str]:
    """Run verify commands and return (success, message)."""
    for cmd in commands:
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=repo_root,
                capture_output=True,
                timeout=120,
            )
            if result.returncode != 0:
                stderr = result.stderr.decode("utf-8", errors="replace")
                stdout = result.stdout.decode("utf-8", errors="replace")
                error_output = stderr or stdout
                if len(error_output) > 500:
                    error_output = error_output[:500] + "..."
                return False, f"Command failed: {cmd}\n{error_output}"
        except subprocess.TimeoutExpired:
            return False, f"Command timed out: {cmd}"
        except Exception as e:
            return False, f"Command error: {cmd} - {str(e)}"

    return True, "All verify commands passed"


def get_completion_markers(repo_root: str, task_dir: str) -> list[str]:
    """Read check.jsonl and generate completion markers."""
    check_jsonl_path = os.path.join(repo_root, task_dir, "check.jsonl")
    markers = []

    if not os.path.exists(check_jsonl_path):
        return ["ALL_CHECKS_FINISH"]

    try:
        with open(check_jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    item = json.loads(line)
                    reason = item.get("reason", "")
                    if reason:
                        marker = f"{reason.upper().replace(' ', '_')}_FINISH"
                        if marker not in markers:
                            markers.append(marker)
                except json.JSONDecodeError:
                    continue
    except Exception:
        pass

    if not markers:
        markers = ["ALL_CHECKS_FINISH"]

    return markers


def load_state(repo_root: str) -> dict:
    """Load Ralph Loop state from file"""
    state_path = os.path.join(repo_root, STATE_FILE)
    if not os.path.exists(state_path):
        return {"task": None, "iteration": 0, "started_at": None}

    try:
        with open(state_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"task": None, "iteration": 0, "started_at": None}


def save_state(repo_root: str, state: dict) -> None:
    """Save Ralph Loop state to file"""
    state_path = os.path.join(repo_root, STATE_FILE)
    try:
        os.makedirs(os.path.dirname(state_path), exist_ok=True)
        with open(state_path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


def check_completion(agent_output: str, markers: list[str]) -> tuple[bool, list[str]]:
    """Check if all completion markers are present in agent output."""
    missing = []
    for marker in markers:
        if marker not in agent_output:
            missing.append(marker)

    return len(missing) == 0, missing


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    hook_event = input_data.get("hook_event_name", "")
    if hook_event != "SubagentStop":
        sys.exit(0)

    subagent_type = input_data.get("subagent_type", "")
    agent_output = input_data.get("agent_output", "")
    original_prompt = input_data.get("prompt", "")
    cwd = input_data.get("cwd", os.getcwd())

    if subagent_type != TARGET_AGENT:
        sys.exit(0)

    if "[finish]" in original_prompt.lower():
        sys.exit(0)

    repo_root = find_repo_root(cwd)
    if not repo_root:
        sys.exit(0)

    task_dir = get_current_task(repo_root)
    if not task_dir:
        sys.exit(0)

    state = load_state(repo_root)

    should_reset = False
    if state.get("task") != task_dir:
        should_reset = True
    elif state.get("started_at"):
        try:
            started = datetime.fromisoformat(state["started_at"])
            if (datetime.now() - started).total_seconds() > STATE_TIMEOUT_MINUTES * 60:
                should_reset = True
        except (ValueError, TypeError):
            should_reset = True

    if should_reset:
        state = {
            "task": task_dir,
            "iteration": 0,
            "started_at": datetime.now().isoformat(),
        }

    state["iteration"] = state.get("iteration", 0) + 1
    current_iteration = state["iteration"]

    save_state(repo_root, state)

    if current_iteration >= MAX_ITERATIONS:
        state["iteration"] = 0
        save_state(repo_root, state)
        output = {
            "decision": "allow",
            "reason": f"Max iterations ({MAX_ITERATIONS}) reached.",
        }
        print(json.dumps(output, ensure_ascii=False))
        sys.exit(0)

    verify_commands = get_verify_commands(repo_root)

    if verify_commands:
        passed, message = run_verify_commands(repo_root, verify_commands)

        if passed:
            state["iteration"] = 0
            save_state(repo_root, state)
            output = {"decision": "allow", "reason": "All verify commands passed."}
            print(json.dumps(output, ensure_ascii=False))
            sys.exit(0)
        else:
            output = {
                "decision": "block",
                "reason": f"Iteration {current_iteration}/{MAX_ITERATIONS}. Verification failed:\n{message}\n\nPlease fix the issues and try again.",
            }
            print(json.dumps(output, ensure_ascii=False))
            sys.exit(0)
    else:
        markers = get_completion_markers(repo_root, task_dir)
        all_complete, missing = check_completion(agent_output, markers)

        if all_complete:
            state["iteration"] = 0
            save_state(repo_root, state)
            output = {"decision": "allow", "reason": "All completion markers found."}
            print(json.dumps(output, ensure_ascii=False))
            sys.exit(0)
        else:
            output = {
                "decision": "block",
                "reason": f"Iteration {current_iteration}/{MAX_ITERATIONS}. Missing markers: {missing}\n\nContinue fixing the issues.",
            }
            print(json.dumps(output, ensure_ascii=False))
            sys.exit(0)


if __name__ == "__main__":
    main()
