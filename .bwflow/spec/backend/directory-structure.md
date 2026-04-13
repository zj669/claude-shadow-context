# Directory Structure

> How Python scripts are organized in this project.

---

## Overview

This project is a **Claude Code plugin** with hybrid architecture:
- **Python** for bwflow workflow scripts and Claude hooks (`.bwflow/scripts/`, `.claude/hooks/`)
- **JavaScript (ESM)** for plugin logic (`scripts/`, `skills/`)

---

## Directory Layout

```
.claude/hooks/              # Python Claude Code hooks
│   ├── session-start.py          # Session start: inject workflow context
│   ├── inject-subagent-context.py # PreToolUse: inject agent-specific context
│   └── ralph-loop.py             # SubagentStop: quality gate loop
│
.bwflow/scripts/          # Python bwflow workflow scripts
│   ├── __init__.py               # Package init (UTF-8 encoding fix)
│   ├── common/                   # Shared modules
│   │   ├── __init__.py           # UTF-8 stdin/stdout/stderr fix
│   │   ├── paths.py              # Path constants (DIR_WORKFLOW, etc.)
│   │   ├── developer.py          # Developer identity
│   │   ├── git_context.py        # Git context extraction
│   │   ├── io.py                 # read_json / write_json
│   │   ├── log.py                # Colors class + log_info/log_error
│   │   ├── tasks.py              # Task CRUD (load_task, iter_active_tasks)
│   │   ├── task_store.py         # Task persistence
│   │   ├── task_context.py       # JSONL context management
│   │   ├── task_queue.py         # Task queue
│   │   ├── task_utils.py         # resolve_task_dir, run_task_hooks
│   │   ├── phase.py              # Phase tracking
│   │   ├── config.py             # Config reader
│   │   ├── worktree.py           # Git worktree + YAML
│   │   ├── registry.py           # Agent registry
│   │   ├── cli_adapter.py        # Multi-platform CLI
│   │   ├── session_context.py    # Session context generation
│   │   └── packages_context.py   # Package discovery
│   ├── hooks/                    # Lifecycle hook scripts (project-specific)
│   │   └── linear_sync.py        # Linear issue sync (example)
│   ├── multi_agent/              # Multi-agent pipeline scripts
│   │   ├── __init__.py
│   │   ├── start.py              # Start worktree agent
│   │   ├── status.py             # Agent status monitoring
│   │   ├── status_display.py     # Status formatting
│   │   ├── status_monitor.py     # Log parsing
│   │   ├── plan.py               # Start plan agent
│   │   ├── cleanup.py            # Worktree cleanup
│   │   └── create_pr.py          # Create PR
│   ├── task.py                   # Entry shim → task_store + task_context
│   ├── get_context.py            # Session context retrieval
│   ├── init_developer.py         # Developer initialization
│   ├── get_developer.py          # Get current developer
│   └── add_session.py            # Session recording
│
scripts/                   # JavaScript plugin scripts (ESM)
│   ├── session-align.mjs         # Blueprint alignment on session end
│   ├── session-align.test.mjs    # Tests
│   └── mcp-server.test.cjs       # MCP server tests (placeholder)
│
skills/                    # Claude Code skills (slash commands)
│   ├── init/                     # Blueprint layer initialization
│   │   └── SKILL.md
│   ├── explore/                  # Blueprint-first exploration
│   │   └── SKILL.md
│   └── align/                    # Blueprint alignment check
│       └── SKILL.md
│
hooks/                     # Plugin hooks definition
│   └── hooks.json                # SessionEnd hook (legacy, in use)
│
.blueprint/                 # Blueprint layer (intention layer)
│   ├── README.md                # Root blueprint
│   └── ...                      # Module-level blueprints
```

---

## Layer Responsibilities

| Layer | Directory | Technology | Responsibility |
|-------|-----------|------------|-----------------|
| Claude Hooks | `.claude/hooks/` | Python 3.10+ | Context injection at Claude runtime events |
| bwflow Scripts | `bwflow/scripts/` | Python 3.10+ | Workflow automation, task management |
| Plugin Logic | `scripts/` | Node.js ESM | Blueprint alignment, session management |
| Skill Definitions | `skills/` | Markdown | Slash command protocols |
| Blueprint Layer | `.blueprint/` | Markdown | Intent layer for project understanding |

---

## Naming Conventions

### Python Scripts

| Pattern | Example | Usage |
|---------|---------|-------|
| `kebab-case.py` | `task_store.py` | All Python files |
| `kebab-case/` | `multi_agent/` | All Python packages |
| `_bootstrap.py` | `multi_agent/_bootstrap.py` | sys.path shim (adds parent to path) |

### JavaScript Scripts

| Pattern | Example | Usage |
|---------|---------|-------|
| `kebab-case.mjs` | `session-align.mjs` | ESM scripts |
| `kebab-case.test.mjs` | `session-align.test.mjs` | ESM test files |

### Skill Definitions

| Pattern | Example | Usage |
|---------|---------|-------|
| `kebab-case/SKILL.md` | `explore/SKILL.md` | Skill directory + definition |

---

## Module Organization

### Python: Entry Shim Pattern

Scripts that grow too large (>300 lines) are split into focused modules. The original filename becomes a thin dispatcher:

```python
# task.py — entry shim (argparse + dispatch only)
from __future__ import annotations

import argparse
import sys

from common.task_store import cmd_create, cmd_archive   # CRUD operations
from common.task_context import cmd_init_context         # JSONL management

def main() -> int:
    parser = argparse.ArgumentParser(...)
    args = parser.parse_args()
    if args.command == "create":
        return cmd_create(args)
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

### Python: Lazy Import for Circular Dependencies

```python
# status_display.py
def cmd_summary(repo_root: Path, filter_assignee: str | None = None) -> int:
    # Lazy import at call time to avoid circular dependency
    from .status_monitor import get_last_tool, get_last_message
    # ... use get_last_tool, get_last_message
```

### JavaScript: ESM with Named Exports

```javascript
// session-align.mjs
export { buildSummary, collectWorkspaceStatus, main, parseGitStatus };

// Internal: named imports
import { readFileSync } from 'node:fs';
```

---

## Cross-Platform Compatibility

### Python: UTF-8 Encoding (CRITICAL)

On Windows, Python's stdout/stdin default to the system code page (GBK/CP936). This causes:
- `UnicodeEncodeError` when printing non-ASCII characters
- `UnicodeDecodeError` when reading piped UTF-8 content

**Solution**: Centralize in `common/__init__.py`:

```python
# common/__init__.py
import io, sys

def _configure_stream(stream):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="replace")
        return stream
    elif hasattr(stream, "detach"):
        return io.TextIOWrapper(stream.detach(), encoding="utf-8", errors="replace")
    return stream

if sys.platform == "win32":
    sys.stdout = _configure_stream(sys.stdout)
    sys.stderr = _configure_stream(sys.stderr)
    sys.stdin = _configure_stream(sys.stdin)
```

All scripts that `from common import ...` automatically get the fix.

### Always Use `python3` Explicitly

Windows does not support shebang (`#!/usr/bin/env python3`). Document invocation with explicit `python3`:

```python
# In docstrings
"""
Usage:
    python3 task.py create "My Task"
    python3 ./bwflow/scripts/init_developer.py <name>
"""
```

---

## DO / DON'T

### DO

- Use `pathlib.Path` for all Python path operations
- Use type hints (Python 3.10+ syntax: `list[str]`, `dict | None`)
- Use `encoding="utf-8"` for all file operations
- Return exit codes from `main()`
- Print errors to stderr
- Use `python3` in all documentation

### DON'T

- Don't use string path concatenation (`path + "/" + name`)
- Don't use `os.path` when `pathlib` works
- Don't hardcode paths — use constants from `common/paths.py`
- Don't use external dependencies in `bwflow/scripts/` (stdlib only)
