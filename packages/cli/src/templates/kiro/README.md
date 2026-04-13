# bwflow for Kiro IDE

## Quick Start

1. **Initialize bwflow**:
   ```bash
   bw init --type kiro
   ```

2. **Start a session**:
   ```
   #start-session
   ```

3. **Switch to Implement Agent**:
   ```
   /agent swap implement
   ```

## How It Works

### Steering System (自动加载)

Kiro 的 Steering 系统会自动将 `.kiro/steering/` 中的规范文件加载到所有对话（包括子 Agent）。

bwflow 的 `.bwflow/spec/` 规范文件会在初始化时复制到 `.kiro/steering/`，实现零成本复用。

### Agent Context Injection (脚本调用)

每个 Agent 在启动时会通过 `agentSpawn` Hook 自动执行：

```bash
python3 .kiro/scripts/get_agent_context.py --agent <type> --update-phase
```

这个脚本会：
- 读取 `.bwflow/tasks/<current-task>/<agent>.jsonl`
- 加载所有引用的文件（需求、设计、额外规范）
- 输出格式化上下文供 Agent 读取
- 更新 task.json 的 current_phase

## Available Agents

| Agent | 用途 | 调用方式 |
|-------|------|---------|
| `implement` | 实现功能 | `/agent swap implement` |
| `check` | 质量检查 | `/agent swap check` |
| `debug` | 调试修复 | `/agent swap debug` |
| `dispatch` | 纯调度器 | `/agent swap dispatch` |

## Troubleshooting

### 脚本未找到

确保：
1. 已运行 `bw init --type kiro`
2. `.kiro/scripts/get_agent_context.py` 存在
3. Python 3 已安装

### 上下文未加载

检查：
1. `.bwflow/.current-task` 文件存在且指向有效任务目录
2. 任务目录包含 `<agent>.jsonl` 文件
3. jsonl 中的所有文件路径存在

### Phase 未更新

确保 Agent 配置中包含 `--update-phase` 参数：

```json
{
  "hooks": {
    "agentSpawn": [
      {
        "command": "python3 .kiro/scripts/get_agent_context.py --agent implement --update-phase"
      }
    ]
  }
}
```

## Differences from Claude/Cursor

| Feature | Claude/Cursor | Kiro |
|---------|---------------|------|
| 规范加载 | 手动引用 | **Steering 自动加载** |
| 上下文注入 | Hook 自动注入 | **agentSpawn Hook + 脚本** |
| Agent 调用 | `Task(subagent_type=...)` | **`/agent swap <name>`** |
| 命令系统 | Slash command | **手动触发 Steering** |

## Directory Structure

```
.kiro/
├── agents/                        # Agent 配置
│   ├── implement.json
│   ├── check.json
│   ├── debug.json
│   └── dispatch.json
├── steering/                      # 规范文件（自动加载）
│   ├── backend/
│   ├── frontend/
│   ├── guides/
│   └── commands/
│       ├── start.md
│       └── finish-work.md
├── scripts/
│   ├── get_agent_context.py       # 上下文获取脚本
│   └── common/                    # 软链接到 .bwflow/scripts/common/
└── README.md

.bwflow/                           # 核心结构
├── tasks/
├── spec/                          # 源规范文件
├── blueprint/
└── scripts/
```

## Workflow Example

1. **Start session**:
   ```
   #start-session
   ```

2. **Create task**:
   ```bash
   python3 .bwflow/scripts/task.py create "Add user profile" --slug user-profile
   python3 .bwflow/scripts/task.py init-context .bwflow/tasks/04-14-user-profile backend
   ```

3. **Implement**:
   ```
   /agent swap implement
   ```
   
   Tell it: "Implement the feature described in prd.md"

4. **Check**:
   ```
   /agent swap check
   ```
   
   Tell it: "Check code changes, fix issues yourself"

5. **Finish**:
   ```
   #finish-work
   ```

## Tips

- Use `#start-session` at the beginning of each session
- Use `#finish-work` before committing
- Steering files are automatically loaded - no need to reference them manually
- Agent context is injected automatically via agentSpawn hook
