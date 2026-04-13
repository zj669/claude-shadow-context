# Check - Code Quality Verification

Check if the code follows development guidelines and architecture blueprints.

---

## Two-Layer Verification

| Layer | Check | Location |
|-------|-------|----------|
| **Blueprint** | Does code match architecture intent? | `.bwflow/blueprint/` |
| **Spec** | Does code follow conventions? | `.bwflow/spec/` |

---

## Steps

### 1. Identify Changed Files

```bash
git diff --name-only HEAD
```

### 2. Check Blueprint Alignment

```bash
cat .bwflow/blueprint/README.md
cat .bwflow/blueprint/<module>/README.md
```

### 3. Read Spec Index

```bash
cat .bwflow/spec/<package>/<layer>/index.md
```

### 4. Run Verification

```bash
pnpm lint
pnpm type-check
```

### 5. Report and Fix

Fix any violations directly.

---

## Completion Markers

After verification passes, output:
- `TYPECHECK_FINISH`
- `LINT_FINISH`
- `ALL_CHECKS_FINISH`
