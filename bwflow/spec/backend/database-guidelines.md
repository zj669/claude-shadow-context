# Database Guidelines

> **To be filled by the team**: Document your project's database or state management approach.

---

## Overview

**To be filled by the team**: Describe how your project manages persistent state.

Questions to answer:
- What database system does your project use? (PostgreSQL, MySQL, MongoDB, SQLite, file-based, etc.)
- What ORM or query library is used? (SQLAlchemy, Prisma, raw SQL, etc.)
- How is database access organized? (repository pattern, direct queries, etc.)

---

## Schema Management

**To be filled by the team**: Document how database schema is managed.

Questions to answer:
- How are migrations created and applied?
- What naming conventions are used for tables and columns?
- How are schema changes reviewed and deployed?

---

## Query Patterns

**To be filled by the team**: Document common query patterns and best practices.

Questions to answer:
- What patterns should be used for common operations (CRUD, pagination, filtering)?
- How should transactions be handled?
- What are the performance considerations?

---

## Examples

**To be filled by the team**: Provide examples of well-written database code from your project.

```python
# Example: To be filled by the team
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
