---
name: finish-work
description: Pre-commit checklist. Runs final quality checks before creating PR.
inclusion: manual
---

# Finish Work (bwflow)

## Pre-Commit Checklist

### 1. Code Quality

- [ ] Lint checks pass
- [ ] Type checks pass
- [ ] Tests pass

### 2. Blueprint Alignment

- [ ] Changes align with blueprint intent
- [ ] No unintended architectural drift
- [ ] Blueprint updated if architecture changed

### 3. Documentation

- [ ] Update spec if new patterns introduced
- [ ] Update README if user-facing changes

### 4. Git Status

- [ ] All changes committed
- [ ] Commit messages follow convention (type(scope): description)

## Final Check

Switch to Check Agent with finish flag:

```
/agent swap check
```

Then tell it:

```
[finish] Execute final completion check before PR
```

## Record Session

After all checks pass:

```bash
python3 .bwflow/scripts/add_session.py --title "Session Title" --commit "abc1234"
```

## Create Pull Request

```bash
# Push to remote
git push origin <branch-name>

# Create PR (if using gh CLI)
gh pr create --title "PR Title" --body "Description"
```
