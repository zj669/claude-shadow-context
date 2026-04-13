# Cross-Layer Thinking Guide

> **Purpose**: Think through data flow across layers before implementing.

---

## The Problem

**Most bugs happen at layer boundaries**, not within layers.

Common cross-layer bugs:
- Hook output format doesn't match Claude runtime expectations
- Python context injection produces different JSON than JavaScript version
- Blueprint drift after code changes (intent ≠ implementation)

---

## Before Implementing Cross-Layer Features

### Step 1: Map the Data Flow

Draw out how data moves:

```
User Input → Claude Hook → JSON Context → Agent Prompt → Code Change → Blueprint Update
```

For each arrow, ask:
- What format is the data in?
- What could go wrong?
- Who is responsible for validation?

### Step 2: Identify Boundaries

| Boundary | Common Issues |
|----------|---------------|
| Claude Hook → JSON | Type mismatch, missing fields |
| Hook Output → Agent | Encoding issues, JSON corruption |
| Code Change → Blueprint | Drift (intent ≠ implementation) |
| Python Hook → JS Hook | Different error handling patterns |

### Step 3: Define Contracts

For each boundary:
- What is the exact input format?
- What is the exact output format?
- What errors can occur?

---

## Common Cross-Layer Mistakes

### Mistake 1: JSON Corruption in Hook Output

**Bad**: Printing debug text to stdout in Claude Code hooks

```python
# Bad: Debug print corrupts JSON output
print(f"[DEBUG] Loading context from {task_dir}")
result = {"hookSpecificOutput": {...}}
print(json.dumps(result))  # JSON is corrupted by debug print!
```

**Good**: Use stderr for debug, stdout for JSON only

```python
print(f"[DEBUG] Loading context from {task_dir}", file=sys.stderr)
result = {"hookSpecificOutput": {...}}
print(json.dumps(result))  # Clean JSON on stdout
```

### Mistake 2: Blueprint Drift After Code Changes

**Bad**: Changing code without updating corresponding blueprint

```markdown
# session-align.mjs 蓝图 (stale)
## 关键方法单元
- location: buildSummary
- purpose: 生成会话摘要
```

The actual code added `recommendations` field but blueprint wasn't updated.

**Good**: Run `align` before commit to check for drift

### Mistake 3: Inconsistent Encoding Across Hooks

**Bad**: Python hook uses UTF-8, JavaScript hook doesn't handle encoding

```javascript
// Bad: Assumes UTF-8 implicitly
const stdout = spawnSync('git', ['status']).stdout;
```

**Good**: Explicit encoding in subprocess calls

```javascript
// Good: Explicit UTF-8 encoding
const result = spawnSync('git', ['status'], { encoding: 'utf8' });
```

---

## Checklist for Cross-Layer Features

Before implementation:
- [ ] Mapped the complete data flow
- [ ] Identified all layer boundaries (Python ↔ JavaScript ↔ Claude runtime)
- [ ] Defined format at each boundary
- [ ] Decided where validation happens
- [ ] Verified encoding is consistent across all layers

After implementation:
- [ ] Tested with edge cases (null, empty, invalid)
- [ ] Verified error handling at each boundary
- [ ] Ran `align` to check blueprint drift

---

## Hook → Claude Runtime Contract

Claude Code hooks return structured JSON. The contract:

```javascript
// PreToolUse output
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",   // or "block"
    "updatedInput": { "prompt": "..." }  // modified prompt
  }
}

// SessionStart output
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "..."  // injected context text
  }
}
```

**Rule**: stdout must contain ONLY valid JSON. Any extra text corrupts the contract.

---

## Blueprint ↔ Code Contract

Code files have corresponding blueprints with path mapping:

| Code | Blueprint |
|------|-----------|
| `scripts/session-align.mjs` | `.blueprint/scripts/session-align.md` |
| `skills/explore/SKILL.md` | `.blueprint/skills/explore/SKILL.md` |

**Rule**: After changing code, run `align` to verify blueprint is still accurate.

---

## When to Create Flow Documentation

Create detailed flow docs when:
- Feature spans 3+ layers (Python hook → JSON → Agent → Blueprint)
- Data format is complex
- Feature has caused cross-layer bugs before
