# Before Dev - Development Guidelines Checklist

Read the relevant development guidelines before starting your task.

---

## Two-Layer Checklist

Before writing code, you MUST understand **both layers**:

| Layer | Answers | Action |
|-------|---------|--------|
| **Blueprint** | "Why?" - Architecture intent | Read first |
| **Spec** | "How?" - Coding conventions | Read second |

---

## Step 1: Read Blueprint (Architecture Intent)

**Read the project blueprint to understand WHY the architecture is designed this way:**

```bash
cat .bwflow/blueprint/README.md              # Root blueprint - overall architecture
cat .bwflow/blueprint/<module>/README.md    # Module blueprint - specific module intent
```

**Blueprint questions to answer:**
- What is the module's responsibility?
- What are the key design decisions?
- Why was this approach chosen over alternatives?

---

## Step 2: Discover Packages and Spec Layers

```bash
python3 ./.bwflow/scripts/get_context.py --mode packages
```

Identify which specs apply to your task based on:
- Which package you're modifying (e.g., `cli/`, `docs-site/`)
- What type of work (backend, frontend, unit-test, docs, etc.)

---

## Step 3: Read Spec Index

```bash
cat .bwflow/spec/<package>/<layer>/index.md   # Package-specific guidelines
cat .bwflow/spec/guides/index.md             # Thinking guides (always read)
```

Follow the **"Pre-Development Checklist"** section in the index.

---

## Step 4: Read Specific Guidelines

Read the specific guideline files listed in the Pre-Development Checklist:

**Common spec files:**
- `error-handling.md` - Error handling patterns
- `conventions.md` - Code style and conventions
- `mock-strategies.md` - Testing patterns
- `directory-structure.md` - Where files should go

The index is NOT the goal — it points you to the actual guideline files.

---

## Step 5: Read Module Blueprint (if applicable)

If your task involves a specific module:

```bash
cat .bwflow/blueprint/<module>/README.md
```

This gives you the **context** for implementation decisions.

---

## Development Readiness Checklist

Before writing any code, confirm you can answer:

### Blueprint Questions
- [ ] What is the module's primary responsibility?
- [ ] What design decisions should I be aware of?
- [ ] What are the key entry points?

### Spec Questions
- [ ] What coding style should I follow?
- [ ] What error handling patterns are used?
- [ ] Where should I place new files?
- [ ] What testing patterns are expected?

---

## Blueprint + Spec Integration Example

When implementing a new feature:

```
1. Read blueprint (why)
   → Understand module responsibility
   → Understand design decisions

2. Read spec (how)
   → Follow coding conventions
   → Use established patterns

3. Implement
   → Code that respects architecture (blueprint)
   → Code that follows conventions (spec)
```

---

## Command Reference

| Command | Purpose |
|--------|---------|
| `/bw start` | Start session (reads blueprints) |
| `/bw finish` | Complete task (validates against specs) |
| `/bw brainstorm` | Explore requirements + blueprints |

This step is **mandatory** before writing any code.
