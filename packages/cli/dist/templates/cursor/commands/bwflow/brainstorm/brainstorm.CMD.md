# Brainstorm

Clarify vague requirements and create a structured plan.

---

## When to Use

Use when:
- Requirements are unclear
- Multiple approaches possible
- User says "I want to add a feature for..."
- No clear implementation path

Don't use for:
- Questions about existing code
- Trivial fixes with clear instructions
- Well-defined small changes

---

## Workflow

### Step 1: Acknowledge

Acknowledge the idea and state your understanding.

### Step 2: Create Task Directory

```bash
TASK_DIR=$(python3 ./.bwflow/scripts/task.py create "<title>" --slug <name>)
```

### Step 3: Ask Questions

Ask **one question at a time**:

1. What is the core goal?
2. Who are the users?
3. What data is involved?
4. What are the constraints?
5. How do we measure success?

### Step 4: Update PRD

After each answer, update `prd.md`:

```markdown
# Task Title

## Goal
<What we're trying to achieve>

## Requirements
- <Requirement 1>
- <Requirement 2>

## Acceptance Criteria
- [ ] <Criterion 1>
- [ ] <Criterion 2>
```

### Step 5: Propose Approaches

For complex decisions, propose 2-3 approaches with trade-offs.

### Step 6: Confirm

Get explicit approval before proceeding.

---

## Key Principles

| Principle | Description |
|-----------|-------------|
| **One at a time** | Never ask multiple questions |
| **Update PRD** | Document decisions immediately |
| **Multiple choice** | Easier for users to answer |
| **YAGNI** | Challenge unnecessary complexity |

---

## Subtask Decomposition

If multiple independent work items emerge:

```bash
python3 ./.bwflow/scripts/task.py create "<subtask>" --slug <name> --parent <parent-task>
```

---

## Output

After brainstorm:
1. Clear PRD in task directory
2. Confirmed requirements
3. Ready to proceed to Task Workflow
