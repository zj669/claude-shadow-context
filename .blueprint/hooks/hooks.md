# hooks.json 蓝图

## Metadata
- title: Bluefirst Hooks 配置
- type: config
- summary: 定义插件的 Hook 触发点，将"蓝图优先"从建议变成约束，在用户提交提示和 agent 结束时自动触发相关流程

## 配置说明

### UserPromptSubmit Hook
- 触发时机：用户提交新的提示词时
- 执行动作：运行 PowerShell 脚本 `remind-load.ps1`
- 目的：提醒 AI 优先使用 `/bluefirst-plugin:load` 加载蓝图上下文
- 超时时间：10 秒

### Stop Hook
- 触发时机：主 agent 结束时
- 执行动作：自动调用 `/bluefirst-plugin:sync` 同步蓝图
- 目的：确保代码修改后蓝图得到同步
- 超时时间：300 秒

### SubagentStop Hook
- 触发时机：子 agent 结束时
- 执行动作：自动调用 `/bluefirst-plugin:sync` 同步蓝图
- 目的：确保子 agent 的代码修改也能同步蓝图
- 超时时间：300 秒

## 设计意图

通过 Hooks 机制，将"蓝图优先"从文档建议提升为运行时约束：
1. 开始前提醒：确保 AI 先看蓝图再动手
2. 结束时同步：确保代码变更反映到蓝图层

## 变更记录
- 2026-03-08: 初始化蓝图，记录 Hooks 配置的架构意图
