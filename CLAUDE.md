# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## 项目概述

`claude-shadow-context` 是一个蓝图驱动的人机共识层。

它不再追求成为完整的 Claude 工作流框架，而是聚焦在两个更小、更核心的问题：

1. 让 AI 在更短上下文中理解项目结构、职责与架构意图
2. 让这种理解在任务结束后仍然保持可信

换句话说，这个项目关注的是 **shared understanding**，而不是大而全的 agent orchestration。

## 核心能力

当前版本围绕三个原语组织：

1. **`init`** (`skills/init/`)
   - 为项目初始化蓝图层，生成根蓝图和模块入口蓝图
   - 渐进式生成：文件级蓝图由 explore 按需补齐
   - 适用于新项目或大型项目中途介入

2. **`explore`** (`skills/explore/`)
   - 在进入任务前，优先通过蓝图收敛最相关上下文
   - 阅读顺序应为：根入口 → 业务入口 → 精准蓝图 → 必要代码
   - 目标是用最少上下文获得足够准确的项目理解

2. **`explore`** (`skills/explore/`)
   - 在进入任务前，优先通过蓝图收敛最相关上下文
   - 阅读顺序应为：根入口 → 业务入口 → 精准蓝图 → 必要代码
   - 目标是用最少上下文获得足够准确的项目理解

3. **`align`** (`skills/align/`)
   - 在任务结束、会话结束、准备提交前，检查蓝图是否仍与代码对齐
   - 输入可以来自会话上下文、修改文件以及 `git diff` / `git log`
   - 目标是识别蓝图漂移，并在必要时做轻量同步

## Hooks 架构

插件默认只保留 3 个 hook：

1. **`UserPromptSubmit`**
   - 当用户开始分析项目或修改代码时，提醒优先使用 `explore`

2. **`SubagentStart`**
   - 当子 agent 启动时，注入同样的蓝图优先上下文

3. **`SessionEnd`**
   - 当会话结束时异步触发对齐检查入口，为下一次进入任务保留“先检查蓝图”的提醒

## 设计原则

1. **蓝图优先**：优先读取意图层，而不是先散搜实现层
2. **最小上下文**：读取所有相关蓝图（蓝图本身就是精简的意图层），只在必要时补看代码
3. **结束对齐**：每次任务结束都应考虑蓝图是否仍然可信
4. **轻量协议**：不追求完整框架，只保留最小闭环

## 重要边界

- 这个项目不做通用 memory 系统
- 不做多角色 agent 平台
- 不做全家桶式自动化编排
- 不试图替代业务项目本身的代码结构

它的职责只有两件事：
- 帮助 AI 更快理解项目
- 帮助人和 AI 共同维护这份理解

## 代码关注点

当你修改这个仓库时，优先关注以下文件：

- `README.md`：对外定位与使用说明
- `hooks/hooks.json`：3 个 hook 的生命周期设计
- `scripts/remind-load.mjs`：用户提示词与子 agent 的蓝图提醒
- `scripts/session-align.mjs`：会话结束时的对齐入口
- `skills/init/SKILL.md`：初始化协议
- `skills/explore/SKILL.md`：探索协议
- `skills/align/SKILL.md`：对齐协议

## 当前实现状态

- `init`、`explore` 与 `align` 是主心智模型
- `bridge/mcp-server.cjs` 仍是占位实现，不是当前产品重点
- 如果未来需要更强的蓝图索引、映射、漂移检测，再考虑通过 MCP 扩展
