# Blueprint-First Thinking Guide

> **Purpose**: Always approach understanding through blueprints before diving into code.

---

## The Problem

AI coding tools often start by searching through code, which leads to:
- Incomplete understanding of project structure
- Missing context about why code exists
- Accidental deviation from original design

---

## Blueprint-First Workflow

### The Golden Path

```
1. Understand task → Read relevant blueprints
2. Blueprints insufficient → Explore少量代码
3. Make changes → Update affected blueprints
4. Before commit → Run align to check drift
```

### Why Blueprints First

Blueprints capture **intent**, not implementation:
- Why does this code exist?
- What problem does it solve?
- What are its boundaries?

Code shows **how**, blueprints show **why**.

---

## When to Use Blueprint-First

### Always Start With

- Understanding a new module
- Analyzing a bug report
- Planning a feature change
- Onboarding to a new area

### Skip Blueprints When

- The file has no blueprint (yet)
- This is the first time touching the area
- Blueprint clearly outdated (run `align` after)

---

## Blueprint Anatomy

Every blueprint has three sections:

### 1. Metadata
```markdown
## Metadata
- title: 模块名称
- type: class | module | service | controller | util
- summary: 一句话描述主要职责
```

### 2. 关键方法单元 (for core files only)
```markdown
## 关键方法单元
- location: 函数或方法名
- purpose: 为什么存在
- input: 参数类型
- output: 返回值类型
- core_steps: 核心业务步骤
```

### 3. 变更记录
```markdown
## 变更记录
- YYYY-MM-DD: 变更摘要
```

---

## Blueprint → Code Path Mapping

Blueprints mirror code structure:

| Code Path | Blueprint Path |
|-----------|---------------|
| `scripts/session-align.mjs` | `.blueprint/scripts/session-align.md` |
| `skills/explore/SKILL.md` | `.blueprint/skills/explore/SKILL.md` |
| `.claude/hooks/session-start.py` | `.blueprint/.claude/hooks/session-start.md` |

**Rule**: For every code file, there is exactly one blueprint file (same name, `.md` extension, `.blueprint/` prefix).

---

## Drift Detection

Blueprint drift happens when code changes but blueprint doesn't.

### Signs of Drift

- Blueprint describes methods that no longer exist
- Blueprint shows old parameter types
- Blueprint is missing new functionality
- Code behavior contradicts blueprint summary

### When Drift Occurs

1. **Code change**: Someone modifies code without updating blueprint
2. **Refactoring**: Method renamed but blueprint not updated
3. **New feature**: New methods added but blueprint unchanged

### Prevention: Run Align Before Commit

```
Before commit:
  /claude-shadow-context:align

Output:
  - 对齐状态: 警告
  - 缺失蓝图: .blueprint/.claude/hooks/ralph-loop.md
  - 漂移蓝图: .blueprint/scripts/session-align.md (buildSummary新增参数)
```

---

## Progressive Blueprint Creation

### Small Projects (< 50 code files)
- Create root blueprint + module blueprints during `init`
- File-level blueprints for core business logic
- Remaining files get blueprints on-demand via `align`

### Large Projects (50+ code files)
- Create root blueprint + module blueprints during `init`
- File-level blueprints created only when touched by a session
- `align` creates missing blueprints from code understanding

---

## Checklist for Blueprint Maintenance

Before commit:
- [ ] Changed code reflects updated intent
- [ ] Blueprint metadata still accurate
- [ ] New methods added to 关键方法单元
- [ ] Changed methods updated in 关键方法单元
- [ ] Entry added to 变更记录

---

## Integration with bwflow Workflow

Blueprint-first is complementary to bwflow's spec system:

| Layer | Purpose | When to Use |
|-------|---------|-------------|
| Blueprint | Intent and understanding | Before touching code |
| Spec | Coding conventions and patterns | When writing code |
| PRD | Requirements and scope | Before implementation |

**Flow**: Blueprint-first (explore) → Spec-guided (implement) → Align (verify)
