# Check - Code Quality Verification

Check if the code you just wrote follows the development guidelines and architecture blueprints.

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

For each changed file, check if it aligns with the blueprint:

```bash
# Read relevant blueprints
cat .bwflow/blueprint/README.md
cat .bwflow/blueprint/<module>/README.md
```

**Blueprint questions:**
- [ ] Does the new code match the module's responsibility?
- [ ] Are design decisions followed?
- [ ] Is the architecture intent respected?

### 3. Determine Which Spec Modules Apply

Based on the changed file paths:

```bash
python3 ./.bwflow/scripts/get_context.py --mode packages
```

### 4. Read the Spec Index

```bash
cat .bwflow/spec/<package>/<layer>/index.md
```

Follow the **"Quality Check"** section in the index.

### 5. Read Specific Guideline Files

Read the guideline files referenced in the Quality Check section:

- `quality-guidelines.md`
- `conventions.md`
- `error-handling.md`
- etc.

### 6. Run Lint and Typecheck

```bash
# For affected package
pnpm lint
pnpm type-check
```

### 7. Report and Fix

Report any violations found:
- Blueprint misalignment
- Convention violations
- Quality issues

Fix them directly if found.
