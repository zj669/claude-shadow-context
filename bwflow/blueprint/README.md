# 项目蓝图根入口

> Blueprint 是 bwflow 的理解层，回答"**为什么**这样做"。
> 代码是实现层，回答"**怎么做**"。

---

## 什么是蓝图

蓝图（Blueprint）是 bwflow 的核心心智之一。它用 Markdown 记录：

1. **模块职责** — 这个模块/文件负责什么，不负责什么
2. **边界** — 和哪些模块有依赖关系
3. **关键方法** — 核心业务逻辑的方法签名和核心步骤
4. **变更记录** — 架构层面的变化历史

蓝图不是文档，不是注释，而是**架构意图的压缩表达**。

---

## 阅读顺序

进入任务前，按以下顺序阅读蓝图：

```
根蓝图 (本文件)
    ↓
模块入口蓝图 (bwflow/blueprint/{module}/index.md)
    ↓
文件级蓝图 (bwflow/blueprint/{module}/{file}.md)
    ↓
必要代码 (仅在蓝图不足以支撑时)
```

---

## 模块地图

| 模块 | 路径 | 职责 |
|------|------|------|
| **scripts** | `scripts/` | Python 执行脚本，任务管理、上下文获取、会话记录 |
| **hooks** | `hooks/` | 生命周期钩子，SessionStart、SubagentStop 等 |
| **agents** | `agents/` | 多角色 Agent 模板，plan/implement/check/dispatch |
| **commands** | `bwflow/commands/` | 命令协议，init/explore/align/plan 等 |
| **spec** | `bwflow/spec/` | 编码规范，回答"怎么写" |
| **blueprint** | `bwflow/blueprint/` | 蓝图层，回答"为什么" |

---

## 核心原则

1. **蓝图优先**：进入任务前，先读蓝图理解意图，再读代码
2. **最小上下文**：蓝图足够时，不扩读实现细节
3. **结束对齐**：任务结束后，检查蓝图是否仍然可信

---

