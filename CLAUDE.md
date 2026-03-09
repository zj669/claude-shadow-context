# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

claude-shadow-context 是一个 Claude Code 插件，将"蓝图优先/影子架构"工作方法产品化为可安装的插件运行时。插件化的对象不是文档本身，而是**协议和流程**——让 AI 在修改代码前后都遵守"蓝图优先协议"。

## 核心架构

插件采用三层组合架构：

1. **Skills 层** (`skills/`)：提供 4 个用户可调用的入口
   - `init`：初始化项目的 `.blueprint/` 基础结构
   - `explore`：探索和熟悉代码上下文，加载相关蓝图（适用于任何需要理解代码的场景）
   - `sync`：代码修改后同步蓝图内容
   - `check`：检查蓝图与代码一致性，识别架构漂移

2. **Hooks 层** (`hooks/hooks.json`)：将"蓝图优先"从建议变成约束
   - `UserPromptSubmit`：提醒优先使用 explore 探索蓝图上下文
   - `SubagentStop`：子代理结束时联动 sync

3. **MCP 层** (`.mcp.json` + `bridge/`)：承载结构化能力
   - 当前 `bridge/mcp-server.cjs` 是占位实现
   - 未来将承载索引、校验、投影、漂移检测能力

## 蓝图模板结构

插件提供两个核心模板（`templates/`）：

- `meta.md`：极简通用蓝图模板，包含 Metadata、关键方法单元、变更记录
- `overview.md`：项目总览蓝图模板，包含项目目标、核心结构、关键方法单元

每个蓝图文件应包含统一元数据：
- `title`：蓝图标题
- `type`：类型（overview | module | flow | class | method）
- `summary`：主要能力描述

关键方法单元格式：
- `location`：代码位置
- `purpose`：存在目的
- `input`/`output`：输入输出
- `core_steps`：核心步骤

## 设计原则

1. **先瘦后胖**：第一版只做最小闭环（初始化、探索、同步、检查）
2. **协议优先**：插件是 Blueprint Runtime，不是文档包
3. **最小上下文**：不要把整个 `.blueprint/` 全部加载，按需加载 1-3 个相关文件
4. **漂移检测**：代码改动后必须检查蓝图是否需要同步

## 工作流建议

**重要：修改本项目代码前，请先查看 `.blueprint/` 目录下的蓝图文件，理解架构意图后再动手。**

标准蓝图优先工作流：
1. 收到需求 → 使用 `explore` 探索相关蓝图上下文
2. 理解架构意图 → 定位需要修改的代码
3. 修改代码 → 使用 `sync` 同步蓝图
4. 完成任务 → 使用 `check` 检查一致性

## 重要约束

- `.blueprint/` 是项目的架构意图层，由各项目自己维护
- 插件不替代项目代码，而是守护"蓝图优先协议"
- `files/` 镜像层适合作为检索增强层，不是默认主上下文
- 第一版只做轻量提醒与一次性收尾阻断，避免复杂自动化误判
- hook 命令依赖本机可执行 `node`
- hook 中使用的相对路径依赖插件目录结构保持不变

## 文档参考

- `docs/2026-03-08-claude-plugin-structure.md`：插件目录结构设计
- `docs/2026-03-08-blueprint-plugin-thoughts.md`：设计理念和判断
- `docs/plans/2026-03-08-plugin-skeleton.md`：实现计划
