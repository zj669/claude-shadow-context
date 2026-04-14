# Type Safety

> Type safety patterns for JavaScript scripts in this project.

---

## Overview

JavaScript uses JSDoc annotations for type safety since there's no TypeScript build step for plugin scripts.

---

## JSDoc Type Annotations

Use `@type`, `@param`, and `@returns` for type documentation:

```javascript
/**
 * @typedef {Object} GitStatusEntry
 * @property {string} status
 * @property {string} filePath
 */

/**
 * @param {string} rawInput
 * @returns {string}
 */
function main(rawInput) {
  // ...
}
```

---

## Common Type Patterns

### Parsed JSON Input

```javascript
/**
 * @param {string} rawInput
 * @returns {Object | null}
 */
function safeParse(rawInput) {
  if (!rawInput || !rawInput.trim()) {
    return null;
  }
  try {
    return JSON.parse(rawInput);
  } catch {
    return null;
  }
}
```

### File System Operations

```javascript
/**
 * @param {string} cwd
 * @returns {boolean}
 */
function isGitRepo(cwd) {
  const gitProbe = spawnSync('git', ['-C', cwd, 'rev-parse', '--is-inside-work-tree'], {
    encoding: 'utf8'
  });
  return gitProbe.status === 0 && gitProbe.stdout.trim() === 'true';
}
```

### Path Handling

```javascript
/**
 * @param {string} filePath
 * @returns {string}
 */
function toDisplayPath(filePath) {
  return filePath.replace(/\\/g, '/');
}
```

---

## Type Guard Patterns

```javascript
/**
 * @param {unknown} value
 * @returns {boolean}
 */
function isObject(value) {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

/**
 * @param {unknown} payload
 * @returns {payload is { cwd: string, session_id: string, reason: string }}
 */
function isValidPayload(payload) {
  return isObject(payload)
    && typeof (/** @type {any} */(payload).cwd) === 'string'
    && typeof (/** @type {any} */(payload).session_id) === 'string';
}
```

---

## Forbidden Patterns

| Pattern | Why | Correct Alternative |
|---------|-----|---------------------|
| `@ts-ignore` | Bypasses type checking | Fix the type annotation |
| `// @ts-nocheck` | Disables all checking | Add proper JSDoc |
| `any` type | No safety | `unknown` or specific type |
| Loose equality (`==`) | Type coercion | Strict equality (`===`) |

---

## DO / DON'T

### DO

- Use JSDoc annotations for all function signatures
- Use `unknown` for untyped external input
- Use type guards for runtime validation
- Use `typeof` checks before property access

### DON'T

- Don't use `any` type
- Don't use `@ts-ignore` or `@ts-nocheck`
- Don't use loose equality (`==`)
- Don't assume property existence without checking
