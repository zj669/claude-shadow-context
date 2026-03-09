# mcp-server.cjs 蓝图

## Metadata
- title: Bluefirst MCP Server
- type: service
- summary: Bluefirst 插件的 MCP 协议服务器实现，当前为占位版本，未来将承载索引、校验、投影、漂移检测能力

## 关键方法单元

### 方法单元：initialize
- location: `rl.on('line')` 事件处理 - initialize 分支
- purpose: 响应 MCP 协议的 initialize 请求，返回服务器能力声明
- input: `{ method: 'initialize', id: string, ...request }`
- output: `{ jsonrpc: '2.0', id: string, result: { protocolVersion, capabilities, serverInfo } }`
- core_steps:
  1. 接收 initialize 请求
  2. 返回协议版本 '2024-11-05'
  3. 声明空的 tools 和 resources 能力（占位）
  4. 返回服务器信息（name: 'bluefirst', version: '0.1.0'）

### 方法单元：tools/list
- location: `rl.on('line')` 事件处理 - tools/list 分支
- purpose: 响应工具列表查询，当前返回空列表
- input: `{ method: 'tools/list', id: string }`
- output: `{ jsonrpc: '2.0', id: string, result: { tools: [] } }`
- core_steps:
  1. 接收 tools/list 请求
  2. 返回空的 tools 数组（占位实现）

### 方法单元：resources/list
- location: `rl.on('line')` 事件处理 - resources/list 分支
- purpose: 响应资源列表查询，当前返回空列表
- input: `{ method: 'resources/list', id: string }`
- output: `{ jsonrpc: '2.0', id: string, result: { resources: [] } }`
- core_steps:
  1. 接收 resources/list 请求
  2. 返回空的 resources 数组（占位实现）

### 方法单元：sendResponse
- location: `sendResponse(response)`
- purpose: 统一的响应发送函数，将 JSON 对象序列化后输出到 stdout
- input: `response: object` - MCP 协议响应对象
- output: 无返回值，直接输出到 stdout
- core_steps:
  1. 将响应对象序列化为 JSON 字符串
  2. 通过 console.log 输出到 stdout

### 方法单元：错误处理
- location: `rl.on('line')` 事件处理 - else 分支
- purpose: 处理未知的 MCP 方法请求，返回标准错误响应
- input: `{ method: string, id: string }` - 未知方法的请求
- output: `{ jsonrpc: '2.0', id: string, error: { code: -32601, message: 'Method not found' } }`
- core_steps:
  1. 识别未知方法
  2. 返回 MCP 标准错误码 -32601（Method not found）

### 方法单元：信号处理
- location: `process.on('SIGINT')` 和 `process.on('SIGTERM')`
- purpose: 优雅处理进程终止信号，确保服务器正常退出
- input: SIGINT 或 SIGTERM 信号
- output: 进程退出（exit code 0）
- core_steps:
  1. 监听 SIGINT 和 SIGTERM 信号
  2. 收到信号后立即退出进程

## 架构说明

当前实现是占位版本，只实现了 MCP 协议的基础握手和空响应。未来将扩展以下能力：

1. **索引能力**：扫描 `.blueprint/` 目录，建立蓝图文件索引
2. **校验能力**：对比代码与蓝图，检测架构漂移
3. **投影能力**：根据任务需求，投影出最相关的蓝图子集
4. **漂移检测**：识别代码变更，提示需要同步的蓝图

## 依赖关系

- 依赖 Node.js 内置模块：`readline`
- 通过 stdin/stdout 与 Claude Code 通信（MCP 协议）
- 被 `.mcp.json` 配置文件引用

## 变更记录
- 2026-03-08: 初始化蓝图，记录占位实现的架构意图
