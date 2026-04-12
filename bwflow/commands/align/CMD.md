# bwflow:align

Check if blueprints are still aligned with code after task completion.

---

## Goal

Keep blueprints trustworthy, not just at the beginning of tasks.

## When to Use

- Task completion
- Session end
- Before commit
- After significant code changes

## Focus Scope

Prioritize checking code that has **architectural intent changes**, not mechanical changes.

---

## Execution Steps

### 1. Identify meaningful business changes

Only code with business significance may require blueprint updates.

Ignore:
- Formatting changes
- Comment updates
- Mechanical adjustments

### 2. Map code paths to blueprint paths

Based on the code-to-blueprint path mapping:

```
scripts/session-align.mjs → bwflow/blueprint/scripts/session-align.md
hooks/hooks.json → bwflow/blueprint/hooks/hooks.md
```

Record:
- Missing blueprints
- Potentially outdated blueprints

### 3. Compare code with blueprints

Check if:
- Responsibilities are still accurate
- Key methods are still correct
- Input/output are unchanged
- Boundaries are maintained

### 4. Classify results

| Result | Action |
|--------|--------|
| No update needed | Done |
| Change log entry needed | Add to blueprint |
| Responsibility or key method needs correction | Update blueprint |
| Blueprint missing | Create blueprint |

### 5. Create missing blueprints

For files without blueprints that were touched this session:

Create using the three-section template:

```markdown
# {filename} Blueprint

## Metadata
- title: {title}
- type: {class|module|service|controller|util}
- summary: {one-line description}

## Key Method Units (only for core business files)
- location: {class.method or function}
- purpose: {why this exists}
- input: {parameter types}
- output: {return type}
- core_steps: {business steps, not code details}

## Change Log
- YYYY-MM-DD: {change summary}
```

### 6. Output final alignment result

Report:
- Alignment status (pass / warning / fail)
- Missing or outdated blueprint files
- Responsibilities or key methods needing correction
- Suggested or completed blueprint sync

---

## Rules

- **Focus on intent drift**, not implementation noise
- **Use git diff** to narrow the scope
- **Don't rewrite all blueprints** just because templates exist
- **Maintain stable path mapping** to keep code-to-blueprint relationship trustworthy
- **Prioritize fixing responsibilities** over expanding details
- **Only create blueprints** for files actually touched this session

---

## Blueprint Template

```markdown
# {filename} Blueprint

## Metadata
- title: {title}
- type: {class|module|service|controller|util}
- summary: {one-line description}

## Key Method Units
- location: {class.method or function}
- purpose: {why this exists}
- input: {parameter types}
- output: {return type}
- core_steps: {business steps}

## Change Log
- YYYY-MM-DD: {change summary}
```

---

## Output

- **Status**: pass / warning / fail
- **Missing blueprints**: [list]
- **Outdated blueprints**: [list]
- **Sync completed**: [list]

---

## Core Principle

> **Blueprints reflect reality, not the other way around.**
