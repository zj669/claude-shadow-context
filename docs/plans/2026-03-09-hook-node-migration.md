# Hook Node 迁移 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 将 `UserPromptSubmit` 的提醒 Hook 从 PowerShell 脚本迁移到跨平台的 Node 脚本，同时保持现有提醒行为稳定。

**Architecture:** 保留现有 Hook 触发时机与提示语义，仅把 `stdin JSON -> 判断 -> stdout JSON` 的处理逻辑迁移到 `scripts/remind-load.mjs`。使用 Node 内置测试验证空输入、跳过条件和正常注入场景，再切换 `hooks/hooks.json` 到 Node 命令并移除旧的 PowerShell 脚本。

**Tech Stack:** Node.js ESM、`node:test`、JSON Hook 配置

---

### Task 1: 建立回归测试

**Files:**
- Create: `scripts/remind-load.test.mjs`

**Step 1: 写出失败测试**

- 用 `node:test` 编写 4 个场景：空输入、已包含 `/bluefirst-plugin:explore`、已包含 `.blueprint/` 或 `.blueprint\\`、普通提示词。

**Step 2: 运行测试确认失败**

- 运行 `node --test scripts/remind-load.test.mjs`
- 预期：因 `scripts/remind-load.mjs` 尚不存在而失败。

### Task 2: 实现跨平台 Node Hook

**Files:**
- Create: `scripts/remind-load.mjs`
- Modify: `scripts/remind-load.test.mjs`

**Step 1: 写最小实现**

- 读取 stdin
- 安全解析 JSON
- 抽取 `prompt`
- 判断是否跳过
- 输出结构化 JSON 或静默退出

**Step 2: 运行测试确认通过**

- 运行 `node --test scripts/remind-load.test.mjs`

### Task 3: 切换 Hook 配置并清理旧实现

**Files:**
- Modify: `hooks/hooks.json`
- Delete: `scripts/remind-load.ps1`
- Modify: `README.md`

**Step 1: 切换命令**

- 将 Hook 命令改为 `node "./scripts/remind-load.mjs"`

**Step 2: 更新文档**

- 将 Hook 运行时描述从 PowerShell/Bash 统一为 Node 脚本实现

**Step 3: 删除旧脚本**

- 删除 `scripts/remind-load.ps1`

### Task 4: 完整验证

**Files:**
- Verify: `scripts/remind-load.test.mjs`
- Verify: `hooks/hooks.json`

**Step 1: 运行测试**

- 运行 `node --test scripts/remind-load.test.mjs`

**Step 2: 手工验证 Hook 输出**

- 用 `echo`/管道传入示例 JSON，确认脚本输出与退出码符合预期。
