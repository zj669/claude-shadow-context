# Skills 层架构说明

## 模块职责

Skills 层是 Bluefirst 插件的用户交互入口，提供 4 个核心命令，实现"蓝图优先"工作流的完整闭环。

## 核心命令

### init - 初始化
- 路径：`skills/init/SKILL.md`
- 职责：为项目初始化蓝图结构，生成根入口和蓝图镜像
- 使用时机：项目首次使用 Bluefirst 插件时
- 蓝图：`.blueprint/skills/init/SKILL.md`

### explore - 探索上下文
- 路径：`skills/explore/SKILL.md`
- 职责：探索和熟悉代码上下文，快速收敛到最相关的蓝图与代码
- 使用时机：任何需要理解代码的时候（熟悉项目、查找功能、分析需求、修复问题、开发功能前）
- 蓝图：`.blueprint/skills/explore/SKILL.md`

### sync - 同步蓝图
- 路径：`skills/sync/SKILL.md`
- 职责：代码修改后，将有意义的变化同步回蓝图
- 使用时机：代码修改后，由 Stop Hook 自动触发或手动调用
- 蓝图：`.blueprint/skills/sync/SKILL.md`

### check - 检查一致性
- 路径：`skills/check/SKILL.md`
- 职责：检查蓝图与代码的一致性，识别架构漂移
- 使用时机：任务结束前、提交代码前、定期审查时
- 蓝图：`.blueprint/skills/check/SKILL.md`

## 工作流闭环

```
用户需求
   ↓
[explore] 探索蓝图上下文
   ↓
理解架构意图
   ↓
修改代码
   ↓
[sync] 同步蓝图（自动触发）
   ↓
[check] 检查一致性
   ↓
完成任务
```

## 设计原则

1. **最小闭环**：4 个命令覆盖初始化、探索、同步、检查的完整流程
2. **协议优先**：通过 Hooks 将建议变成约束
3. **轻量实现**：第一版只做核心功能，避免过度设计

## 相关文档

- 项目根 CLAUDE.md：项目整体架构说明
- `.blueprint/` 目录：本项目的蓝图镜像层
- `hooks/hooks.json`：Hooks 配置，联动 Skills 层
