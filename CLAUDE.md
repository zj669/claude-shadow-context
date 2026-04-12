# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## 项目概述

`bwflow` 是一个蓝图驱动的人机共识层。

它关注两个核心问题：

1. 让 AI 在更短上下文中理解项目结构、职责与架构意图
2. 让这种理解在任务结束后仍然保持可信

## 目录结构

```
bwflow/                    # 核心工作流目录
├── blueprint/            # 架构蓝图层
│   └── README.md        # 根蓝图入口
├── spec/                # 编码规范层
│   ├── backend/
│   └── frontend/
├── commands/            # 命令协议 (bw 命令)
│   ├── init/            # 初始化协议
│   ├── explore/         # 探索协议
│   ├── align/           # 对齐协议
│   ├── start/           # 会话开始协议
│   └── finish/          # 完成任务协议
└── hooks/               # 生命周期钩子
    └── session-start.py

.claude/                  # Claude Code 配置
└── commands/bwflow/     # 同步的命令协议
```

## 命令参考

在 Claude Code 中使用 `/bw` 前缀调用命令：

| 命令 | 说明 |
|------|------|
| `/bw start` | 开始会话，读取项目上下文 |
| `/bw explore [模块]` | 探索指定模块的蓝图 |
| `/bw align` | 检查蓝图与代码的对齐 |
| `/bw finish` | 完成任务，生成摘要 |

## 核心原语

1. **Blueprint（蓝图层）**
   - 架构意图、模块职责、关键方法
   - 回答"为什么这样设计"

2. **Spec（规范层）**
   - 编码标准、模式、协作约定
   - 回答"如何编写符合项目风格的代码"

## 设计原则

1. **蓝图优先**：优先读取意图层，而不是先散搜实现层
2. **最小上下文**：读取相关蓝图，只在必要时补看代码
3. **结束对齐**：每次任务结束检查蓝图是否仍然可信
4. **轻量协议**：不追求完整框架，只保留最小闭环

## CLI 使用

```bash
# 安装
npm install -g @zj669/bwflow

# 初始化项目
bw init

# 同步到 Claude Code
bw sync
```
