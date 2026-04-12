# bwflow:explore

Blueprint-first exploration. Understand project context before diving into code.

---

## Goal

Let AI understand the project using blueprints first, instead of searching through code.

## Core Thinking

Fixed reading order for minimum context:

```
Root Blueprint (bwflow/blueprint/README.md)
    ↓
Session Summary (bwflow/last-session.md) - if exists
    ↓
Module Blueprint (bwflow/blueprint/{module}/index.md)
    ↓
File Blueprint (bwflow/blueprint/{module}/{file}.md)
    ↓
Necessary Code (only when blueprints are insufficient)
```

---

## Execution Steps

### 1. Understand the current task

Determine which business domain, module, or problem the user wants to explore.

### 2. Read root blueprint

```bash
cat bwflow/blueprint/README.md
```

### 3. Read session summary (if exists)

```bash
cat bwflow/last-session.md
```

Check if there are any pending `init` or `align` tasks from the last session.

### 4. Follow the blueprint path

Based on the root blueprint's module map, navigate to the relevant module blueprint:

```bash
cat bwflow/blueprint/{module}/index.md
```

### 5. Read all relevant blueprints

Extract responsibilities, boundaries, key methods, and dependencies from blueprints.

### 6. Only read code when necessary

Only look at actual code when:
- Blueprints don't contain enough detail
- Need to understand specific implementation
- Need to verify the current state

### 7. Output minimum viable context

Report:
- Relevant business domain or module
- Most relevant blueprint files
- Responsibility and key method summary
- Recommended code locations to continue exploring

---

## Rules

- **Don't** load the entire `bwflow/blueprint/` at once
- **Don't** skip the root blueprint and search code directly
- Session summary is only a clue, not a replacement for blueprints
- When blueprints are sufficient, don't expand to implementation details
- If the project lacks blueprints, recommend running `/bwflow:init` first
- If a file lacks a blueprint, record that file path; the align phase will fill it in
- **Explore is read-only** — don't generate blueprints during exploration

---

## Output Template

```markdown
## Relevant Module
{module name}

## Relevant Blueprints
- bwflow/blueprint/{module}/index.md
- bwflow/blueprint/{module}/{file}.md

## Responsibilities
- {responsibility 1}
- {responsibility 2}

## Key Methods
- {method name}: {purpose}
- {method name}: {purpose}

## Recommended Code Locations
- {file path}: {what to look for}
```

---

## Core Principle

> **Blueprint First, Code Second** — Understand the "why" before the "how".
