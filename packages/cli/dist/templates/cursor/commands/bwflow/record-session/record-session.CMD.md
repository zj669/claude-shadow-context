# Record Session

Record session summary and link commits to tasks.

---

## When to Use

After completing a task or significant milestone.

---

## What It Records

1. Session summary (what was done)
2. Commits made during session
3. Task status update
4. Links to relevant documents

---

## Workflow

### Step 1: Check Current State

```bash
# View recent commits
git log --oneline -10

# View current task
cat .bwflow/.current-task
```

### Step 2: Run Record

```bash
python3 ./.bwflow/scripts/record_session.py
```

This will:
- Prompt for session summary
- Link commits to current task
- Update task status
- Generate session report

### Step 3: Verify

Check the generated report in:
`.bwflow/tasks/<task>/sessions/<date>-<time>.md`

---

## Output Format

```markdown
# Session Report

## Date
YYYY-MM-DD HH:MM

## Task
<task-name>

## Summary
<what was accomplished>

## Commits
- abc1234: <commit message>
- def5678: <commit message>

## Next Steps
<what comes next>
```

---

## Commands

| Command | Purpose |
|---------|---------|
| `.bwflow/scripts/record_session.py` | Record current session |
| `.bwflow/scripts/task.py archive <task>` | Archive completed task |
