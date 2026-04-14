# Backend Development Guidelines

> Best practices for Python scripts and JavaScript modules in this Claude Code plugin.

---

## Overview

This directory contains guidelines for backend (script) development in this project. Since this is a **Claude Code plugin** rather than a traditional backend service, "backend" here refers to:

- **Python scripts**: bwflow workflow scripts (`.bwflow/scripts/`) and Claude hooks (`.claude/hooks/`)
- **JavaScript modules**: Plugin scripts (`scripts/`)

---

## Guidelines Index

| Guide | Description | Status |
|-------|-------------|--------|
| [Directory Structure](./directory-structure.md) | Module organization and file layout | ✅ Filled |
| [Database Guidelines](./database-guidelines.md) | File-based state management (no DB) | ✅ Filled |
| [Error Handling](./error-handling.md) | Python + JavaScript error patterns | ✅ Filled |
| [Quality Guidelines](./quality-guidelines.md) | Type hints, imports, path handling | ✅ Filled |
| [Logging Guidelines](./logging-guidelines.md) | `common/log.py` usage, log levels | ✅ Filled |

---

## Technology Stack

| Layer | Technology | Standard |
|-------|-----------|----------|
| bwflow Scripts | Python 3.10+ | stdlib only |
| Claude Hooks | Python 3.10+ | stdlib only |
| Plugin Scripts | Node.js ESM | JSDoc annotations |
| Blueprint Layer | Markdown | Three-section template |

---

## Key Conventions

1. **Python**: Use `pathlib.Path`, type hints, `encoding="utf-8"`
2. **JavaScript**: Use `node:` prefix, named exports, fail-closed hooks
3. **State**: File-based (JSON + Markdown), no database
4. **Context**: JSONL files for agent context injection

---

## Pre-Development Checklist

Before writing Python or JavaScript code:

- [ ] Read [directory-structure.md](./directory-structure.md)
- [ ] Read [error-handling.md](./error-handling.md)
- [ ] Read [quality-guidelines.md](./quality-guidelines.md)
- [ ] For logging: read [logging-guidelines.md](./logging-guidelines.md)
- [ ] For task/state management: read [database-guidelines.md](./database-guidelines.md)
