# Database Guidelines

> This project does not use a traditional database.

---

## Overview

`claude-shadow-context` is a Claude Code plugin that manages project context through file-based storage. All persistence uses JSON files and Markdown documents versioned in Git.

---

## File-Based State Management

| Data Type | Storage | Format |
|-----------|---------|--------|
| Task state | `.bwflow/tasks/{task-id}/task.json` | JSON |
| Agent context | `.bwflow/tasks/{task-id}/*.jsonl` | JSON Lines |
| Session memory | `.bwflow/workspace/{developer}/journal-N.md` | Markdown |
| Blueprint layer | `.blueprint/` | Markdown |
| Developer identity | `.bwflow/.developer` | Plain text |
| Current task | `.bwflow/.current-task` | Plain text |

---

## Task JSON Schema

Tasks are stored as individual JSON files:

```json
{
  "title": "Task Title",
  "status": "in_progress",
  "created": "2026-04-12",
  "description": "Task description",
  "branch": "feat/task-name",
  "current_phase": 1,
  "next_action": [
    { "phase": 1, "action": "implement" },
    { "phase": 2, "action": "check" },
    { "phase": 3, "action": "finish" }
  ],
  "assignee": "zj669",
  "priority": "P1"
}
```

### Read-Write Pattern

```python
from pathlib import Path
import json

def load_task(task_dir: Path) -> dict | None:
    task_json = task_dir / "task.json"
    try:
        return json.loads(task_json.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def save_task(task_dir: Path, data: dict) -> bool:
    task_json = task_dir / "task.json"
    try:
        task_json.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
        return True
    except OSError:
        return False
```

---

## JSONL Context Files

Agent context is stored as JSON Lines (one JSON object per line):

```jsonl
{"file": "bwflow/spec/backend/error-handling.md", "reason": "ErrorHandling"}
{"file": "bwflow/spec/backend/", "type": "directory", "reason": "AllBackendSpecs"}
```

Schema:
- `file`: Relative path to context file
- `reason`: Why this file is included
- `type`: `"file"` (default) or `"directory"` (read all .md files)

---

## Blueprint Files

Blueprints follow a three-section template stored as Markdown:

```markdown
# {filename} 蓝图

## Metadata
- title: 蓝图标题
- type: 类型标识 (class | module | service | controller | util)
- summary: 一句话描述

## 关键方法单元
- location: 代码位置 (类名.方法名 或 函数名)
- purpose: 方法目的，解决什么问题
- input: 参数类型和说明
- output: 返回值类型和说明
- core_steps: 核心步骤列表

## 变更记录
- YYYY-MM-DD: 变更摘要
```

Path mapping: `src/foo/bar.js` → `.blueprint/foo/bar.md`

---

## Data Integrity

- All state is Git-versioned (easy rollback, PR review)
- Key paths centralized in `common/paths.py`
- UTF-8 encoding on all reads/writes
- Silent failure for optional reads, boolean returns for writes

---

## Why No Database

1. **Lightweight**: No database server to install or maintain
2. **Git-native**: All state is versioned, branchable, reviewable
3. **Portable**: Works across all platforms without configuration
4. **Simple backup**: Just `git clone` everything

If you need to add persistence, prefer file-based JSON storage with the patterns above.
