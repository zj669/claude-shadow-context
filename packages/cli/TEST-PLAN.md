# bwflow CLI 测试计划

## 测试环境准备

```bash
# 创建测试目录
mkdir -p /tmp/bwflow-e2e-test
cd /tmp/bwflow-e2e-test

# 使用本地构建的 CLI
CLI_PATH="/home/zj669/repo/claude-shadow-context/packages/cli/dist/index.js"
```

## 测试结果

| Test | 状态 | 结果 |
|------|------|------|
| Test 1: bw init | ✅ PASS | 正确创建 8 个目录 + 复制命令/Hooks |
| Test 2: bw sync | ✅ PASS | 正确同步到 .claude/commands/bwflow/ |
| Test 3: 文件结构 | ✅ PASS | 13 个文件正确生成 |
| Test 4: Hook 执行 | ✅ PASS | 正确读取 README 并显示上下文 |
| Test 5: bw --help | ✅ PASS | 显示 5 个命令 |
| Test 6: 重复 init | ✅ PASS | 正确提示已存在 |
| Test 7: --force | ✅ PASS | 重新创建所有文件 |
| Test 8: 平台选择 | ✅ PASS | cursor 提示暂未实现 |

---

## 测试用例详情

### Test 1: 初始化项目

```bash
node $CLI_PATH init
```

**实际输出**：

```
🔷 bwflow 初始化

目标目录: /tmp/bwflow-e2e-test
模板目录: .../dist/templates/claude

📂 创建目录:

  ✓ bwflow/
  ✓ bwflow/blueprint/
  ✓ bwflow/blueprint/src/
  ✓ bwflow/spec/
  ✓ bwflow/spec/backend/
  ✓ bwflow/spec/frontend/
  ✓ bwflow/commands/
  ✓ bwflow/hooks/

📁 复制命令模板:

  ✓ bwflow/commands/align/CMD.md
  ✓ bwflow/commands/explore/CMD.md
  ✓ bwflow/commands/finish/CMD.md
  ✓ bwflow/commands/init/CMD.md
  ✓ bwflow/commands/start/CMD.md

📁 复制 Hooks 模板:

  ✓ bwflow/hooks/session-start.py
  ✓ bwflow/blueprint/README.md
  ✓ .claude-shadow-context/

✅ bwflow 初始化完成!
```

### Test 2: 同步到 Claude Code

```bash
node $CLI_PATH sync
```

**实际输出**：

```
🔄 bwflow 同步

目标平台: claude
工作目录: /tmp/bwflow-e2e-test

同步到 Claude Code...

  同步 Claude Code 配置...
    ✓ commands → .claude/commands/bwflow/
    ✓ README.md → .claude/commands/bwflow/README.md

✅ 同步完成!
```

### Test 3: 验证文件结构

```bash
find . -type f | grep -v node_modules | sort
```

**实际输出**：

```
./bwflow/blueprint/README.md
./bwflow/commands/align/CMD.md
./bwflow/commands/explore/CMD.md
./bwflow/commands/finish/CMD.md
./bwflow/commands/init/CMD.md
./bwflow/commands/start/CMD.md
./bwflow/hooks/session-start.py
./.claude/commands/bwflow/align/CMD.md
./.claude/commands/bwflow/explore/CMD.md
./.claude/commands/bwflow/finish/CMD.md
./.claude/commands/bwflow/init/CMD.md
./.claude/commands/bwflow/README.md
./.claude/commands/bwflow/start/CMD.md
```

### Test 4: Hook 执行

```bash
python3 ./bwflow/hooks/session-start.py
```

**实际输出**：

```
============================================================
🔷 bwflow Session Start
============================================================

📋 项目架构 (Blueprint):
----------------------------------------
  # 项目架构蓝图
  
  ## 概述
  [项目简介：一句话描述项目是什么、解决什么问题]
  ...

📌 当前任务: 无

📜 上次会话: 无记录

============================================================
💡 使用 '/bw align' 检查蓝图对齐
💡 使用 '/bw finish' 完成任务
============================================================
```

### Test 5: 命令帮助

```bash
node $CLI_PATH --help
```

**实际输出**：

```
Usage: bw [options] [command]

bwflow - Blueprint Workflow CLI

Commands:
  init [options]    初始化 bwflow 结构到当前项目
  sync [options]    同步 bwflow 配置到各平台
  start             开始开发会话
  explore [module]  探索指定模块的蓝图
  align             检查蓝图与代码的对齐
  finish            完成任务，检查对齐并生成摘要
```

### Test 6: 重复初始化

```bash
node $CLI_PATH init
```

**实际输出**：

```
⚠️  bwflow 目录已存在
使用 --force 强制覆盖
```

### Test 7: 强制覆盖

```bash
node $CLI_PATH init --force
```

**实际输出**：重新创建所有文件（与 Test 1 相同）

### Test 8: 平台选择

```bash
node $CLI_PATH sync --platform cursor
```

**实际输出**：

```
⚠️  Cursor 集成暂未实现
```

---

## Claude Code 集成测试

### 验证 .claude/commands/bwflow/ 结构

```bash
ls -la .claude/commands/bwflow/
```

**预期**：

```
align/   explore/  finish/  init/  README.md  start/
```

### 在 Claude Code 中测试命令

```
/bw start
/bw explore auth
/bw align
/bw finish
```

---

## 清理

```bash
rm -rf /tmp/bwflow-e2e-test
```

---

## 测试总结

**8/8 测试通过** ✅

CLI 核心功能验证完成：
- ✅ 初始化项目结构
- ✅ 同步到 Claude Code
- ✅ Hook 执行
- ✅ 命令帮助
- ✅ 重复检测
- ✅ 强制覆盖
- ✅ 平台选择

下一步：发布到 npm
