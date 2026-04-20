# Changelog

All notable changes to this project will be documented in this file.

## [0.1.9] - 2026-04-20

### Other
- Release version 0.1.9


## [Unreleased]

### Added
- **交互式初始化流程**：使用 `bw init` 启动友好的交互式命令行界面
  - 多平台多选支持（Claude Code、Cursor、Kiro）
  - 自动从 git config 读取开发者名称作为默认值
  - Spec 模板来源选择（默认模板或远程仓库）
  - 文件冲突处理策略选择（覆盖/跳过/取消）
- **远程模板下载**：支持从 Git 仓库下载 Spec 模板
  - 支持 GitHub 简写格式（`gh:org/repo`）
  - 支持 GitLab 简写格式（`gitlab:org/repo`）
  - 支持子目录下载（`gh:org/repo/subpath`）
  - 支持完整 URL 格式
  - 下载失败自动回退到默认模板
- **配置验证**：初始化完成后自动验证配置完整性
  - 验证核心目录和配置文件
  - 验证平台配置目录
  - 验证必需的脚本文件
  - 显示详细的错误和警告信息
- **CLI 参数**：新增 `--registry <url>` 参数用于指定远程模板 URL
- **非交互模式增强**：`-y` 参数支持完全跳过交互式提示，适用于 CI/CD

### Changed
- **init 命令重构**：采用模块化架构，职责分离
  - `InteractivePrompt`：交互式输入收集
  - `TemplateFetcher`：远程模板下载
  - `ConfigManager`：配置文件管理
  - `PlatformConfigurator`：平台配置复制
  - `ValidationService`：初始化验证
  - `ErrorHandler` & `RollbackManager`：错误处理和回滚
- **平台选择方式**：从单选改为多选，支持同时配置多个平台
- **开发者初始化**：改用 Python 脚本执行（`init_developer.py`）

### Deprecated
- `-t, --type <type>` 参数已废弃，请使用交互式多选或 `-y` 默认配置

### Dependencies
- 新增 `inquirer@^9.0.0`：交互式命令行界面
- 新增 `giget@^1.2.0`：Git 模板下载
- 新增 `ora@^7.0.0`：加载动画和进度指示

### Fixed
- 修复多平台配置时的文件冲突检测问题
- 修复 Unix 系统上脚本执行权限设置问题

## [0.1.5] - 2026-04-15

### Other
- Release version 0.1.5

