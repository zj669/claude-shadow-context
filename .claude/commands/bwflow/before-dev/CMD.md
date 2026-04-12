# bwflow:before-dev

Read the relevant development guidelines before starting your task.

**Timing**: Before writing any code

---

## Steps

### 1. Discover available guidelines

```bash
cat bwflow/spec/frontend/index.md  # Frontend guidelines
cat bwflow/spec/backend/index.md   # Backend guidelines
cat bwflow/spec/guides/index.md    # Thinking guides
```

### 2. Identify which specs apply to your task

Based on:
- Which module you're modifying
- What type of work (backend, frontend, fullstack)

### 3. Read the spec index for each relevant module

```bash
cat bwflow/spec/<module>/index.md
```

Follow the **"Pre-Development Checklist"** section in the index.

### 4. Read the specific guideline files

The index is NOT the goal — it points you to the actual guideline files.

Read those files to understand the coding standards and patterns.

### 5. Always read shared guides

```bash
cat bwflow/spec/guides/index.md
```

### 6. Read the Blueprint Layer

For understanding the architecture intent:

```bash
cat bwflow/blueprint/README.md
cat bwflow/blueprint/<module>/index.md
```

### 7. Understand and proceed

Understand the coding standards and patterns you need to follow, then proceed with your development plan.

---

## Pre-Development Checklist

Before writing any code:

- [ ] Read `bwflow/spec/` relevant guidelines
- [ ] Read `bwflow/blueprint/` for architecture understanding
- [ ] Understand coding standards and patterns
- [ ] Ready to implement

---

## Core Principle

> **Read Before Write** — Understand context before starting development.
