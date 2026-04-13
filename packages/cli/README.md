# bwflow

> Blueprint Workflow - 蓝图驱动的 AI 开发伴侣，基于 Trellis 构建

```
$ bw init
✅ 初始化完成

$ /bw start
📋 读取上下文...
🚀 开始会话
```

## 为什么需要 bwflow？

| 痛点 | bwflow 解决方案 |
|------|------------------|
| AI 不理解项目架构 | Blueprint 层沉淀架构意图 |
| 每次都要重复解释规范 | Spec 层统一注入上下文 |
| 任务上下文丢失 | 任务 + 会话连续性 |
| Agent 实现质量不一 | Subagent 循环验证 |

## Quick Start

```bash
# 安装
npm install -g @zj669/bwflow

# 初始化项目
bw init

# Claude Code 中使用
/bw start
```

## Features

| 功能 | 说明 |
|------|------|
| **Blueprint 层** | 架构意图，设计决策文档化 |
| **Spec 层** | 编码标准自动注入上下文 |
| **8 个命令** | start, before-dev, finish 等 |
| **子 Agent 支持** | Implement / Check / Debug |
| **Ralph Loop** | Check Agent 循环验证直到通过 |
| **会话连续性** | Journal + Task 追踪 |

## Commands

### Claude Code

| 命令 | 说明 |
|------|------|
| `/bw start` | 开始会话，读取上下文 |
| `/bw before-dev` | 开发前检查规范 |
| `/bw finish` | 完成任务，验证质量 |
| `/bw record` | 记录会话摘要 |
| `/bw brainstorm` | 需求探索 |
| `/bw check` | 代码检查 |
| `/bw parallel` | 并行任务 |
| `/bw update-spec` | 更新规范 |

### CLI

```bash
bw init    # 初始化项目
bw sync    # 同步配置
```

## Architecture

```
.bwflow/                    # 核心工作流
├── blueprint/               # 架构蓝图 (新增)
├── spec/                    # 编码规范
├── tasks/                   # 任务追踪
├── workspace/                # 会话记忆
├── workflow.md              # 工作流规则
└── scripts/                 # Python 工具
    ├── task.py             # 任务管理
    ├── get_context.py       # 上下文获取
    └── hooks/               # 生命周期钩子
        ├── session-start.py
        ├── inject-subagent-context.py
        ├── ralph-loop.py
        └── statusline.py

.claude/
└── commands/bwflow/        # Claude Code 命令
```

### 两层理解框架

| 层 | 回答 | 位置 |
|---|------|------|
| Blueprint | "为什么这样设计？" | `.bwflow/blueprint/` |
| Spec | "如何编写符合项目风格？" | `.bwflow/spec/` |

## Development Flow

```
/bw start      → 读取 Blueprint + Spec 索引
/bw before-dev → 开发前检查规范
[实现功能]
/bw finish     → 质量验证 + Blueprint 对齐
git commit
/bw record     → 记录会话
```

## License

MIT
