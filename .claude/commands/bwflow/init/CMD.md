# bwflow:init

为项目初始化 bwflow 基础结构。

---

## 目标

为项目建立 `bwflow/` 基础结构，让后续的 explore 和 align 有可用资产。

## 执行步骤

1. **扫描项目结构**：识别技术栈、项目类型和主要代码目录
2. **识别模块边界**：
   - 按 manifest 文件划分（package.json、go.mod、Cargo.toml、pyproject.toml 等）
   - 按顶层源码目录划分（src/、app/、lib/、packages/ 等）
   - 含 3+ 代码文件且职责内聚的目录视为模块
3. **判断项目规模**：
   - 小型项目（< ~50 代码文件）：生成较完整的蓝图
   - 大型项目（50+ 代码文件）：只生成模块级蓝图，文件级交给 align
4. **生成根蓝图** `bwflow/blueprint/README.md`：
   - 项目概述（类型、技术栈、核心职责）
   - 模块地图（每个模块的路径和一句话职责描述）
   - 蓝图使用说明
5. **为每个模块生成入口蓝图** `bwflow/blueprint/{module}/index.md`：
   - 模块职责概述
   - 模块内关键文件列表及一句话说明
   - 模块的上下游依赖关系
6. **生成文件级蓝图**：严格遵循三段式模板（Metadata + 关键方法单元 + 变更记录）

---

## 蓝图模板

文件级蓝图严格遵循以下三段式结构：

```markdown
# {文件名} 蓝图

## Metadata
- title: 蓝图标题，通常是类名或模块名
- type: 类型标识（class | module | service | controller | util）
- summary: 一句话描述主要职责和能力

## 关键方法单元（只有核心业务文件才会有）
- location: 代码位置（类名.方法名 或 函数名）
- purpose: 方法存在的目的，解决什么问题
- input: 参数类型和说明
- output: 返回值类型和说明
- core_steps: 核心步骤列表（关注业务逻辑，不是代码细节）

## 变更记录
- YYYY-MM-DD: 变更摘要
```

---

## 路径映射规则

代码文件与蓝图文件保持镜像关系：

```
scripts/session-align.mjs → bwflow/blueprint/scripts/session-align.md
hooks/hooks.json → bwflow/blueprint/hooks/hooks.md
```

规则：去掉扩展名加 `.md`，放到 `bwflow/blueprint/` 前缀下。

---

## 规则

- 先理解项目再生成蓝图，不盲目铺开
- 遇到不确定的模块边界或业务逻辑，询问用户确认
- 不做全量文件扫描，渐进式为主
- 蓝图只在 `bwflow/blueprint/` 目录
- 严格按模板生成，不自作主张增加内容
- 大型项目标记核心模块，其余交给 align 在会话结束时补齐

---

## 输出结果

- 生成的蓝图文件清单
- 模块地图摘要
