---
name: start-session
description: Start a bwflow development session. Load project context and current task.
inclusion: manual
---

# Start Session (bwflow)

Execute this command to get project context:

```bash
python3 .bwflow/scripts/get_context.py
```

## Next Steps

1. Review the context above
2. Select a task to work on (or create new task)
3. Begin development following bwflow workflow

## Available Agents

- Implement: `/agent swap implement`
- Check: `/agent swap check`
- Debug: `/agent swap debug`
- Dispatch: `/agent swap dispatch`

## Creating a New Task

```bash
python3 .bwflow/scripts/task.py create "Task Title" --slug task-name
python3 .bwflow/scripts/task.py init-context .bwflow/tasks/<task-dir> backend
```

## Workflow Overview

1. **Plan** - Analyze requirements, generate PRD
2. **Implement** - Code implementation following specs
3. **Check** - Quality checks and fixes
4. **Finish** - Pre-commit checklist and session recording
