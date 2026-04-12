# bwflow

> 蓝图驱动的结构化 AI 开发伴侣

bwflow 将**蓝图优先**的理解心智与**结构化工作流**深度融合，帮助 AI 在更短上下文中理解项目，并在任务结束后保持理解可信。

## 核心心智

### Blueprint vs Spec

bwflow 将项目知识分为两层：

| 问题 | 答案来自 |
|------|---------|
| 这个模块负责什么？ | `bwflow/blueprint/` — 蓝图层 |
| 代码应该怎么写？ | `bwflow/spec/` — 规范层 |
| 遇到这个错误怎么办？ | `bwflow/evolved/` — 进化技能 |
| 这次修改是否偏离了原设计？ | `/bwflow:align` — 蓝图对齐 |

### 工作流程

```
进入任务 → /bwflow:explore → 理解蓝图 → 实现 → /bwflow:align → 结束
```

1. **explore**：优先通过蓝图理解项目，而不是先散搜代码
2. **implement**：按蓝图理解执行实现
3. **align**：任务结束后检查蓝图是否仍与代码对齐

---

## 快速开始

### 1. 安装

```bash
npm install -g @zj669/bwflow
```

### 2. 初始化项目

```bash
cd my-project
bw init -u your-name
```

这会创建：

- `bwflow/` — 核心工作流目录
- `.claude/` — Claude Code 配置（自动同步）

### 3. 开始使用

```bash
/bwflow:start   # 启动会话（推荐）
```

或直接使用核心命令：

- `/bwflow:explore` — 探索项目上下文
- `/bwflow:align` — 检查蓝图对齐

---

## 命令参考

### 会话管理

| 命令 | 用途 |
|------|------|
| `/bwflow:start` | 启动会话，初始化上下文 |
| `/bwflow:finish-work` | 提交前检查清单 |
| `/bwflow:record-session` | 记录本次会话 |

### 任务管理

| 命令 | 用途 |
|------|------|
| `/bwflow:plan` | 分析需求，生成 PRD |
| `/bwflow:brainstorm` | 头脑风暴，需求发现 |
| `/bwflow:parallel` | 并行任务管理 |

### 开发流程

| 命令 | 用途 |
|------|------|
| `/bwflow:init` | 初始化项目蓝图层 |
| `/bwflow:explore` | 蓝图优先探索 |
| `/bwflow:align` | 蓝图对齐检查 |
| `/bwflow:before-dev` | 开发前准备 |

### 质量检查

| 命令 | 用途 |
|------|------|
| `/bwflow:check` | 代码质量检查 |
| `/bwflow:check-cross-layer` | 跨层影响检查 |
| `/bwflow:break-loop` | 调试后的深度分析 |

---

## 目录结构

```
{project}/
├── bwflow/
│   ├── blueprint/       ← 蓝图层（回答"为什么"）
│   │   ├── README.md
│   │   └── {module}/
│   ├── commands/        ← 命令协议
│   │   ├── start/
│   │   ├── explore/
│   │   ├── align/
│   │   └── ...
│   ├── agents/          ← 多角色 Agent 模板
│   ├── hooks/           ← 生命周期钩子
│   ├── scripts/         ← Python 执行脚本
│   ├── tasks/           ← 任务目录
│   ├── workspace/       ← 会话日志
│   ├── spec/           ← 编码规范（回答"怎么写"）
│   └── evolved/         ← 自我学习技能
├── .claude/             ← Claude Code 配置
└── packages/
    └── cli/             ← NPM CLI 工具
```

---

## 设计原则

1. **蓝图优先**：优先读取意图层（`bwflow/blueprint/`），而不是先散搜实现层
2. **最小上下文**：蓝图足够时，不扩读实现细节
3. **结束对齐**：每次任务结束都应考虑蓝图是否仍然可信
4. **自我学习**：从失败中沉淀 Evolved Skills

---

## Blueprint 模板

文件级蓝图严格遵循三段式结构：

```markdown
# {文件名} 蓝图

## Metadata
- title: 蓝图标题
- type: 类型标识（class | module | service | controller | util）
- summary: 一句话描述主要职责和能力

## 关键方法单元（只有核心业务文件才会有）
- location: 代码位置
- purpose: 方法存在的目的
- input / output
- core_steps: 核心业务步骤

## 变更记录
- YYYY-MM-DD: 变更摘要
```

---

## CLI 参考

```bash
bw init              # 初始化项目
bw sync              # 同步配置到各平台
bw upgrade           # 升级模板
```

---

## License

MIT
