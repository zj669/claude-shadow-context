# Start Session

Initialize your AI development session and begin working on tasks.

---

## Initialization

### Step 1: Understand Development Workflow

First, read the workflow guide:

```bash
cat .bwflow/workflow.md
```

### Step 2: Get Current Context

```bash
python3 ./.bwflow/scripts/get_context.py
```

### Step 3: Read Blueprint

```bash
cat .bwflow/blueprint/README.md              # Root blueprint
cat .bwflow/blueprint/src/README.md          # Source modules (if exists)
```

### Step 4: Read Guidelines Index

```bash
python3 ./.bwflow/scripts/get_context.py --mode packages
cat .bwflow/spec/<package>/<layer>/index.md   # Package-specific guidelines
cat .bwflow/spec/guides/index.md              # Thinking guides
```

---

## Task Classification

| Type | Criteria | Workflow |
|------|----------|----------|
| **Question** | User asks about code or architecture | Answer directly |
| **Trivial Fix** | Typo, single-line change | Direct Edit |
| **Simple Task** | Clear goal, 1-2 files | Quick confirm → Implement |
| **Complex Task** | Vague goal, multiple files | **Brainstorm → Task Workflow** |

---

## Simple Task

1. Confirm: "I understand you want to [goal]. Shall I proceed?"
2. Execute all steps:
   - Create task directory
   - Write PRD
   - Research + Blueprint
   - Configure context
   - Activate task
   - Implement
   - Check quality
   - Complete

---

## Complex Task - Brainstorm First

1. Acknowledge and classify
2. Create task directory
3. Ask questions one at a time
4. Propose approaches
5. Confirm requirements
6. Proceed to Task Workflow

---

## Task Workflow

### Phase 1: Requirements

```bash
TASK_DIR=$(python3 ./.bwflow/scripts/task.py create "<title>" --slug <name>)
# Write prd.md
```

### Phase 2: Prepare

```bash
python3 ./.bwflow/scripts/task.py init-context "$TASK_DIR" <type>
python3 ./.bwflow/scripts/task.py start "$TASK_DIR"
```

### Phase 3: Execute

```
Task(
  subagent_type: "implement",
  prompt: "Implement the task described in prd.md",
  model: "opus"
)
```

```
Task(
  subagent_type: "check",
  prompt: "Review and fix issues",
  model: "opus"
)
```

---

## Commands Reference

| Command | Purpose |
|---------|---------|
| `/bw start` | Begin session |
| `/bw brainstorm` | Clarify requirements |
| `/bw finish` | Pre-commit check |
| `/bw record` | Record session |
