# Code Reuse Thinking Guide

> **Purpose**: Stop and think before creating new code - does it already exist?

---

## The Problem

**Duplicated code is the #1 source of inconsistency bugs.**

When you copy-paste or rewrite existing logic:
- Bug fixes don't propagate
- Behavior diverges over time
- Codebase becomes harder to understand

---

## Before Writing New Code

### Step 1: Search First

```bash
# Search for similar function names
grep -r "functionName" .

# Search for similar patterns
grep -r "parseGitStatus\|collectWorkspaceStatus" .
```

### Step 2: Ask These Questions

| Question | If Yes... |
|----------|-----------|
| Does a similar function exist in `common/`? | Use or extend it |
| Is this pattern used in `.claude/hooks/`? | Follow the existing pattern |
| Could this be a shared utility? | Create it in the right place |
| Am I copying code from another file? | **STOP** - extract to shared |
| Does a blueprint exist for this file? | Update blueprint after changing |

---

## Common Duplication Patterns

### Pattern 1: Copy-Paste Functions

**Bad**: Copying a JSON parsing function to another file

```javascript
// Bad: Duplicated across files
function safeParse(rawInput) {
  if (!rawInput || !rawInput.trim()) return null;
  try { return JSON.parse(rawInput); } catch { return null; }
}
```

**Good**: Import from shared location

```javascript
import { safeParse } from './shared/json.mjs';
```

### Pattern 2: Repeated Path Constants

**Bad**: Defining the same path constant in multiple files

```javascript
// Bad: Hardcoded path
const configPath = '.claude-shadow-context/last-session.md';
```

**Good**: Single source of truth

```javascript
// Good: Centralized constant
import { RUNTIME_DIR, SUMMARY_FILE } from './constants.mjs';
```

### Pattern 3: Similar Claude Hook Patterns

**Bad**: Different error handling in each hook script

```javascript
// Hook 1: Silent failure
catch { /* nothing */ }

// Hook 2: Exit with error
catch (e) => { process.exit(1); }
```

**Good**: Follow the established pattern for each hook type

| Hook Type | Pattern |
|-----------|---------|
| SessionEnd | Fail closed (silent) |
| PreToolUse | Return JSON + allow |
| SessionStart | Return JSON + additionalContext |

---

## Blueprint ↔ Code Alignment

Before changing a file with a blueprint:

1. Read the blueprint first
2. Make the code change
3. Run `align` to check drift
4. Update blueprint if intent changed

```bash
# Before changing session-align.mjs:
/claude-shadow-context:explore
# → Read .blueprint/scripts/session-align.md

# After changing:
/claude-shadow-context:align
# → Verify blueprint still matches
```

---

## After Batch Modifications

When you've made similar changes to multiple files:

1. **Review**: Did you catch all instances?
2. **Search**: Run grep to find any missed
3. **Consider**: Should this be abstracted?
4. **Blueprint**: Did you update all affected blueprints?

---

## Gotcha: Hook vs Script Patterns

**Problem**: Hook scripts (`*.py` in `.claude/hooks/`) and plugin scripts (`*.mjs` in `scripts/`) have different conventions:

| Aspect | Claude Hook (Python) | Plugin Script (JavaScript) |
|--------|---------------------|---------------------------|
| Error handling | Return structured JSON | Fail closed (silent) |
| Encoding | Via `common/__init__.py` | Explicit in subprocess |
| Output | JSON to stdout | JSON or empty |

**Prevention**: Don't copy patterns from one layer to another without checking the contract.

---

## Checklist Before Commit

- [ ] Searched for existing similar code
- [ ] No copy-pasted logic that should be shared
- [ ] Constants defined in one place
- [ ] Similar patterns follow same structure
- [ ] Blueprint updated after code changes
- [ ] `align` run to check for drift
