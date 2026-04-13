# Update Spec

Update code-spec documents when new patterns or conventions are discovered.

---

## When to Use

- New coding patterns established
- Bug discovered with non-obvious fix
- Cross-layer contracts defined
- Lessons learned during development

---

## Two-Layer Update

| Layer | Document | When to Update |
|-------|----------|----------------|
| **Blueprint** | Architecture intent | New modules, design decisions |
| **Spec** | Coding conventions | Patterns, guidelines, contracts |

---

## Update Blueprint

Create/update `.bwflow/blueprint/<module>/README.md`:

```markdown
# Module Blueprint

## Responsibilities
What this module does

## Key Methods
| Method | Path | Description |
|--------|------|-------------|
| method1 | path/to/file.ts | What it does |

## Design Intent
Why decisions were made this way

## Change Log
- YYYY-MM-DD Initial
- YYYY-MM-DD Updated: <reason>
```

---

## Update Spec

Create/update `.bwflow/spec/<layer>/<topic>.md`:

```markdown
# <Topic> Guidelines

## When to Apply
When to use this pattern

## Pattern
```typescript
// Code example
```
## Examples
- Good: `<file>:<line>`
- Bad: `<file>:<line>`

## Common Mistakes
What to avoid
```

---

## Trigger Conditions

Update spec when:
- New component pattern established
- Cross-layer contract defined
- Error handling approach standardized
- Non-obvious bug fix discovered
- API contract created

---

## Quick Update Flow

```bash
# 1. Identify what changed
git diff --name-only

# 2. Determine which spec to update
# - New files → create spec
# - Changed behavior → update spec
# - Bug fix → add to error-handling.md

# 3. Update the spec file
# 4. Verify format consistency
```
