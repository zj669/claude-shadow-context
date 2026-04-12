# @zj669/bwflow

Blueprint Workflow CLI - 基于 Trellis + 蓝图层 的 AI 开发伴侣。

## 特性

- **完整 Trellis 功能**：14 个命令、多 Agent 支持、任务管理
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

## Claude Code 命令

在 Claude Code 中使用 `/bw` 前缀调用：

| 命令 | 说明 |
|------|------|
| `/bw start` | 开始会话 |
| `/bw before-dev` | 开发前读取规范 |
| `/bw finish` | 完成任务检查 |
| `/bw record` | 记录会话 |
| `/bw brainstorm` | 需求探索 |
| `/bw check` | 通用检查 |
| `/bw check-cross-layer` | 跨层检查 |
| `/bw create-command` | 创建命令 |
| `/bw integrate-skill` | 集成技能 |
| `/bw onboard` | 新人引导 |
| `/bw parallel` | 并行任务 |
| `/bw break-loop` | 跳出循环 |
| `/bw update-spec` | 更新规范 |

## 开发流程

```
/bw start      -> 开始会话
/bw before-dev -> 开发前读取规范
[实现功能]
/bw finish     -> 提交前检查
git commit
/bw record     -> 记录会话
```

## 目录结构

```
bwflow/
├── blueprint/              # 架构蓝图 (新增)
├── spec/                  # 编码规范
├── commands/              # 命令协议 (14个)
├── hooks/                # 生命周期钩子
├── tasks/                # 任务目录
├── sessions/             # 会话记录
├── archive/              # 归档
└── scripts/              # Python 脚本 (Trellis)

.claude/
└── commands/bwflow/      # Claude Code 命令
```

## License

MIT
