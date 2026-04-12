# bwflow:finish

Complete the task and perform final cleanup.

**Timing**: After all implementation and checks pass

---

## Steps

### 1. Run finish-work checklist

```bash
/bwflow:finish-work
```

Ensure all items are checked.

### 2. Check blueprint alignment

```bash
/bwflow:align
```

Ensure blueprints are still trustworthy.

### 3. Record session

```bash
python3 ./bwflow/scripts/add_session.py \
  --title "Task Title" \
  --commit "abc1234" \
  --summary "Brief summary of what was done"
```

### 4. Archive task

```bash
python3 ./bwflow/scripts/task.py archive <task-name>
```

### 5. Clear current task

```bash
python3 ./bwflow/scripts/task.py finish
```

---

## Final Checklist

- [ ] `/bwflow:finish-work` completed
- [ ] `/bwflow:align` shows blueprints aligned
- [ ] Session recorded
- [ ] Task archived
- [ ] Current task cleared

---

## Core Principle

> **Task completion includes code + blueprint alignment + session recording.**
