# claude-shadow-context

> 通过蓝图压缩上下文，建立人和 AI 的共享项目理解。
> 先用蓝图理解，再在结束时校验是否仍然对齐。

claude-shadow-context 是一个轻量的 Claude Code 插件。
它不试图成为完整的 AI 开发框架，而是聚焦在一个更小也更关键的问题：

- 让 AI 在更短上下文里理解项目结构、职责和架构意图
- 让这种理解在任务结束后仍然保持可信

它约束的不是文档数量，而是 AI 理解和修改代码的方式。

## 快速安装和开始

### 1. 安装插件

```bash
/plugin marketplace add https://github.com/zj669/claude-shadow-context.git
/plugin install claude-shadow-context@claude-shadow-context
```

### 2. 准备蓝图层

如果项目还没有蓝图层，需要先建立 `.blueprint/` 结构，作为代码之外的意图层。

### 3. 开始使用

```bash
/claude-shadow-context:explore
```

之后围绕下面这条最小工作流使用即可：

```text
explore → 修改代码 → align
```

- `explore`：动手前先用蓝图收敛最相关上下文
- `align`：结束前根据会话和代码变化检查蓝图是否仍然对齐

## 项目定位

claude-shadow-context 不再追求做一个完整的 Claude 工作流框架。

它现在只解决两件事：

1. **探索压缩**：让 AI 在探索上下文时优先通过蓝图理解项目，而不是先散搜代码
2. **结束对齐**：让 AI 在会话结束或提交前检查蓝图是否仍与代码一致

这意味着它更像一个 **Blueprint Alignment Layer**，而不是一个全家桶式 AI 开发生态。

## Hook 运行前提

当前插件中的 hook 通过 Node 脚本执行：

- 需要用户机器上可执行 `node`
- 推荐通过 `${CLAUDE_PLUGIN_ROOT}` 引用插件内脚本，避免工作目录变化导致路径失效
- 本地用 `--plugin-dir` 验证时，应指向插件根目录；当前仓库应使用 `E:/WorkSpace/repo/bluefirst`，不要指向 `E:/WorkSpace/repo/bluefirst/.claude-plugin`

推荐安装后至少验证一次：

1. 安装插件
2. 发送一个普通提示词
3. 确认 `UserPromptSubmit` 会注入 explore 提醒
4. 触发涉及代码修改的子代理任务
5. 确认 `SubagentStart` 会注入同类蓝图提醒
6. 确认 `SessionEnd` 会异步触发对齐提醒

本地可用下面的方式验证 `UserPromptSubmit`：

```bash
claude -p --plugin-dir "E:/WorkSpace/repo/bluefirst" "请只回答：如果你收到了额外的 hook 提醒，就原样复述那段提醒；如果没有收到，就只回答 NO_HOOK_CONTEXT"
```

## 什么是蓝图优先

claude-shadow-context 的核心不是“多写文档”，而是：**让意图层成为 AI 的优先入口**。

- **代码** 是实现层，回答“怎么做”
- **蓝图** 是意图层，回答“为什么这样做、职责是什么、边界在哪里”

在真实项目里，代码会持续演化，但架构意图很容易丢失。久而久之，AI 只能根据局部代码猜测上下文，修改会越来越偏离原始设计。

claude-shadow-context 解决的是两个具体问题：

- 进入任务前，先读取最相关的蓝图，压缩理解成本
- 结束任务时，根据会话和代码变化检查蓝图是否发生漂移

所以 claude-shadow-context 不是一个文档包，也不是一个完整框架，而是一个 **Blueprint Alignment Protocol**：
它把“先通过蓝图理解，再在结束时确认蓝图仍可信”变成可执行的工作流协议。

## 有哪些指令

| 指令 | 作用 | 使用时机 |
| --- | --- | --- |
| `/claude-shadow-context:explore` | 优先通过蓝图收敛最相关项目上下文 | 分析需求、修复问题、开发功能前 |
| `/claude-shadow-context:align` | 根据会话与代码变化检查蓝图是否仍对齐，必要时给出同步建议 | 任务结束前、提交前 |

## 最小能力模型

### 1. `explore`

- 从根入口收敛到最相关的业务蓝图
- 读取所有相关蓝图（蓝图本身就是精简的意图层）
- 只有蓝图不足时，再补看少量代码

### 2. `align`

- 基于本轮会话、修改文件和 `git diff` 判断是否存在蓝图漂移
- 区分“无需更新 / 需要补记录 / 需要修正职责或关键方法单元”
- 在必要时执行轻量同步，而不是全量重写蓝图

## Hooks 设计

插件默认只保留 3 个 hook：

1. `UserPromptSubmit`
   - 当用户进入项目分析或代码修改任务时，提醒优先使用 `explore`
2. `SubagentStart`
   - 当子 agent 启动时，注入同样的蓝图优先上下文
3. `SessionEnd`
   - 会话结束时异步触发 `align` 提醒，确保结束阶段也考虑蓝图对齐

## 可选 Git 集成

如果希望在真实 `git commit` 前做蓝图对齐检查，建议额外提供一个可选的 `.git/hooks/pre-commit` 集成。

这类检查不应依赖 Claude 会话是否仍然存活，而应作为独立补充能力存在。
