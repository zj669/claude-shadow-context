# @zj669/bwflow

Blueprint Workflow CLI - 基于 Trellis + 蓝图层 的 AI 开发伴侣。

## 特性

- **完整 Trellis 功能**：8 个核心命令、任务管理
- **蓝图层**：架构意图沉淀，模块职责清晰
- **规范层**：编码标准统一，代码风格一致

## 安装

```bash
npm install -g @zj669/bwflow
```

## CLI 命令

| 命令 | 说明 |
|------|------|
| `bw init` | 初始化项目（创建 bwflow/ 目录，同步到 Claude Code） |
| `bw sync` | 同步配置 |

## Claude Code 命令（8 个）

在 Claude Code 中使用 `/bw` 前缀调用：

| 命令 | 说明 |
|------|------|
| `/bw start` | 开始会话 |
| `/bw before-dev` | 开发前读取规范 |
| `/bw finish` | 完成任务检查 |
| `/bw record` | 记录会话 |
| `/bw brainstorm` | 需求探索 |
| `/bw check` | 通用检查 |
| `/bw parallel` | 并行任务 |
| `/bw update-spec` | 更新规范 |

## 蓝图层（Blueprint Layer）

bwflow 新增架构意图层：

| 层级 | 回答 | 位置 |
|------|------|------|
| **Blueprint** | "为什么？" - 架构意图、设计决策 | `bwflow/blueprint/` |
| **Spec** | "怎么做？" - 编码标准、模式、规范 | `bwflow/spec/` |

**阅读顺序**：先读 Blueprint（理解意图）→ 再读 Spec（遵循规范）

## 开发流程

```
/bw start      -> 开始会话（读取蓝图）
/bw before-dev -> 开发前读取规范
[实现功能]
/bw finish     -> 提交前检查（蓝图对齐）
git commit
/bw record     -> 记录会话（包含蓝图变更）
```

## 目录结构

```
bwflow/
├── blueprint/              # 架构蓝图 (新增)
│   └── README.md         # 根蓝图
├── spec/                  # 编码规范
├── commands/              # 命令协议 (8个)
├── hooks/                 # 生命周期钩子
├── tasks/                 # 任务目录
├── sessions/              # 会话记录
├── archive/               # 归档
└── scripts/               # Python 脚本 (Trellis)

.claude/
└── commands/bwflow/     # Claude Code 命令
```

## License

MIT
