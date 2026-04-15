# Logging Guidelines

> **To be filled by the team**: Document your project's logging standards and practices.

---

## Overview

**To be filled by the team**: Describe your logging approach.

Questions to answer:
- What logging library/framework is used?
- What log levels are available and when should each be used?
- How are logs structured (plain text, JSON, etc.)?

---

## Log Levels

**To be filled by the team**: Document when to use each log level.

Questions to answer:
- DEBUG: When to use?
- INFO: When to use?
- WARNING: When to use?
- ERROR: When to use?
- CRITICAL: When to use?

---

## What to Log

**To be filled by the team**: Document what information should be logged.

Questions to answer:
- What events should be logged?
- What context should be included in logs?
- What should NOT be logged (e.g., sensitive data)?

---

## Examples

**To be filled by the team**: Provide examples of good logging from your project.

```python
# Example: To be filled by the team
| `log_warn` | stdout | Warnings, degraded functionality |
| `log_error` | stdout | Errors (not stderr, for color consistency) |
| `print(..., file=sys.stderr)` | stderr | Raw errors without formatting |

**Note**: All `log_*` functions print to **stdout** for color consistency. Only use `sys.stderr` for raw/unformatted errors.

---

## Log Level Semantics

### `[INFO]`

General information about script progress. Use for:
- Starting an operation
- Confirming successful completion of a step
- Displaying intermediate results

```python
from common.log import log_info

log_info("Initialized developer: zj669")
```

### `[SUCCESS]`

Operation completed successfully. Use for:
- Final confirmation of a multi-step operation
- Checklist completion markers

```python
from common.log import log_success

log_success("Auto-committed: chore: record journal")
```

### `[WARN]`

Degraded functionality but script can continue. Use for:
- Optional operations that failed
- Missing optional dependencies
- Hook failures (non-blocking)

```python
from common.log import log_warn

log_warn("Hook failed: linear_sync.py — continuing without Linear sync")
```

### `[ERROR]`

Operation failed, script should exit. Use for:
- Missing required files
- Invalid arguments
- Git operations that must succeed

```python
from common.log import log_error

log_error("Not in a bwflow project")
sys.exit(1)
```

---

## Hook Logging

### Task Lifecycle Hooks

Task lifecycle hooks (configured in `config.yaml`) run non-blocking. Log hook failures as warnings:

```python
result = subprocess.run(
    cmd, shell=True, cwd=repo_root, capture_output=True,
    encoding="utf-8", errors="replace"
)
if result.returncode != 0:
    log_warn(f"Hook failed: {cmd}")
    # Continue — don't block main operation
```

### Claude Code Hooks (Python)

Python hooks that output structured JSON should not emit log messages to stdout (which would corrupt JSON output). Use `sys.stderr` for debug output during development:

```python
import sys

# Debug: only in development
print(f"[DEBUG] Loading context from {task_dir}", file=sys.stderr)
```

For production, hooks should be silent (return only structured JSON).

---

## Session Recording

When auto-committing after session recording:

```python
from common.log import log_success, log_warn

# Check if there are staged changes
result = subprocess.run(
    ["git", "diff", "--cached", "--quiet"],
    cwd=repo_root,
)
if result.returncode == 0:
    log_info("No changes to commit")
    return

# Commit
result = subprocess.run(
    ["git", "commit", "-m", commit_message],
    cwd=repo_root, capture_output=True, text=True
)
if result.returncode == 0:
    log_success(f"Auto-committed: {commit_message}")
else:
    log_warn(f"Auto-commit failed: {result.stderr.strip()}")
```

---

## What NOT to Log

- **User input**: Never log raw user input that may contain sensitive data
- **Full stack traces**: Show only the error message, not the traceback
- **Debug output in production hooks**: Keep hooks silent
- **JSON response data**: Hooks return JSON to Claude runtime — no logging

---

## DO / DON'T

### DO

- Use `common/log.py` for all Python script output
- Use `log_info` for progress, `log_success` for completion
- Use `log_warn` for non-blocking failures
- Use `log_error` + `sys.exit(1)` for blocking errors
- Log to stderr only when raw output (not colored) is needed

### DON'T

- Don't use bare `print()` for status messages (use `log_info`)
- Don't log full stack traces to users
- Don't log in Claude Code hooks (they return JSON)
- Don't use color codes directly — use the `colored()` function
- Don't log sensitive user data
