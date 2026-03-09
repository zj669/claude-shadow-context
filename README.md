# claude-shadow-context

> 蓝图优先的 Claude Code 插件。
> 先理解架构意图，再修改代码。

claude-shadow-context 把“蓝图优先 / 影子架构”工作方法产品化为 Claude Code 插件。
它约束的不是文档本身，而是 AI 修改代码的流程。

## 快速安装和开始

### 1. 安装插件

```bash
/plugin marketplace add https://github.com/zj669/claude-shadow-context.git
/plugin install claude-shadow-context
```

### 2. 初始化项目

```bash
/claude-shadow-context:init
```

初始化后，claude-shadow-context 会为项目建立 `.blueprint/` 结构，作为代码之外的蓝图层。

### 3. 开始使用

```bash
/claude-shadow-context:explore
```

之后围绕下面这条最小工作流使用即可：

```text
explore → 修改代码 → sync → check
```

- `explore`：动手前先收敛最相关上下文
- `sync`：代码改动后同步蓝图
- `check`：结束前检查蓝图与代码是否一致

## 什么是蓝图优先

claude-shadow-context 的核心不是“多写文档”，而是：**代码与意识分离**。

- **代码** 是实现层，回答“怎么做”
- **蓝图** 是意图层，回答“为什么这样做、职责是什么、边界在哪里”

在真实项目里，代码会持续演化，但架构意图很容易丢失。久而久之，AI 只能根据局部代码猜测上下文，修改会越来越偏离原始设计。

claude-shadow-context 解决的是这个问题：

- 修改前，先读取最相关的蓝图，理解架构意图
- 修改后，把有意义的变化同步回蓝图
- 在任务结束时检查蓝图与代码是否发生漂移

所以 claude-shadow-context 不是一个文档包，而是一个 **Blueprint Runtime**：
它把“先理解意图，再改代码”变成可执行的工作流协议。

## 有哪些指令

| 指令 | 作用 | 使用时机 |
| --- | --- | --- |
| `/claude-shadow-context:init` | 初始化项目蓝图结构 | 第一次接入项目时 |
| `/claude-shadow-context:explore` | 探索最相关的蓝图与代码上下文 | 分析需求、修复问题、开发功能前 |
| `/claude-shadow-context:sync` | 将代码变化同步回蓝图 | 完成代码修改后 |
| `/claude-shadow-context:check` | 检查蓝图与代码是否一致 | 任务结束前、提交前 |
