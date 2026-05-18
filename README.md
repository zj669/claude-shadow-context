<h1 align="center">bwflow</h1>

<p align="center">
  <strong>蓝图驱动的结构化 AI 开发伴侣</strong><br>
  为 Claude Code、Cursor、Kiro 项目初始化统一的 Blueprint Workflow，
  让 AI 在更短上下文中理解项目、执行任务并沉淀会话记忆。
</p>

<p align="center">
  简体中文
</p>

<p align="center">
  <a href="#简介">简介</a> •
  <a href="#功能特性">功能特性</a> •
  <a href="#架构">架构</a> •
  <a href="#快速开始">快速开始</a> •
  <a href="#cli-用法">CLI 用法</a> •
  <a href="#项目结构">项目结构</a> •
  <a href="#开发">开发</a> •
  <a href="#qa">Q&A</a>
</p>

---

## 简介

`bwflow` 是一个 Blueprint Workflow CLI。它不会替代你的业务框架，也不会强行接管
项目结构，而是把一套可复制的 AI 协作协议安装到现有项目中：

- `.bwflow/`：项目级蓝图、规范、任务、脚本和会话记录。
- `.claude/`：Claude Code 命令、agent 和 hook 模板。
- `.cursor/`：Cursor 命令、agent 和 hook 模板。
- `.kiro/`：Kiro steering、agent、hook 和脚本模板。

它解决两个长期存在的问题：

- **上下文爆炸**：用蓝图层压缩架构意图，避免 AI 每次都从散乱代码重新理解项目。
- **理解漂移**：任务结束后检查 blueprint/spec 是否仍然可信，把经验沉淀回工作流。

适用场景：

- 需要在多个 AI 编程工具之间共享同一套项目理解。
- 需要用任务、PRD、上下文 JSONL 和会话日志约束 AI 开发过程。
- 希望把项目规范从口头经验变成可读取、可注入、可检查的工程资产。

## 功能特性

- 一条 `bw init` 命令初始化 `.bwflow` 核心工作流。
- 支持 Claude Code、Cursor、Kiro 三个平台模板。
- 交互式初始化：平台多选、开发者名称、spec 来源、冲突策略。
- 支持远程 spec 模板：`gh:org/repo`、`gitlab:org/repo`、HTTPS URL。
- 远程模板下载失败时自动回退默认 spec，初始化流程不中断。
- 初始化后自动验证核心目录、配置文件、平台目录和关键脚本。
- Python 脚本提供任务创建、上下文注入、会话记录、归档和多 agent worktree 流程。
- Blueprint 层记录架构意图，Spec 层记录代码规范，Workspace 层记录工作历史。
- 模板中内置 `/bw start`、`/bw check`、`/bw finish-work`、`/bw parallel` 等命令。
- 包含 TypeScript CLI 源码和构建后的 npm 发布产物。

## 架构

```text
Developer terminal
        |
        |  bw init
        v
TypeScript CLI (src/index.ts)
        |
        +--> init command (src/commands/init.ts)
        |       |
        |       +--> InteractivePrompt       collect platforms, developer, spec source
        |       +--> TemplateFetcher         download remote spec templates
        |       +--> ConfigManager           initialize developer identity
        |       +--> PlatformConfigurator    copy Claude/Cursor/Kiro templates
        |       +--> ValidationService       verify generated workflow files
        |       +--> RollbackManager         remove created paths on fatal errors
        |
        v
Generated project workflow
        |
        +--> .bwflow/
        |       +--> blueprint/              architecture intent
        |       +--> spec/                   coding conventions
        |       +--> scripts/                task/session/context utilities
        |       +--> tasks/                  PRD and task context
        |       +--> workspace/              session journals
        |
        +--> .claude/ or .cursor/ or .kiro/
                +--> commands                /bw workflow commands
                +--> agents                  plan/implement/check/debug/research/dispatch
                +--> hooks/scripts           context injection and quality loops
```

## 工作流模型

`bwflow` 把 AI 开发拆成两层理解和四段闭环：

| 层级 | 位置 | 回答的问题 | 典型内容 |
|---|---|---|---|
| Blueprint | `.bwflow/blueprint/` | 为什么这样设计 | 模块职责、边界、设计决策、关键流程 |
| Spec | `.bwflow/spec/` | 代码应该怎么写 | 目录规范、错误处理、类型安全、测试要求 |
| Task | `.bwflow/tasks/` | 当前要做什么 | PRD、上下文 JSONL、阶段、子任务 |
| Workspace | `.bwflow/workspace/` | 做过什么 | 会话记录、提交摘要、后续事项 |

```text
/bw start
    |
    +--> read workflow + blueprint + spec indexes
    |
    v
plan / brainstorm
    |
    +--> create task + PRD + context files
    |
    v
implement
    |
    +--> hooks inject task/spec/blueprint context
    |
    v
/bw check
    |
    +--> verify code, blueprint alignment, spec compliance
    |
    v
/bw finish-work
    |
    +--> final checklist + session record + archive
```

## 快速开始

### 安装

```bash
npm install -g @zj669/bwflow
```

确认 CLI 可用：

```bash
bw --version
```

### 交互式初始化

推荐在普通开发环境中使用交互式初始化：

```bash
cd my-project
bw init
```

初始化过程会依次询问：

1. 要配置的平台：Claude Code、Cursor、Kiro。
2. 开发者名称：默认尝试读取 `git config user.name`。
3. Spec 模板来源：默认模板或远程仓库。
4. 如果目标平台目录已存在，选择覆盖、跳过或取消。

初始化完成后，项目中会出现类似结构：

```text
.bwflow/
.claude/        # 如果选择 Claude Code
.cursor/        # 如果选择 Cursor
.kiro/          # 如果选择 Kiro
```

然后在对应 AI 工具中运行：

```text
/bw start
```

### CI / 非交互初始化

当前 CLI 的非交互模式需要显式提供平台和开发者名称：

```bash
bw init -y -t claude -u "your-name"
```

指定远程 spec 模板：

```bash
bw init -y -t claude -u "your-name" --registry gh:your-org/bwflow-specs
```

强制覆盖已存在的平台配置：

```bash
bw init -y -t claude -u "your-name" --registry gh:your-org/bwflow-specs --force
```

> `-t, --type` 在交互式使用中已经不推荐，但它仍是当前非交互模式下选择单个平台的兼容参数。

## CLI 用法

### `bw init`

初始化 `.bwflow` 核心目录和平台模板。

```bash
bw init [options]
```

| 选项 | 说明 |
|---|---|
| `-t, --type <type>` | 指定单个平台。可选值：`claude`、`cursor`、`kiro`。交互模式推荐使用多选。 |
| `-u, --user <name>` | 指定开发者名称，跳过开发者名称输入。 |
| `-y, --yes` | 非交互模式。当前需要同时提供 `-t` 和 `-u`。 |
| `-f, --force` | 强制覆盖已存在的平台目录。 |
| `--registry <url>` | 远程 spec 模板地址。支持 `gh:`、`gitlab:` 和 HTTPS URL。 |

常用示例：

```bash
# 交互式
bw init

# 单平台非交互
bw init -y -t claude -u "Alice"

# 使用远程 spec 模板
bw init -t cursor -u "Alice" --registry gh:org/specs

# 覆盖已有平台目录
bw init -t kiro -u "Alice" --force
```

### `bw sync`

目前是 `init` 的提示型别名，不会执行额外同步逻辑：

```bash
bw sync
```

## 远程 Spec 模板

`--registry` 用于把外部仓库中的 spec 模板下载到 `.bwflow/spec`。

支持格式：

| 格式 | 示例 |
|---|---|
| GitHub 简写 | `gh:org/repo` |
| GitHub 子目录 | `gh:org/repo/templates/backend` |
| GitLab 简写 | `gitlab:org/repo` |
| HTTPS URL | `https://github.com/org/repo` |

下载逻辑：

1. 校验 registry 格式。
2. 转换为 `giget` 支持的地址。
3. 下载到 `.bwflow/spec`。
4. 如果 30 秒超时或下载失败，回退到包内默认 spec。

## 项目结构

```text
src/
|-- index.ts                  CLI 入口，注册 bw init / bw sync
|-- commands/
|   |-- init.ts               初始化主流程
|   +-- upgrade.ts            升级命令占位实现
|-- core/
|   |-- InteractivePrompt.ts  交互式参数收集
|   |-- TemplateFetcher.ts    远程模板下载
|   |-- ConfigManager.ts      开发者初始化
|   |-- PlatformConfigurator.ts 平台模板复制
|   |-- ValidationService.ts  初始化结果验证
|   |-- RollbackManager.ts    失败回滚
|   +-- ErrorHandler.ts       错误处理
|-- templates/
|   |-- claude/               Claude Code 模板
|   |-- cursor/               Cursor 模板
|   +-- kiro/                 Kiro 模板

bwflow/
|-- blueprint/                蓝图层，记录架构意图
|-- spec/                     规范层，记录代码标准
|-- scripts/                  Python 任务、上下文和会话脚本
|-- tasks/                    任务与归档
|-- workspace/                会话日志
|-- config.yaml               工作流配置
+-- workflow.md               开发工作流说明

dist/                         TypeScript 构建产物和发布模板
```

## 开发

### 环境要求

- Node.js `>=18.0.0`
- npm
- Python 3，用于验证 `.bwflow/scripts` 工作流脚本

### 安装依赖

```bash
npm install
```

### 类型检查

```bash
npx tsc --noEmit
```

### 构建

```bash
npm run build
```

构建会执行：

1. `tsc` 编译 TypeScript 到 `dist/`。
2. 复制 `src/templates` 到 `dist/templates`。
3. 清理模板中的旧版嵌套 `bwflow` 目录。

### 测试

```bash
npm test
```

当前仓库配置了 Jest 命令；新增 CLI 行为时建议优先覆盖这些路径：

- 参数矩阵：交互式、非交互、`--registry`、`--force`。
- 文件冲突：覆盖、跳过、取消。
- 远程模板：成功、超时、失败回退。
- 平台模板复制：Claude Code、Cursor、Kiro。
- 验证服务：缺失目录、缺失脚本、无效 YAML。

## 设计原则

- **蓝图优先**：先读架构意图，再读实现细节。
- **最小上下文**：只注入完成任务所需的 blueprint/spec/task 上下文。
- **规范驱动**：开发前读 spec，检查时按 spec 验证。
- **结束对齐**：任务完成后同步 blueprint/spec/workspace，避免理解漂移。
- **可迁移协议**：同一个 `.bwflow` 核心目录可以服务多个 AI 平台。

## Q&A

### `bwflow` 会改我的业务代码吗？

不会。`bw init` 只生成 `.bwflow/` 和被选择平台的配置目录，例如 `.claude/`、`.cursor/`、`.kiro/`。

### 可以同时配置多个 AI 平台吗？

可以。交互式 `bw init` 支持多选平台。多个平台共享同一套 `.bwflow` 核心上下文。

### 远程模板下载失败怎么办？

初始化不会直接中断。CLI 会提示下载失败，并回退到包内默认 spec 模板。

### 已经存在 `.claude` 或 `.cursor` 怎么办？

交互式模式会提示选择覆盖、跳过或取消。非交互模式默认跳过，传入 `--force` 后覆盖。

### 为什么非交互模式还要传 `-t`？

当前实现中，`-y` 只表示跳过提示，不会自动选择默认平台；因此需要 `-t claude`、`-t cursor` 或 `-t kiro` 明确目标平台。

### 初始化后应该从哪里开始？

先编辑项目蓝图：

```bash
$EDITOR .bwflow/blueprint/README.md
```

然后在 AI 工具中运行：

```text
/bw start
```

## License

MIT
