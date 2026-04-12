# bwflow:finish-work

Pre-commit checklist before submitting or committing changes.

**Timing**: After code is written and tested, before commit

---

## Checklist

### 1. Code Quality

```bash
# Run lint and typecheck
pnpm lint
pnpm type-check
pnpm test
```

- [ ] `pnpm lint` passes with 0 errors?
- [ ] `pnpm type-check` passes with no type errors?
- [ ] Tests pass?
- [ ] No `console.log` statements (use logger)?
- [ ] No `any` types?

### 2. Blueprint Alignment

**CRITICAL**: Check if your code changes align with existing blueprints.

```bash
/bwflow:align
```

- [ ] Blueprint alignment checked?
- [ ] No significant drift from original architecture?

### 3. Spec Sync

If you discovered new patterns or conventions:

- [ ] Does `bwflow/spec/` need updates?
- [ ] New patterns documented?

### 4. Cross-Layer Verification

If the change spans multiple layers:

- [ ] Data flows correctly through all layers?
- [ ] Error handling works at each boundary?
- [ ] Types are consistent across layers?

### 5. Manual Testing

- [ ] Feature works in browser/app?
- [ ] Edge cases tested?
- [ ] Error states tested?

---

## Quick Check Flow

```bash
# 1. Code checks
pnpm lint && pnpm type-check

# 2. Blueprint alignment
/bwflow:align

# 3. View changes
git status
git diff --name-only
```

---

## Common Oversights

| Oversight | Consequence | Check |
|-----------|-------------|-------|
| Blueprint not updated | Architecture drift | `/bwflow:align` |
| Spec docs not updated | Others don't know the change | Check `bwflow/spec/` |
| Console.log left in | Noisy production logs | Search for console.log |
| Types not synced | Runtime errors | Check shared types |

---

## Core Principle

> **Delivery includes not just code, but also documentation and verification.**

Complete work = Code + Docs + Tests + Verification

---

## Relationship to Other Commands

```
Development Flow:
  Write code -> Test -> /bwflow:finish-work -> git commit -> /bwflow:record-session
                          |                              |
                   Ensure completeness              Record progress
```

- `/bwflow:finish-work` - Check work completeness (this command)
- `/bwflow:align` - Blueprint alignment check
- `/bwflow:record-session` - Record session and commits
