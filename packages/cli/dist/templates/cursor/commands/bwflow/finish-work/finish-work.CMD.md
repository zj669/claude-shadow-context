# Finish Work - Pre-Commit Checklist

Before submitting or committing, use this checklist.

---

## Two-Layer Completion Check

| Layer | Check | Update if Needed |
|-------|-------|-----------------|
| **Blueprint** | Does code match architecture intent? | `.bwflow/blueprint/<module>/` |
| **Spec** | Does code follow conventions? | `.bwflow/spec/<layer>/` |

---

## Checklist

### 1. Code Quality

```bash
pnpm lint
pnpm type-check
pnpm test
```

- [ ] `pnpm lint` passes?
- [ ] `pnpm type-check` passes?
- [ ] Tests pass?
- [ ] No `console.log` statements?
- [ ] No non-null assertions (`x!`)?
- [ ] No `any` types?

### 2. Test Coverage

- [ ] New pure function → unit test added?
- [ ] Bug fix → regression test added?
- [ ] Logic change → integration test updated?

### 3. Blueprint Sync

- [ ] New module → blueprint created?
- [ ] Changed responsibilities → blueprint updated?
- [ ] Architectural decisions → documented?

### 4. Spec Sync

- [ ] Backend specs updated?
- [ ] Frontend specs updated?
- [ ] Guides updated with lessons learned?

### 5. Manual Testing

- [ ] Feature works?
- [ ] Edge cases tested?
- [ ] Error states handled?

---

## Quick Check Flow

```bash
pnpm lint && pnpm type-check
git status
git diff --name-only
```
