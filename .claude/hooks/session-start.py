#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session Start Hook - Inject structured context for bwflow
"""

# IMPORTANT: Suppress all warnings FIRST
import warnings
warnings.filterwarnings("ignore")

import json
import os
import subprocess
import sys
from io import StringIO
from pathlib import Path

# IMPORTANT: Force stdout to use UTF-8 on Windows
if sys.platform == "win32":
    import io as _io
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    elif hasattr(sys.stdout, "detach"):
        sys.stdout = _io.TextIOWrapper(sys.stdout.detach(), encoding="utf-8", errors="replace")


def should_skip_injection() -> bool:
    return (
        os.environ.get("CLAUDE_NON_INTERACTIVE") == "1"
        or os.environ.get("OPENCODE_NON_INTERACTIVE") == "1"
    )


def read_file(path: Path, fallback: str = "") -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (FileNotFoundError, PermissionError):
        return fallback


def run_script(script_path: Path, cwd: Path) -> str:
    try:
        if script_path.suffix == ".py":
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            cmd = [sys.executable, "-W", "ignore", str(script_path)]
        else:
            env = os.environ
            cmd = [str(script_path)]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
            cwd=cwd,
            env=env,
        )
        return result.stdout if result.returncode == 0 else "No context available"
    except (subprocess.TimeoutExpired, FileNotFoundError, PermissionError):
        return "No context available"


def _get_task_status(bwflow_dir: Path) -> str:
    """Check current task status and return structured status string."""
    current_task_file = bwflow_dir / ".current-task"
    if not current_task_file.is_file():
        return "Status: NO ACTIVE TASK\nNext: Describe what you want to work on"

    task_ref = current_task_file.read_text(encoding="utf-8").strip()
    if not task_ref:
        return "Status: NO ACTIVE TASK\nNext: Describe what you want to work on"

    # Resolve task directory
    if Path(task_ref).is_absolute():
        task_dir = Path(task_ref)
    elif task_ref.startswith("bwflow/"):
        task_dir = bwflow_dir.parent / task_ref
    else:
        task_dir = bwflow_dir / "tasks" / task_ref
    if not task_dir.is_dir():
        return f"Status: STALE POINTER\nTask: {task_ref}\nNext: Task directory not found. Run: python3 ./bwflow/scripts/task.py finish"

    # Read task.json
    task_json_path = task_dir / "task.json"
    task_data = {}
    if task_json_path.is_file():
        try:
            task_data = json.loads(task_json_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, PermissionError):
            pass

    task_title = task_data.get("title", task_ref)
    task_status = task_data.get("status", "unknown")

    if task_status == "completed":
        return f"Status: COMPLETED\nTask: {task_title}\nNext: Archive with `python3 ./bwflow/scripts/task.py archive {task_dir.name}` or start a new task"

    # Check if context is configured (jsonl files exist and non-empty)
    has_context = False
    for jsonl_name in ("implement.jsonl", "check.jsonl", "spec.jsonl"):
        jsonl_path = task_dir / jsonl_name
        if jsonl_path.is_file() and jsonl_path.stat().st_size > 0:
            has_context = True
            break

    has_prd = (task_dir / "prd.md").is_file()

    if not has_prd:
        return f"Status: NOT READY\nTask: {task_title}\nMissing: prd.md not created\nNext: Write PRD, then research → init-context → start"

    if not has_context:
        return f"Status: NOT READY\nTask: {task_title}\nMissing: Context not configured (no jsonl files)\nNext: Complete Phase 2 (research → init-context → start) before implementing"

    return f"Status: READY\nTask: {task_title}\nNext: Continue with implement or check"


def main():
    if should_skip_injection():
        sys.exit(0)

    project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")).resolve()
    bwflow_dir = project_dir / "bwflow"
    claude_dir = project_dir / ".claude"

    output = StringIO()

    output.write("""<session-context>
You are starting a new session in a bwflow-managed project.
Read and follow all instructions below carefully.
</session-context>

""")

    output.write("<current-state>\n")
    context_script = bwflow_dir / "scripts" / "get_context.py"
    output.write(run_script(context_script, bwflow_dir))
    output.write("\n</current-state>\n\n")

    output.write("<workflow>\n")
    workflow_content = read_file(bwflow_dir / "workflow.md", "No workflow.md found")
    output.write(workflow_content)
    output.write("\n</workflow>\n\n")

    output.write("<blueprint>\n")
    blueprint_content = read_file(bwflow_dir / "blueprint" / "README.md", "No blueprint/README.md found")
    output.write(blueprint_content)
    output.write("\n</blueprint>\n\n")

    output.write("<guidelines>\n")
    output.write("**Note**: The guidelines below are index files — they list available guideline documents and their locations.\n")
    output.write("During actual development, you MUST read the specific guideline files listed in each index's Pre-Development Checklist.\n\n")

    spec_dir = bwflow_dir / "spec"
    if spec_dir.is_dir():
        for sub in sorted(spec_dir.iterdir()):
            if not sub.is_dir() or sub.name.startswith("."):
                continue
            index_file = sub / "index.md"
            if index_file.is_file():
                output.write(f"## {sub.name}\n")
                output.write(read_file(index_file))
                output.write("\n\n")

    output.write("</guidelines>\n\n")

    output.write("<instructions>\n")
    start_md = read_file(
        claude_dir / "commands" / "bwflow" / "start" / "CMD.md", "No start CMD.md found"
    )
    output.write(start_md)
    output.write("\n</instructions>\n\n")

    # Check task status and inject structured tag
    task_status = _get_task_status(bwflow_dir)
    output.write(f"<task-status>\n{task_status}\n</task-status>\n\n")

    output.write("""<ready>
Context loaded. Steps 1-3 (workflow, context, guidelines) are already injected above — do NOT re-read them.
Start from Step 4. Wait for user's first message, then follow <instructions> to handle their request.
If there is an active task, ask whether to continue it.
</ready>""")

    result = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": output.getvalue(),
        }
    }

    print(json.dumps(result, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
