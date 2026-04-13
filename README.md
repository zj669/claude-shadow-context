# bwflow

> 蓝图驱动的结构化 AI 开发伴侣

bwflow 是一个 Blueprint Workflow CLI 工具，它将**蓝图优先**的理解心智与**结构化工作流**深度融合，帮助 AI 在更短上下文中理解项目，并在任务结束后保持理解可信。

## 核心能力

bwflow 围绕三个原语组织：

1. **init** — 为项目初始化蓝图层和工作流结构
2. **explore** — 蓝图优先探索，用最小上下文获得足够准确的项目理解
3. **align** — 任务结束后检查蓝图是否仍与代码对齐

加上从 Trellis 借鉴的：

4. **plan** — 需求分析，生成 PRD 和任务上下文
5. **implement** — 实现阶段，Hook 自动注入蓝图和规范上下文
6. **check** — 质量检查，Ralph Loop 守护直到达标
7. **finish** — 收尾，align 蓝图 + 记录会话 + 同步规范

## 快速开始

### 安装

```bash
npm install -g @zj669/bwflow
```

### 初始化项目

```bash
cd my-project
bw init -u your-name --targets claudecode,cursor
```


## 设计原则

1. **蓝图优先**：优先读取意图层，而不是先散搜实现层
2. **最小上下文**：蓝图足够时，不扩读实现细节
3. **结束对齐**：每次任务结束都应考虑蓝图是否仍然可信
4. **自我学习**：从失败中沉淀经验，形成可复用的 Evolved Skills

## License

MIT
