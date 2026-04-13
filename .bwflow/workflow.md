# Development Workflow

> Blueprint-driven structured AI development companion.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Core Principles](#core-principles)
3. [Session Start Process](#session-start-process)
4. [Development Process](#development-process)
5. [Session End](#session-end)
6. [File Descriptions](#file-descriptions)
7. [Best Practices](#best-practices)

---

## Quick Start

### Step 0: Initialize Developer Identity (First Time Only)

```bash
# Check if already initialized
python3 ./bwflow/scripts/get_developer.py

# If not initialized, run:
python3 ./bwflow/scripts/init_developer.py <your-name>
```

This creates:
- `.bwflow/.developer` - Your identity file (gitignored, not committed)
- `.bwflow/workspace/<your-name>/` - Your personal workspace directory

### Step 1: Understand Current Context

```bash
# Get full context in one command
python3 ./bwflow/scripts/get_context.py
```

### Step 2: Read Project Guidelines

**CRITICAL**: Read guidelines before writing any code:

```bash
# Read frontend guidelines index (if applicable)
cat .bwflow/spec/frontend/index.md

# Read backend guidelines index (if applicable)
cat .bwflow/spec/backend/index.md
```

### Step 3: Before Coding - Read Specific Guidelines

Based on your task, read the **detailed** guidelines:

**Frontend Task**:
```bash
cat .bwflow/spec/frontend/component-guidelines.md
cat .bwflow/spec/frontend/type-safety.md
```

**Backend Task**:
```bash
cat .bwflow/spec/backend/database-guidelines.md
cat .bwflow/spec/backend/error-handling.md
```

---

## Core Principles

1. **Blueprint First** — Read `.bwflow/blueprint/` before diving into code
2. **Follow Standards** — **MUST read** `.bwflow/spec/` guidelines before coding
3. **Minimum Context** — Blueprints are sufficient, don't expand to implementation details
4. **End Alignment** — Check if blueprints are still trustworthy at task end

---

## Session Start Process

### Step 1: Get Session Context

```bash
python3 ./bwflow/scripts/get_context.py
```

### Step 2: Read Development Guidelines

**MUST read** guidelines before writing code:

```bash
cat .bwflow/spec/frontend/index.md   # Frontend guidelines
cat .bwflow/spec/backend/index.md    # Backend guidelines
cat .bwflow/spec/guides/index.md     # Thinking guides
```

### Step 3: Select Task to Develop

```bash
# List active tasks
python3 ./bwflow/scripts/task.py list

# Create new task
python3 ./bwflow/scripts/task.py create "<title>" --slug <name>
```

---

## Development Process

### Task Development Flow

```
1. Create or select task
   --> python3 ./bwflow/scripts/task.py create "<title>" --slug <name>

2. Explore using blueprints
   --> /bwflow:explore

3. Implement according to guidelines
   --> Read bwflow/spec/ docs relevant to your task

4. Self-test
   --> Run project's lint/test commands

5. Commit code
   --> git add <files>
   --> git commit -m "type(scope): description"

6. Record session
   --> python3 ./bwflow/scripts/add_session.py --title "Title" --commit "hash"
```

### Code Quality Checklist

**Must pass before commit**:
- [OK] Lint checks pass
- [OK] Type checks pass (if applicable)
- [OK] Tests pass

---

## Session End

### One-Click Session Recording

After code is committed, use:

```bash
python3 ./bwflow/scripts/add_session.py \
  --title "Session Title" \
  --commit "abc1234" \
  --summary "Brief summary"
```

### Pre-end Checklist

Use `/bwflow:finish-work` command to run through:
1. [OK] All code committed
2. [OK] Blueprint alignment checked (`/bwflow:align`)
3. [OK] No lint/test errors
4. [OK] Session recorded

---

## File Descriptions

### 1. bwflow/blueprint/ - Blueprint Layer

**Purpose**: Architecture intent, module responsibilities, key methods

**Structure**:
```
blueprint/
├── README.md              # Root blueprint
└── {module}/              # Module blueprints
    ├── index.md
    └── {file}.md          # File-level blueprints
```

**When to update**:
- New module created
- Module responsibility changed
- Key method signatures changed

### 2. bwflow/spec/ - Coding Standards

**Purpose**: Code style, patterns, quality guidelines

**Structure**:
```
spec/
├── backend/              # Backend guidelines
├── frontend/            # Frontend guidelines
└── guides/              # Thinking guides
```

**When to update**:
- New pattern discovered
- Bug fixed that reveals missing guidance
- New convention established

### 3. bwflow/tasks/ - Task Tracking

Each task is a directory:

```
tasks/
├── MM-DD-name/
│   ├── task.json
│   ├── prd.md
│   └── context/
│       ├── blueprint.jsonl
│       ├── implement.jsonl
│       └── check.jsonl
└── archive/
```

### 4. bwflow/workspace/ - Session Logs

```
workspace/
├── index.md              # Workspace index
└── {developer}/
    ├── index.md          # Personal index
    └── journal-N.md       # Journal files
```

---

## Best Practices

### DO

1. **Before session start**:
   - Run `python3 ./bwflow/scripts/get_context.py`
   - **MUST read** relevant `bwflow/spec/` docs

2. **During development**:
   - **Follow** `bwflow/spec/` guidelines
   - Use `/bwflow:explore` for understanding
   - Use `/bwflow:align` before finishing

3. **After development**:
   - Use `/bwflow:finish-work` for completion checklist
   - Human commits after testing passes
   - Use `add_session.py` to record progress

### DON'T

1. **Don't** skip reading `bwflow/spec/` guidelines
2. **Don't** let journal exceed 2000 lines
3. **Don't** develop multiple unrelated tasks simultaneously
4. **Don't** commit code with lint/test errors

---

## Quick Reference

### Must-read Before Development

| Task Type | Must-read Document |
|-----------|-------------------|
| Frontend work | `frontend/index.md` → relevant docs |
| Backend work | `backend/index.md` → relevant docs |
| Blueprint understanding | `blueprint/README.md` |

### Commit Convention

```bash
git commit -m "type(scope): description"
```

**Type**: feat, fix, docs, refactor, test, chore
**Scope**: Module name (e.g., auth, api, ui)

### Common Commands

```bash
# Session management
python3 ./bwflow/scripts/get_context.py    # Get full context
python3 ./bwflow/scripts/add_session.py    # Record session

# Task management
python3 ./bwflow/scripts/task.py list     # List tasks
python3 ./bwflow/scripts/task.py create    # Create task

# Slash commands
/bwflow:start           # Session start
/bwflow:explore        # Blueprint-first exploration
/bwflow:align           # Blueprint alignment check
/bwflow:finish-work     # Pre-commit checklist
```

---

## Summary

Following this workflow ensures:
- [OK] Continuity across multiple sessions
- [OK] Consistent code quality
- [OK] Trackable progress
- [OK] Blueprint understanding persists
- [OK] Knowledge accumulation in spec docs
