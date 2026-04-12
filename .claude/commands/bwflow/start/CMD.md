# bwflow:start

Initialize your AI development session and begin working on tasks.

---

## Operation Types

| Marker | Meaning | Executor |
|--------|---------|----------|
| `[AI]` | Bash scripts or Task calls executed by AI | You (AI) |
| `[USER]` | Slash commands executed by user | User |

---

## Initialization `[AI]`

### Step 1: Understand Development Workflow

First, read the workflow guide to understand the development process:

```bash
cat bwflow/workflow.md
```

**Follow the instructions in workflow.md** - it contains:
- Core principles (Blueprint First, Follow Standards, etc.)
- File system structure
- Development process
- Best practices

### Step 2: Get Current Context

```bash
python3 ./bwflow/scripts/get_context.py
```

This shows: developer identity, git status, current task (if any), active tasks.

### Step 3: Read Guidelines Index

```bash
cat bwflow/spec/frontend/index.md  # Frontend guidelines
cat bwflow/spec/backend/index.md   # Backend guidelines
cat bwflow/spec/guides/index.md    # Thinking guides
```

> **Important**: The index files are navigation — they list the actual guideline files and their Pre-Development Checklist.
> At this step, just read the indexes to understand what's available.
> When you start actual development, you MUST go back and read the specific guideline files.

### Step 4: Report and Ask

Report what you learned and ask: "What would you like to work on?"

---

## Task Classification

When user describes a task, classify it:

| Type | Criteria | Workflow |
|------|----------|----------|
| **Question** | User asks about code, architecture, or how something works | Answer directly |
| **Trivial Fix** | Typo fix, comment update, single-line change | Direct Edit |
| **Simple Task** | Clear goal, 1-2 files, well-defined scope | Quick confirm → Implement |
| **Complex Task** | Vague goal, multiple files, architectural decisions | **Brainstorm → Task Workflow** |

### Classification Signals

**Trivial/Simple indicators:**
- User specifies exact file and change
- "Fix the typo in X"
- "Add field Y to component Z"
- Clear acceptance criteria already stated

**Complex indicators:**
- "I want to add a feature for..."
- "Can you help me improve..."
- Mentions multiple areas or systems
- No clear implementation path
- User seems unsure about approach

### Decision Rule

> **If in doubt, use Brainstorm + Task Workflow.**

---

## Question / Trivial Fix

For questions or trivial fixes, work directly:

1. Answer question or make the fix
2. If code was changed, remind user to run `/bwflow:finish-work`

---

## Simple Task

For simple, well-defined tasks:

1. Quick confirm: "I understand you want to [goal]. Shall I proceed?"
2. If no, clarify and confirm again
3. **If yes: execute ALL steps below without stopping.**
   - Create task directory
   - Explore using blueprints (`/bwflow:explore`)
   - Implement
   - Check quality (`/bwflow:check`)
   - Complete

---

## Complex Task - Brainstorm First

For complex or vague tasks, **automatically start the brainstorm process**.

See `/bwflow:brainstorm` for the full process. Summary:

1. **Acknowledge and classify** - State your understanding
2. **Create task directory** - Track evolving requirements in `prd.md`
3. **Ask questions one at a time** - Update PRD after each answer
4. **Propose approaches** - For architectural decisions
5. **Confirm final requirements** - Get explicit approval
6. **Proceed to Task Workflow** - With clear requirements in PRD

---

## Task Workflow

### Phase 1: Establish Requirements

**Step 1: Create Task Directory**

```bash
TASK_DIR=$(python3 ./bwflow/scripts/task.py create "<title>" --slug <name>)
```

**Step 2: Explore using Blueprints**

```bash
/bwflow:explore
```

**Step 3: Write PRD**

Create `prd.md` in the task directory with:

```markdown
# <Task Title>

## Goal
<What we're trying to achieve>

## Requirements
- <Requirement 1>
- <Requirement 2>

## Acceptance Criteria
- [ ] <Criterion 1>
- [ ] <Criterion 2>

## Technical Notes
<Any technical decisions or constraints>
```

### Phase 2: Prepare for Implementation

**Step 4: Research the Codebase**

Based on the confirmed PRD, search relevant blueprints and specs:

```bash
cat bwflow/blueprint/README.md
cat bwflow/spec/<module>/index.md
```

**Step 5: Configure Context**

```bash
python3 ./bwflow/scripts/task.py init-context "$TASK_DIR" <type>
# type: backend | frontend | fullstack
```

**Step 6: Activate Task**

```bash
python3 ./bwflow/scripts/task.py start "$TASK_DIR"
```

### Phase 3: Execute

**Step 7: Implement**

Follow the blueprints and specs. Run lint/typecheck frequently.

**Step 8: Check Quality**

```bash
/bwflow:check
```

**Step 9: Complete**

1. Verify lint and typecheck pass
2. Report what was implemented
3. Remind user to:
   - Test the changes
   - Commit when ready
   - Run `/bwflow:align` to check blueprint alignment

---

## Continuing Existing Task

If `get_context.py` shows a current task:

1. Read the task's `prd.md` to understand the goal
2. Check `task.json` for current status
3. Ask user: "Continue working on <task-name>?"

---

## Commands Reference

### User Commands `[USER]`

| Command | When to Use |
|---------|-------------|
| `/bwflow:start` | Begin a session (this command) |
| `/bwflow:brainstorm` | Clarify vague requirements |
| `/bwflow:finish-work` | Before committing changes |
| `/bwflow:record-session` | After completing a task |

### AI Scripts `[AI]`

| Script | Purpose |
|--------|---------|
| `python3 ./bwflow/scripts/get_context.py` | Get session context |
| `python3 ./bwflow/scripts/task.py create` | Create task directory |
| `python3 ./bwflow/scripts/task.py start` | Set current task |
| `python3 ./bwflow/scripts/task.py finish` | Clear current task |

---

## Key Principle

> **Blueprint context is injected, not remembered.**
>
> The Task Workflow ensures agents receive relevant blueprint context automatically.
> This is more reliable than hoping the AI "remembers" conventions.
