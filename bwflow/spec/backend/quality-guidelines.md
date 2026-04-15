# Quality Guidelines

> **To be filled by the team**: Document your project's code quality standards and practices.

---

## Overview

**To be filled by the team**: Describe your quality standards.

Questions to answer:
- What tools are used for code quality (linters, formatters, type checkers)?
- What are the quality gates before code can be merged?
- How is code quality measured?

---

## Code Style

**To be filled by the team**: Document code style conventions.

Questions to answer:
- What style guide is followed?
- How should code be formatted?
- What naming conventions are used?

---

## Testing Standards

**To be filled by the team**: Document testing requirements.

Questions to answer:
- What types of tests are required (unit, integration, e2e)?
- What is the minimum test coverage requirement?
- How should tests be structured?

---

## Code Review

**To be filled by the team**: Document code review practices.

Questions to answer:
- What should reviewers look for?
- What are common issues to avoid?
- How should feedback be given?

---

## Examples

**To be filled by the team**: Provide examples of high-quality code from your project.

```python
# Example: To be filled by the team
```

### Forbidden Patterns

| Pattern | Why Forbidden | Correct Alternative |
|---------|---------------|---------------------|
| `any` type | No type safety | `dict \| None`, `list[str]` |
| `os.path.join()` | Platform issues | `pathlib.Path` `/` operator |
| Implicit return types | Unclear contracts | Explicit `-> Type` |

### Required Patterns

| Pattern | Requirement | Example |
|---------|-------------|---------|
| Return type declarations | All functions | `def foo() -> int:` |
| Unused variables | Prefix with `_` | `def f(_req, res):` |
| UTF-8 encoding | All file I/O | `encoding="utf-8"` |

---

## JavaScript: ESM Quality Standards

### Strict Mode and Type Safety

This project uses JSDoc-style type documentation:

```javascript
// @ts-check — Enable type checking

/**
 * @param {string} rawInput
 * @returns {string}
 */
function main(rawInput) {
  // ...
}
```

### Forbidden Patterns

| Pattern | Why Forbidden | Correct Alternative |
|---------|---------------|---------------------|
| `any` type | No type safety | `unknown` or specific types |
| `==` (loose) | Type coercion bugs | `===` |
| `\|\|` for defaults | Treats falsy values | `??` (nullish coalescing) |

### Required Patterns

| Pattern | Requirement | Example |
|---------|-------------|---------|
| Named exports | All public functions | `export function foo(): void` |
| Error boundaries | Hook entry points | `try/catch` with documented behavior |
| Strict equality | All comparisons | `===` |

---

## Shared: Path Handling

### Python: Always Use `pathlib.Path`

```python
# Good
from pathlib import Path
def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")
config_path = repo_root / DIR_WORKFLOW / "config.json"

# Bad - string concatenation
config_path = repo_root + "/" + DIR_WORKFLOW + "/config.json"
```

### JavaScript: Use `node:path` and `node:fs`

```javascript
// Good
import { join } from 'node:path';
import { existsSync, readFileSync } from 'node:fs';
const configPath = join(repoRoot, '.trellis', 'config.json');

// Bad - relative path without path.join
const configPath = repoRoot + '/bwflow/config.json';
```

---

## Shared: JSON Operations

### Python

```python
import json
from pathlib import Path

def read_json(path: Path) -> dict | None:
    """Read JSON file, return None on error."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None

def write_json(path: Path, data: dict) -> bool:
    """Write JSON file, return success status."""
    try:
        path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
        return True
    except Exception:
        return False
```

### JavaScript

```javascript
import { readFileSync, writeFileSync } from 'node:fs';

function safeParse(rawInput) {
  if (!rawInput || !rawInput.trim()) return null;
  try {
    return JSON.parse(rawInput);
  } catch {
    return null;
  }
}
```

---

## Python: Logging

Use the centralized `common/log.py` for consistent output:

| Function | Output | Usage |
|----------|--------|-------|
| `log_info(msg)` | `[INFO] msg` (blue) | General information |
| `log_success(msg)` | `[SUCCESS] msg` (green) | Successful operations |
| `log_warn(msg)` | `[WARN] msg` (yellow) | Warnings, degraded functionality |
| `log_error(msg)` | `[ERROR] msg` (red) | Errors |

All `log_*` functions print to **stdout**. Use `print(..., file=sys.stderr)` for stderr output.

---

## Quality Checklist

Before committing Python or JavaScript changes, ensure:

- [ ] Type hints (Python) / JSDoc (JavaScript) are complete
- [ ] No forbidden patterns (`any`, loose equality)
- [ ] All functions have explicit return types
- [ ] Path operations use proper APIs (`pathlib`, `node:path`)
- [ ] JSON operations have error handling
- [ ] No hardcoded paths — use constants
- [ ] Unused variables are prefixed with `_`
- [ ] Import statements are grouped: stdlib → third-party → local

---

## Import Organization

### Python

```python
# 1. Future imports
from __future__ import annotations

# 2. Standard library
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# 3. Local imports
from common.paths import get_repo_root
from common.developer import get_developer
```

### JavaScript (ESM)

```javascript
// 1. Node.js built-ins
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

// 2. Named exports (avoid default exports for utilities)
export { buildSummary, collectWorkspaceStatus };
```

---

## DO / DON'T

### Python

- **DO**: Use `pathlib.Path`, type hints, `encoding="utf-8"`
- **DO**: Prefix unused parameters with `_`
- **DO**: Return exit codes from `main()`
- **DO**: Print errors to stderr
- **DON'T**: Use string path concatenation
- **DON'T**: Use external dependencies (stdlib only for scripts)

### JavaScript

- **DO**: Use named exports for utilities
- **DO**: Use `node:` prefix for built-in imports
- **DO**: Use strict equality (`===`)
- **DO**: Use nullish coalescing (`??`) over `||`
- **DON'T**: Use `any` type
- **DON'T**: Throw unhandled errors in hook entry points
