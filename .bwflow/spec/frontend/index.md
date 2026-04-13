# Frontend Development Guidelines

> Best practices for JavaScript modules and Claude Code skills in this plugin.

---

## Overview

This directory contains guidelines for frontend (JavaScript + skills) development. Since this is a **Claude Code plugin** rather than a traditional frontend app, "frontend" here refers to:

- **JavaScript modules**: ESM scripts in `scripts/`
- **Claude Code skills**: Slash command protocols in `skills/`
- **Hook configurations**: Runtime wiring

---

## Guidelines Index

| Guide | Description | Status |
|-------|-------------|--------|
| [Directory Structure](./directory-structure.md) | Module organization and file layout | ✅ Filled |
| [Component Guidelines](./component-guidelines.md) | JavaScript module patterns | ✅ Filled |
| [Hook Guidelines](./hook-guidelines.md) | Claude Code hook architecture | ✅ Filled |
| [State Management](./state-management.md) | File-based state patterns | ✅ Filled |
| [Quality Guidelines](./quality-guidelines.md) | ESM, JSDoc, error handling | ✅ Filled |
| [Type Safety](./type-safety.md) | JSDoc annotations, type guards | ✅ Filled |

---

## Technology Stack

| Component | Technology | Standard |
|-----------|-----------|----------|
| Plugin Scripts | Node.js ESM | JSDoc annotations |
| Hook Configuration | JSON | `hooks/hooks.json` |
| Skills | Markdown | YAML frontmatter + content |
| Testing | Vitest | `*.test.mjs` |

---

## Pre-Development Checklist

Before writing JavaScript code:

- [ ] Read [directory-structure.md](./directory-structure.md)
- [ ] Read [component-guidelines.md](./component-guidelines.md)
- [ ] Read [hook-guidelines.md](./hook-guidelines.md)
- [ ] Read [type-safety.md](./type-safety.md)
- [ ] For state: read [state-management.md](./state-management.md)
