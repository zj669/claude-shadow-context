# Cursor IDE - bwflow 模板

bwflow 蓝图驱动工作流在 Cursor IDE 上的配置模板。

## 目录结构

```
.cursor/                      # Cursor 配置文件
├── hooks.json                # Hook 配置
├── hooks/                    # Hook 脚本
│   ├── session-start.py      # 会话开始时注入上下文
│   ├── inject-subagent-context.py  # 子代理上下文注入
│   └── ralph-loop.py         # Check 代理循环控制
├── agents/                   # 子代理定义
│   ├── dispatch.md           # 调度代理
│   ├── implement.md         # 实现代理
│   ├── check.md             # 检查代理
│   ├── debug.md             # 调试代理
│   ├── research.md          # 研究代理
│   └── plan.md              # 计划代理
└── commands/bwflow/         # 命令协议
    ├── start/                # 开始会话
    ├── check/               # 代码检查
    ├── finish-work/         # 完成检查
    ├── brainstorm/          # 头脑风暴
    ├── parallel/            # 并行工作树
    ├── update-spec/         # 更新规范
    ├── record-session/      # 记录会话
    └── before-dev/          # 开发前准备
```

## 安装

### 1. 复制配置文件

```bash
# 复制 hooks 配置
cp .cursor/hooks.json <your-project>/.cursor/

# 复制 hooks 脚本
cp -r .cursor/hooks <your-project>/.cursor/

# 复制 agents 定义
cp -r .cursor/agents <your-project>/.cursor/

# 复制 commands
cp -r .cursor/commands <your-project>/.cursor/
```

### 2. 设置脚本执行权限

```bash
chmod +x .cursor/hooks/*.py
```

### 3. 重启 Cursor

Cursor 会自动加载 `hooks.json` 配置。

## Hook 配置说明

### hooks.json

```json
{
  "version": 1,
  "hooks": {
    "sessionStart": [
      {
        "command": "python3 .cursor/hooks/session-start.py",
        "timeout": 10
      }
    ],
    "preToolUse": [
      {
        "command": "python3 .cursor/hooks/inject-subagent-context.py",
        "timeout": 30,
        "matcher": "Task"
      }
    ],
    "subagentStop": [
      {
        "command": "python3 .cursor/hooks/ralph-loop.py",
        "timeout": 10,
        "matcher": "check"
      }
    ]
  }
}
```

### Hook 事件说明

| 事件 | 触发时机 | 用途 |
|------|----------|------|
| `sessionStart` | 会话开始时 | 注入项目上下文、工作流、指南 |
| `preToolUse` | 工具调用前 | 为 Task 工具注入子代理上下文 |
| `subagentStop` | 子代理停止时 | 控制 Check 代理循环直到验证通过 |

## 子代理说明

### 内置子代理

| 代理 | 用途 | 触发方式 |
|------|------|----------|
| `implement` | 代码实现 | Task(subagent_type="implement") |
| `check` | 代码检查 | Task(subagent_type="check") |
| `debug` | 问题修复 | Task(subagent_type="debug") |
| `research` | 代码研究 | Task(subagent_type="research") |
| `plan` | 任务规划 | Task(subagent_type="plan") |
| `dispatch` | 多代理调度 | 主代理自动使用 |

### 自定义子代理

在 `.cursor/agents/` 目录创建 Markdown 文件：

```markdown
---
name: my-agent
description: Agent description for auto-dispatch
model: opus
---

# My Agent

Your agent prompt here...
```

## 命令协议

使用 `/bw` 前缀调用命令：

| 命令 | 说明 |
|------|------|
| `/bw start` | 开始会话，读取项目上下文 |
| `/bw brainstorm` | 头脑风暴，澄清需求 |
| `/bw check` | 代码质量检查 |
| `/bw finish` | 提交前检查清单 |
| `/bw parallel` | 并行工作树开发 |
| `/bw update-spec` | 更新规范文档 |
| `/bw record` | 记录会话 |
| `/bw before-dev` | 开发前准备 |

## 与 Claude Code 的差异

| 功能 | Claude Code | Cursor |
|------|-------------|--------|
| Hook 配置 | `settings.json` | `hooks.json` |
| Hook 脚本 | `.claude/hooks/` | `.cursor/hooks/` |
| 子代理 | `.claude/agents/` | `.cursor/agents/` |
| 命令 | `.claude/commands/` | `.cursor/commands/` |

### 主要适配

1. **路径调整**: 使用 `.bwflow/` 作为工作流目录
2. **Hook 输入/输出**: Cursor 使用标准 JSON 格式
3. **环境变量**: Cursor 使用 `CLAUDE_PROJECT_DIR` 或从当前目录向上查找

## 与 bwflow 集成

这些模板假设项目已初始化 bwflow 结构：

```
.bwflow/
├── blueprint/           # 架构蓝图
├── spec/               # 编码规范
├── commands/           # 命令协议
├── scripts/            # 脚本
│   ├── get_context.py
│   ├── task.py
│   └── ...
└── tasks/              # 任务目录
    └── <task>/
        ├── task.json
        ├── prd.md
        ├── implement.jsonl
        └── check.jsonl
```

## 故障排除

### Hook 不生效

1. 检查 `hooks.json` 路径是否正确
2. 确保 Python 脚本有执行权限
3. 查看 Cursor 日志中的错误信息

### 子代理上下文未注入

1. 检查 `.bwflow/.current-task` 是否设置
2. 确认 `inject-subagent-context.py` 可以正常执行
3. 验证 task 目录下的 jsonl 文件存在

### Ralph Loop 不工作

1. 检查 `check.jsonl` 是否有 `reason` 字段
2. 确认 `ralph-loop.py` 能正确解析上下文

## 参考

- [Cursor Hooks 文档](https://cursor.com/docs/hooks)
- [Cursor Subagents 文档](https://cursor.com/docs/subagents)
- [Cursor Commands 文档](https://cursor.com/docs/commands)
