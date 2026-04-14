# Quality Guidelines

> Code quality standards for JavaScript scripts.

---

## Overview

JavaScript scripts in this project follow ESM conventions with JSDoc type annotations for safety.

---

## Module System

### ESM with Named Exports

```javascript
// Good: Named exports
export { buildSummary, collectWorkspaceStatus, main, parseGitStatus };

// Bad: Default export
export default { buildSummary, collectWorkspaceStatus };
```

### Node.js Built-in Imports

Always use `node:` prefix for built-in modules:

```javascript
// Good
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

// Acceptable but less explicit
import fs from 'fs';
```

---

## Type Safety

### JSDoc Annotations

```javascript
// @ts-check — Enable type checking at top of file

/**
 * @param {string} rawInput
 * @returns {string}
 */
function main(rawInput) {
  // ...
}
```

### Forbidden Types

| Type | Why | Alternative |
|------|-----|-------------|
| `any` | No type safety | `unknown` or specific type |
| `@ts-ignore` | Bypasses checking | Fix the annotation |

---

## Error Handling

### Hook Entry Points: Fail Closed

```javascript
process.stdin.on('end', () => {
  try {
    const output = main(rawInput);
    if (output) process.stdout.write(output);
  } catch {
    // Fail closed — never disrupt Claude shutdown
  }
});
```

### Utility Functions: Explicit Error Results

```javascript
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

## Path Handling

Always use `path` module for path operations:

```javascript
import path from 'node:path';

const configPath = path.join(cwd, RUNTIME_DIR, SUMMARY_FILE);
const displayPath = filePath.replace(/\\/g, '/');
```

---

## Quality Checklist

Before committing JavaScript changes:

- [ ] All functions have JSDoc type annotations
- [ ] No `any` types
- [ ] No `@ts-ignore` or `@ts-nocheck`
- [ ] All imports use `node:` prefix for built-ins
- [ ] Hook entry points use fail-closed pattern
- [ ] Path operations use `node:path`
- [ ] JSON parsing has error handling

---

## DO / DON'T

### DO

- Use `node:` prefix for built-in imports
- Use named exports
- Document function signatures with JSDoc
- Use `unknown` for untyped input
- Use strict equality (`===`)

### DON'T

- Don't use `any` type
- Don't use `@ts-ignore`
- Don't use default exports for utilities
- Don't use bare specifiers for built-ins
