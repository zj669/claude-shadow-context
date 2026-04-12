# bwflow

Blueprint Workflow - 蓝图驱动的结构化 AI 开发伴侣。

## 核心理念

bwflow 将项目知识组织为两层：

1. **Blueprint（蓝图层）**：架构意图、模块职责、关键方法
2. **Spec（规范层）**：编码标准、模式、协作约定

AI 通过阅读蓝图理解"为什么这么设计"，通过 Spec 理解"如何编写符合项目风格的代码"。

## 快速开始

### 初始化项目

```bash
npm install @zj669/bwflow
bw init
```

这会在当前项目创建 `bwflow/` 目录，包含：

```
bwflow/
├── blueprint/          # 架构蓝图
│   └── README.md       # 蓝图入口
├── spec/               # 编码规范
│   ├── backend/        # 后端规范
│   └── frontend/       # 前端规范
├── commands/           # 命令协议
│   ├── init/           # 初始化协议
│   ├── explore/        # 探索协议
│   ├── align/          # 对齐协议
│   └── finish/         # 完成协议
└── hooks/              # 生命周期钩子
    ├── session-start.py
    └── ralph-loop.py
```

### 开发流程

```
bw start    # 开始会话，注入上下文
bw explore  # 探索项目结构
bw finish   # 完成任务，检查对齐
```

## 命令参考

| 命令 | 说明 |
|------|------|
| `bw init` | 初始化 bwflow 结构 |
| `bw start` | 开始开发会话 |
| `bw explore [模块]` | 探索指定模块的蓝图 |
| `bw align` | 检查蓝图与代码的对齐 |
| `bw finish` | 完成任务，对齐检查 |

## 设计原则

1. **蓝图优先**：优先读取意图层，而不是先散搜实现层
2. **最小上下文**：读取相关蓝图，只在必要时补看代码
3. **结束对齐**：每次任务结束检查蓝图是否仍然可信
4. **轻量协议**：不追求完整框架，只保留最小闭环
