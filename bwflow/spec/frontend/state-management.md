# State Management

> How state is managed in this plugin project.

---

## Overview

This project manages state through files, not in-memory state. The "state" is the current session context, task status, and workspace memory — all persisted to disk.

---

## State Categories

| Category | Storage | Access |
|----------|---------|--------|
| Session context | `bwflow/workspace/{developer}/journal-N.md` | Append-only |
| Task state | `bwflow/tasks/{task-id}/task.json` | Read/write via `common/tasks.py` |
| Agent context | `bwflow/tasks/{task-id}/*.jsonl` | JSONL read via `common/task_context.py` |
| Current task | `bwflow/.current-task` | Plain text, single value |
| Developer identity | `bwflow/.developer` | Plain text, single value |
| Blueprint alignment | `.blueprint/` | Markdown files |

---

## Task State Management

### Python API

```python
from pathlib import Path
from common.tasks import load_task, iter_active_tasks

# Load single task
task = load_task(Path("bwflow/tasks/00-task-name"))
if task:
    status = task.status  # via TaskInfo properties

# Iterate all active tasks
for task_info in iter_active_tasks(Path("bwflow/tasks")):
    print(f"{task_info.dir_name}: {task_info.status}")
```

### State Transitions

```
planning → in_progress → completed → archived
```

Tasks follow a strict lifecycle. Phase advancement is tracked via `current_phase` in `task.json`:

```json
{
  "current_phase": 2,
  "next_action": [
    { "phase": 1, "action": "implement" },
    { "phase": 2, "action": "check" },
    { "phase": 3, "action": "finish" }
  ]
}
```

---

## Agent Context (JSONL)

Context is stored as JSON Lines files, one JSON object per line:

```jsonl
{"file": "bwflow/spec/backend/error-handling.md", "reason": "ErrorHandling"}
{"file": "bwflow/spec/backend/", "type": "directory", "reason": "AllBackendSpecs"}
```

Read via `common/task_context.py`:

```python
from common.task_context import read_jsonl_entries

# Returns list of (file_path, content) tuples
entries = read_jsonl_entries(repo_root, "implement.jsonl")
for file_path, content in entries:
    # Process context file
    pass
```

---

## Blueprint State

Blueprints are file-based. The `align` skill compares code state with blueprint state:

```
blueprint_present: boolean      # Does .blueprint/ exist?
worktreeFiles: []               # Non-blueprint changed files
blueprintFiles: []              # Blueprint changed files
```

---

## No In-Memory State

This project intentionally avoids in-memory state:
- **No singleton stores**: All state is file-based
- **No caching layers**: Always read from disk
- **No event buses**: Scripts are stateless

This makes every operation independently verifiable and recoverable.

---

## Session Memory Pattern

Each session appends to a journal file:

```markdown
## Session: 2026-04-12 14:00

**Task**: Bootstrap Guidelines
**Commit**: b823caa

### Work Done
- Filled backend/error-handling.md
- Filled backend/quality-guidelines.md

### Next Steps
- Fill frontend specs
- Update thinking guides
```

Journal files rotate at 2000 lines via `add_session.py`.

---

## DO / DON'T

### DO

- Use file-based state for all persistence
- Use `common/tasks.py` for task state access
- Use `common/task_context.py` for JSONL context
- Rotate journal files at 2000 lines

### DON'T

- Don't create in-memory state stores
- Don't cache task state between script invocations
- Don't use global variables for state
- Don't store state in temporary files that aren't cleaned up
