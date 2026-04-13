# Parallel - Isolated Worktree Execution

Run complex tasks in isolated git worktrees for parallel development.

---

## When to Use

- Complex refactoring affecting many files
- Long-running tasks that shouldn't block main work
- Experiments that might be discarded
- Tasks that need clean context

---

## How It Works

```
Main Branch: feature-a (current)
Worktree 1:  feature-b (isolated)
Worktree 2:  feature-c (isolated)
```

Each worktree has:
- Isolated git working directory
- Independent file changes
- No interference between tasks

---

## Workflow

### Step 1: Create Worktree

```bash
# Create isolated worktree
python3 ./.bwflow/scripts/worktree.py create <task-name>

# This creates:
# - New git worktree at ../<task-name>/
# - Task directory in .bwflow/tasks/<date>-<name>/
# - Switches to worktree automatically
```

### Step 2: Work in Isolated Context

```bash
# You're now in the worktree
cd ../<task-name>

# Initialize bwflow if needed
python3 ./.bwflow/scripts/init.py

# Start working
python3 ./.bwflow/scripts/task.py start <task-dir>
```

### Step 3: Complete Work

```bash
# When done, close worktree
python3 ./.bwflow/scripts/worktree.py close <task-name>
```

### Step 4: Merge Back

```bash
# Back in main branch
git merge <task-name>
```

---

## Commands

| Command | Purpose |
|---------|---------|
| `.bwflow/scripts/worktree.py create <name>` | Create new worktree |
| `.bwflow/scripts/worktree.py list` | List all worktrees |
| `.bwflow/scripts/worktree.py close <name>` | Close worktree |
| `.bwflow/scripts/worktree.py switch <name>` | Switch to worktree |

---

## Key Principles

- **One task per worktree**: Don't mix concerns
- **Keep worktrees short-lived**: Merge back quickly
- **Main branch stays clean**: Only merge tested, complete work
- **Archive completed tasks**: Keep task history for future reference
