#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session Start Hook - Inject structured context for Cursor Agent
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

# =============================================================================
# Path Constants
# =============================================================================

DIR_WORKFLOW = ".bwflow"
DIR_TASKS = "tasks"
FILE_CURRENT_TASK = ".current-task"
FILE_TASK_JSON = "task.json"


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


def run_script(script_path: Path) -> str:
    try:
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        cmd = [sys.executable, "-W", "ignore", str(script_path)]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            cwd=script_path.parent.parent,
            env=env,
        )
        return result.stdout if result.returncode == 0 else "No context available"
    except (subprocess.TimeoutExpired, FileNotFoundError, PermissionError):
        return "No context available"


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
            normalized = f".bwflow/{normalized}"
        return normalized
    except Exception:
        return None


def get_task_status(trellis_dir: Path) -> str:
    """Check current task status"""
    current_task_file = trellis_dir / FILE_CURRENT_TASK
    if not current_task_file.is_file():
        return "Status: NO ACTIVE TASK\nNext: Describe what you want to work on"

    task_ref = read_file(current_task_file, "").strip()
    if not task_ref:
        return "Status: NO ACTIVE TASK\nNext: Describe what you want to work on"

    # Normalize task_ref
    normalized = task_ref.replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    if normalized.startswith("tasks/"):
        normalized = f".bwflow/{normalized}"

    path_obj = Path(normalized)
    if path_obj.is_absolute():
        task_dir = path_obj
    elif normalized.startswith(".bwflow/"):
        task_dir = trellis_dir.parent / path_obj
    else:
        task_dir = trellis_dir / "tasks" / task_ref

    if not task_dir.is_dir():
        return f"Status: STALE POINTER\nTask: {task_ref}\nNext: Task directory not found"

    task_json_path = task_dir / FILE_TASK_JSON
    task_data = {}
    if task_json_path.is_file():
        try:
            task_data = json.loads(task_json_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, PermissionError):
            pass

    task_title = task_data.get("title", task_ref)
    task_status = task_data.get("status", "unknown")

    if task_status == "completed":
        return f"Status: COMPLETED\nTask: {task_title}\nNext: Archive with `python3 .bwflow/scripts/task.py archive {task_dir.name}`"

    has_prd = (task_dir / "prd.md").is_file()
    has_context = any(
        (task_dir / f).is_file() and (task_dir / f).stat().st_size > 0
        for f in ["implement.jsonl", "check.jsonl", "spec.jsonl"]
    )

    if not has_prd:
        return f"Status: NOT READY\nTask: {task_title}\nMissing: prd.md\nNext: Write PRD first"

    if not has_context:
        return f"Status: NOT READY\nTask: {task_title}\nMissing: Context not configured\nNext: Complete research and init-context"

    return f"Status: READY\nTask: {task_title}\nNext: Continue with implement or check"


def main():
    if should_skip_injection():
        sys.exit(0)

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    repo_root = find_repo_root(project_dir) or project_dir
    trellis_dir = Path(repo_root) / DIR_WORKFLOW

    output = StringIO()

    output.write("""<session-context>
You are starting a new session in a bwflow-managed project.
Read and follow all instructions below carefully.
</session-context>

""")

    output.write("<current-state>\n")
    context_script = trellis_dir / "scripts" / "get_context.py"
    if context_script.is_file():
        output.write(run_script(context_script))
    else:
        output.write(get_task_status(trellis_dir))
    output.write("\n</current-state>\n\n")

    output.write("<workflow>\n")
    workflow_content = read_file(trellis_dir / "workflow.md", "No workflow.md found")
    output.write(workflow_content)
    output.write("\n</workflow>\n\n")

    output.write("<guidelines>\n")
    output.write("**Note**: The guidelines below are index files — they list available guideline documents.\n\n")

    spec_dir = trellis_dir / "spec"
    if spec_dir.is_dir():
        for sub in sorted(spec_dir.iterdir()):
            if not sub.is_dir() or sub.name.startswith("."):
                continue

            if sub.name == "guides":
                index_file = sub / "index.md"
                if index_file.is_file():
                    output.write(f"## {sub.name}\n")
                    output.write(read_file(index_file))
                    output.write("\n\n")
                continue

            index_file = sub / "index.md"
            if index_file.is_file():
                output.write(f"## {sub.name}\n")
                output.write(read_file(index_file))
                output.write("\n\n")

    output.write("</guidelines>\n\n")

    output.write("<instructions>\n")
    start_md = read_file(
        Path(repo_root) / ".cursor" / "commands" / "bw" / "start.md", "No start.md found"
    )
    output.write(start_md)
    output.write("\n</instructions>\n\n")

    # Check task status and inject structured tag
    task_status = get_task_status(trellis_dir)
    output.write(f"<task-status>\n{task_status}\n</task-status>\n\n")

    output.write("""<ready>
Context loaded. Steps 1-3 (workflow, context, guidelines) are already injected above — do NOT re-read them.
Start from Step 4. Wait for user's first message, then follow <instructions> to handle their request.
If there is an active task, ask whether to continue it.
</ready>""")

    result = {
        "allow": True,
        "message": output.getvalue()
    }

    print(json.dumps(result, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
