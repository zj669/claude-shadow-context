# Component Guidelines

> How JavaScript modules (not UI components) are structured in this project.

---

## Overview

This project doesn't have UI components. "Component" here refers to JavaScript modules — self-contained functional units with clear responsibilities.

---

## Module Structure

### Standard Pattern

Each JavaScript module follows this structure:

```javascript
// 1. imports
import fs from 'node:fs';
import path from 'node:path';

// 2. constants
const RUNTIME_DIR = '.claude-shadow-context';
const SUMMARY_FILE = 'last-session.md';
const MAX_LISTED_FILES = 20;

// 3. helper functions (private)
// 4. public functions (exported)

// 5. main entry point
let rawInput = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', (chunk) => { rawInput += chunk; });
process.stdin.on('end', () => {
  try {
    const output = main(rawInput);
    if (output) process.stdout.write(output);
  } catch {
    // Fail closed for hook scripts
  }
});

// 6. exports
export { buildSummary, collectWorkspaceStatus, main, parseGitStatus };
```

### Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Module file | `kebab-case.mjs` | `session-align.mjs` |
| Function | `camelCase` | `buildSummary`, `collectWorkspaceStatus` |
| Constant | `UPPER_SNAKE_CASE` | `RUNTIME_DIR`, `MAX_LISTED_FILES` |
| Private helper | Prefix with `_` | `_normalizePath` |

---

## Function Design

### Single Responsibility

Each function does one thing:

```javascript
// Good: Single purpose
function parseGitStatus(stdout) {
  return stdout.split(/\r?\n/).filter(Boolean).map((line) => {
    const status = line.slice(0, 2);
    const filePath = normalizeGitPath(line.slice(3));
    return { status, filePath };
  });
}

// Bad: Multiple responsibilities
function parseGitStatusAndLog(stdout, cwd) {
  // Parsing AND logging mixed together
}
```

### Explicit Return Types

Document return types via JSDoc:

```javascript
/**
 * @param {string} stdout
 * @returns {Array<{ status: string, filePath: string }>}
 */
function parseGitStatus(stdout) {
  // ...
}
```

---

## Error Handling in Modules

### Fail-Closed for Hooks

Hook entry scripts use stdin/stdout for communication with Claude runtime:

```javascript
// session-align.mjs
process.stdin.on('end', () => {
  try {
    const output = main(rawInput);
    if (output) process.stdout.write(output);
  } catch {
    // SessionEnd hook should fail closed to avoid disrupting Claude shutdown.
  }
});
```

### Explicit Error Propagation for Utilities

Utility functions propagate errors rather than swallowing them:

```javascript
/**
 * @param {string} cwd
 * @returns {{ changedFiles: Array, blueprintFiles: Array, worktreeFiles: Array }}
 */
function collectWorkspaceStatus(cwd) {
  // Return structured result, let caller handle errors
  if (!isGitRepo(cwd)) {
    return { changedFiles: [], blueprintFiles: [], worktreeFiles: [] };
  }
  // ...
}
```

---

## Testing Pattern

Tests use Vitest:

```javascript
// session-align.test.mjs
import { describe, it, expect } from 'vitest';
import { parseGitStatus } from './session-align.mjs';

describe('parseGitStatus', () => {
  it('parses standard git status output', () => {
    const stdout = ' M file.js\n?? new-file.js';
    const result = parseGitStatus(stdout);
    expect(result).toHaveLength(2);
    expect(result[0].status).toBe(' M');
  });
});
```

---

## DO / DON'T

### DO

- Use named exports for all public functions
- Use `node:` prefix for built-in module imports
- Document function signatures with JSDoc
- Keep functions focused (single responsibility)
- Use fail-closed pattern for hook entry points

### DON'T

- Don't use default exports for utility modules
- Don't mix concerns (parsing + logging + file I/O in one function)
- Don't throw from utility functions (return error results instead)
- Don't use bare specifiers for Node.js built-ins
