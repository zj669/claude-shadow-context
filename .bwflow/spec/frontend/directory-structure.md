# Directory Structure

> How JavaScript scripts and Claude Code skills are organized.

---

## Overview

This project is a **Claude Code plugin** written in JavaScript (ESM). The "frontend" layer consists of:
- **Plugin scripts** (`scripts/`): ESM modules for session management
- **Claude Code skills** (`skills/`): Slash command definitions
- **Hook configurations** (`hooks/`, `.claude/`): Runtime wiring

---

## Directory Layout

```
scripts/                   # JavaScript plugin scripts (ESM)
│   ├── session-align.mjs         # Blueprint alignment on session end
│   ├── session-align.test.mjs   # Tests (Vitest)
│   └── mcp-server.test.cjs      # MCP server tests (CJS, legacy)
│
skills/                    # Claude Code skills (slash commands)
│   ├── init/                     # Blueprint layer initialization
│   │   └── SKILL.md             # init protocol definition
│   ├── explore/                  # Blueprint-first exploration
│   │   └── SKILL.md             # explore protocol definition
│   └── align/                    # Blueprint alignment check
│       └── SKILL.md             # align protocol definition
│
hooks/                     # Plugin hooks (legacy)
│   └── hooks.json               # SessionEnd hook (SessionEnd → session-align.mjs)
│
.claude/                   # Claude Code integration
│   ├── hooks/                  # Python runtime hooks
│   │   ├── session-start.py           # Session start context injection
│   │   ├── inject-subagent-context.py  # PreToolUse agent context injection
│   │   └── ralph-loop.py              # SubagentStop quality gate
│   ├── agents/                 # Multi-agent definitions
│   │   ├── implement.md
│   │   ├── check.md
│   │   ├── research.md
│   │   ├── plan.md
│   │   ├── debug.md
│   │   └── dispatch.md
│   ├── commands/              # Slash command definitions
│   │   └── trellis/           # bwflow workflow commands
│   │       ├── start.md
│   │       ├── finish-work.md
│   │       └── ...
│   └── settings.json           # Hook configuration
│
.blueprint/                 # Blueprint layer (intention layer)
│   ├── README.md              # Root blueprint
│   ├── bridge/
│   ├── scripts/
│   ├── skills/
│   └── ...
```

---

## Module Organization

### JavaScript Scripts

Each script is a standalone ESM module with named exports:

```javascript
// scripts/session-align.mjs
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

export { buildSummary, collectWorkspaceStatus, main, parseGitStatus };

// Entry point
let rawInput = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', (chunk) => { rawInput += chunk; });
process.stdin.on('end', () => {
  try {
    const output = main(rawInput);
    if (output) process.stdout.write(output);
  } catch {
    // Fail closed for SessionEnd hooks
  }
});
```

### Claude Code Skills

Skills are Markdown files with YAML frontmatter defining the protocol:

```markdown
---
name: explore
description: 探索和熟悉项目上下文时，优先通过蓝图收敛最相关的职责、边界和关键方法。
---

# explore - Blueprint First Exploration

## 目标
...

## 执行步骤
1. ...
2. ...
```

### Layer Responsibilities

| Layer | Directory | Technology | Responsibility |
|-------|-----------|------------|----------------|
| Plugin Logic | `scripts/` | Node.js ESM | Blueprint alignment, session management |
| Skill Definitions | `skills/` | Markdown | Slash command protocols |
| Claude Hooks | `.claude/hooks/` | Python 3.10+ | Context injection at Claude runtime |
| Blueprint Layer | `.blueprint/` | Markdown | Intent layer for project understanding |

---

## Naming Conventions

| Pattern | Example | Usage |
|---------|---------|-------|
| `kebab-case.mjs` | `session-align.mjs` | ESM scripts |
| `kebab-case.test.mjs` | `session-align.test.mjs` | ESM test files |
| `kebab-case/SKILL.md` | `explore/SKILL.md` | Skill directory + definition |

---

## Cross-Platform Compatibility

JavaScript scripts use `node:` prefix for built-in modules:

```javascript
// Good - explicit node: prefix
import fs from 'node:fs';
import path from 'node:path';

// Bad - bare specifier (implicit node: allowed but less clear)
import fs from 'fs';
```

---

## DO / DON'T

### DO

- Use `node:` prefix for built-in module imports
- Use named exports for all utility functions
- Use `try/catch` with fail-closed pattern in hook entry points
- Use `spawnSync` with explicit `encoding: "utf-8"` for subprocess calls
- Use absolute paths via `path.resolve()` for Git operations

### DON'T

- Don't use default exports for utility modules
- Don't use bare specifiers for Node.js built-ins
- Don't throw unhandled errors in hook entry points
- Don't use `process.exit(1)` in hook scripts (use fail-closed pattern)
