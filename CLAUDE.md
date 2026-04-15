# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## 项目概述

**bwflow** 是一个蓝图驱动的 AI 协作 CLI 工具,解决两大核心问题:

1. **上下文爆炸** — 用蓝图层压缩架构意图,让 AI 在更短上下文中理解项目
2. **理解漂移** — 任务结束后通过 align 检查蓝图是否仍与代码对齐

**本质**: 这是一个 NPM CLI 工具,为项目生成 `.bwflow/` 核心结构 + 平台特定配置(`.claude/` / `.cursor/` / `.kiro/`)。

---

## 架构分层

```
项目根目录/
├── bwflow/                    # 核心工作流目录(被 CLI 复制到用户项目)
│   ├── blueprint/            # 蓝图层 — 回答"为什么这样设计"
│   │   └── README.md        # 根蓝图入口
│   ├── spec/                # 规范层 — 回答"如何编写符合项目风格的代码"
│   │   ├── backend/         # Python/JS 脚本规范
│   │   ├── frontend/        # 前端规范(如适用)
│   │   └── guides/          # 思维指南(code-reuse/cross-layer/blueprint-first)
│   ├── scripts/             # Python 执行脚本(任务管理/上下文获取/会话记录)
│   ├── tasks/               # 任务目录
│   ├── workspace/           # 会话日志
│   ├── evolved/             # 自我学习技能
│   ├── config.yaml          # 配置文件
│   └── workflow.md          # 开发工作流文档

src/                          # CLI 源码(TypeScript)
├── commands/
│   ├── init.ts              # 初始化命令 — 复制 bwflow/ 到用户项目
│   └── upgrade.ts           # 升级命令
├── templates/               # 平台模板
│   ├── claude/              # Claude Code 模板
│   │   ├── commands/bw/    # 9个命令: start/finish-work/check/brainstorm/parallel/...
│   │   ├── agents/          # 6个角色: plan/implement/check/debug/research/dispatch
│   │   └── hooks/           # session-start.py
│   ├── cursor/              # Cursor 模板(结构同上)
│   └── kiro/                # Kiro 模板(结构同上)
└── index.ts                 # CLI 入口

dist/                         # 编译产物
package.json                 # NPM 包配置(@zj669/bwflow)
```

---

## 核心工作流

```
用户执行: bw init -t claude -u <name>
    ↓
CLI 复制 bwflow/ → 用户项目/.bwflow/
CLI 复制 src/templates/claude/ → 用户项目/.claude/
    ↓
用户在 Claude Code 中执行: /bw start
    ↓
读取 .bwflow/workflow.md + blueprint/ + spec/
    ↓
开发 → /bw check → /bw finish-work → 提交
```

---

## 可用命令(Claude Code)

**会话管理**:
- `/bw start` — 启动会话,初始化上下文
- `/bw finish-work` — 提交前检查清单
- `/bw record-session` — 记录本次会话

**任务管理**:
- `/bw brainstorm` — 头脑风暴,需求发现
- `/bw parallel` — 并行任务管理

**开发流程**:
- `/bw before-dev` — 开发前准备
- `/bw check` — 代码质量检查
- `/bw update-spec` — 更新规范层
- `/bw onboard` — 新成员入职引导

---

## 可用 Agent 角色

- `plan` — 需求分析,生成 PRD
- `implement` — 实现阶段
- `check` — 质量检查
- `debug` — 调试分析
- `research` — 研究探索
- `dispatch` — 任务分发

---

## 核心原则

1. **蓝图优先** — 优先读取 `.bwflow/blueprint/`,而不是先散搜代码
2. **最小上下文** — 蓝图足够时,不扩读实现细节
3. **结束对齐** — 每次任务结束检查蓝图是否仍然可信
4. **规范驱动** — 开发前必读 `.bwflow/spec/` 相关规范

---

## 开发此项目时的注意事项

### 目录职责

- **bwflow/** — 核心工作流,会被复制到用户项目的 `.bwflow/`
- **src/templates/** — 平台特定模板,会被复制到用户项目的 `.claude/` / `.cursor/` / `.kiro/`
- **src/commands/** — CLI 命令实现

### 修改模板时

1. 修改 `src/templates/claude/commands/bw/*.md` 后需运行 `npm run build`
2. 修改 `bwflow/` 内容后需运行 `npm run build` 复制到 `dist/`
3. 测试时在其他项目执行 `bw init -t claude` 验证

### 技术栈

- **CLI**: TypeScript + Commander + Chalk
- **bwflow 脚本**: Python 3.10+ (仅 stdlib)
- **模板系统**: Markdown + YAML
- **发布**: NPM 包 `@zj669/bwflow`

---

## CLI 使用

```bash
# 安装
npm install -g @zj669/bwflow

# 初始化项目(必须指定类型)
bw init -t claude -u <your-name>
bw init -t cursor -u <your-name>
bw init -t kiro -u <your-name>

# 同步(alias for init)
bw sync
```

---

## 设计哲学

**不是框架,是协议** — bwflow 不追求完整框架,只保留最小闭环:
- 蓝图层压缩架构意图
- 规范层统一编码标准
- 命令协议标准化工作流
- 会话记录保持上下文连续性
