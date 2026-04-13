# Finish Work - Pre-Commit Checklist

Before submitting or committing, use this checklist to ensure work completeness.

**Timing**: After code is written and tested, before commit

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
# Must pass
pnpm lint
pnpm type-check
pnpm test
```

- [ ] `pnpm lint` passes with 0 errors?
- [ ] `pnpm type-check` passes with no type errors?
- [ ] Tests pass?
- [ ] No `console.log` statements (use logger)?
- [ ] No non-null assertions (the `x!` operator)?
- [ ] No `any` types?

### 2. Test Coverage

Check if your change needs new or updated tests (see `.bwflow/spec/unit-test/conventions.md`):

- [ ] New pure function → unit test added?
- [ ] Bug fix → regression test added in `test/regression.test.ts`?
- [ ] Changed init/update behavior → integration test added/updated?
- [ ] No logic change (text/data only) → no test needed

### 3. Blueprint Sync (Architecture Intent)

**Does the code match the architecture blueprints?**

```bash
# Check changed files
git diff --name-only

# For each changed file, check if blueprint needs update:
# 1. New module? → Create blueprint
# 2. Changed responsibilities? → Update blueprint
# 3. New design decisions? → Update blueprint
```

**Blueprint check questions:**
- [ ] Did I create new modules? → Create blueprint for them
- [ ] Did I change module responsibilities? → Update blueprint
- [ ] Did I make architectural decisions? → Document in blueprint

**Key Question**:
> "If someone reads the blueprint, will they understand what this code does and why?"

If NO → Update the relevant blueprint.

### 4. Spec Sync (Coding Conventions)

**Code-Spec Docs**:
- [ ] Does `.bwflow/spec/backend/` need updates?
  - New patterns, new modules, new conventions
- [ ] Does `.bwflow/spec/frontend/` need updates?
  - New components, new hooks, new patterns
- [ ] Does `.bwflow/spec/guides/` need updates?
  - New cross-layer flows, lessons from bugs

**Key Question**:
> "If I fixed a bug or discovered something non-obvious, should I document it so future me (or others) won't hit the same issue?"

If YES -> Update the relevant code-spec doc.

### 5. Code-Spec Hard Block (Infra/Cross-Layer)

If this change touches infra or cross-layer contracts, this is a blocking checklist:

- [ ] Spec content is executable (real signatures/contracts), not principle-only text
- [ ] Includes file path + command/API name + payload field names
- [ ] Includes validation and error matrix
- [ ] Includes Good/Base/Bad cases
- [ ] Includes required tests and assertion points
- [ ] Blueprint documents the architectural decision

**Block Rule**:
In pipeline mode, the finish agent will automatically detect and execute spec updates when gaps are found.
If running this checklist manually, ensure spec and blueprint sync is complete before committing — run `/bw update-spec` if needed.

### 6. API Changes

If you modified API endpoints:

- [ ] Input schema updated?
- [ ] Output schema updated?
- [ ] API documentation updated?
- [ ] Client code updated to match?
- [ ] Blueprint documents the API design?

### 7. Database Changes

If you modified database schema:

- [ ] Migration file created?
- [ ] Schema file updated?
- [ ] Related queries updated?
- [ ] Seed data updated (if applicable)?
- [ ] Blueprint documents the data model?

### 8. Cross-Layer Verification

If the change spans multiple layers:

- [ ] Data flows correctly through all layers?
- [ ] Error handling works at each boundary?
- [ ] Types are consistent across layers?
- [ ] Loading states handled?
- [ ] Blueprint reflects the cross-layer design?

### 9. Manual Testing

- [ ] Feature works in browser/app?
- [ ] Edge cases tested?
- [ ] Error states tested?
- [ ] Works after page refresh?

---

## Quick Check Flow

```bash
# 1. Code checks
pnpm lint && pnpm type-check

# 2. View changes
git status
git diff --name-only

# 3. Check blueprint alignment
# - New modules created?
# - Responsibilities changed?
# - Design decisions made?

# 4. Check spec alignment
# - Coding conventions followed?
# - New patterns to document?

# 5. Based on changed files, check relevant items above
```

---

## Common Oversights

| Oversight | Consequence | Check |
|-----------|-------------|-------|
| Blueprint not updated | Others don't understand architecture | Check .bwflow/blueprint/ |
| Code-spec docs not updated | Others don't know the change | Check .bwflow/spec/ |
| Spec text is abstract only | Easy regressions in infra/cross-layer changes | Require signature/contract/matrix/cases/tests |
| Migration not created | Schema out of sync | Check db/migrations/ |
| Types not synced | Runtime errors | Check shared types |
| Tests not updated | False confidence | Run full test suite |
| Console.log left in | Noisy production logs | Search for console.log |

---

## Blueprint Update Example

If you created a new module `src/auth/`:

```markdown
# .bwflow/blueprint/src/auth.md

## 职责
用户认证模块，负责登录、注册、Token 管理

## 关键方法

| 方法 | 路径 | 说明 |
|------|------|------|
| login | src/auth/login.ts | 用户登录 |
| register | src/auth/register.ts | 用户注册 |
| verifyToken | src/auth/jwt.ts | Token 验证 |

## 设计意图

- 使用 JWT 进行身份验证
- 密码使用 bcrypt 加密
- Refresh Token 用于 token 续期

## Change Log
- 2024-04-13 Initial
```

---

## Relationship to Other Commands

```
Development Flow:
  Write code -> Test -> /bw finish -> git commit -> /bw record
                          |                              |
                   Ensure completeness              Record progress
                   
Debug Flow:
  Hit bug -> Fix -> /bw break-loop -> Knowledge capture
                       |
                  Deep analysis
```

- `/bw finish` - Check work completeness (this command)
- `/bw record` - Record session and commits
- `/bw break-loop` - Deep analysis after debugging

---

## Core Principles

> **Delivery includes not just code, but also documentation, verification, and knowledge capture.**

> **Blueprint answers "Why?", Spec answers "How?"**

Complete work = Code + Blueprint + Spec + Tests + Verification
