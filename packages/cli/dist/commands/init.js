/**
 * Init Command
 * 初始化 bwflow 结构到用户项目
 */
import chalk from "chalk";
import fs from "fs-extra";
import { join, dirname, relative } from "node:path";
import { fileURLToPath } from "node:url";
import { getClaudeTemplatesDir } from "../templates/index.js";
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
// Trellis 命令映射到 bwflow
const COMMAND_MAP = {
    "trellis/start": "start",
    "trellis/before-dev": "before-dev",
    "trellis/finish-work": "finish",
    "trellis/record-session": "record",
    "trellis/brainstorm": "brainstorm",
    "trellis/check": "check",
    "trellis/parallel": "parallel",
    "trellis/update-spec": "update-spec",
};
/**
 * 初始化 bwflow 结构
 */
export async function initCommand(options) {
    const cwd = process.cwd();
    const templatesDir = getClaudeTemplatesDir();
    console.log(chalk.blue("\n🔷 bwflow 初始化\n"));
    console.log(chalk.gray(`目标目录: ${cwd}`));
    console.log(chalk.gray(`模板目录: ${templatesDir}\n`));
    // 检查是否已存在 .bwflow
    const bwflowDir = join(cwd, ".bwflow");
    if (fs.existsSync(bwflowDir) && !options.force) {
        console.log(chalk.yellow("⚠️  .bwflow 目录已存在"));
        console.log(chalk.gray("使用 --force 强制覆盖\n"));
        return;
    }
    // 创建 .bwflow 目录结构（与 Trellis 保持一致，增加 blueprint 层）
    const dirsToCreate = [
        bwflowDir,
        join(bwflowDir, "blueprint"),
        join(bwflowDir, "spec"),
        join(bwflowDir, "spec", "backend"),
        join(bwflowDir, "spec", "frontend"),
        join(bwflowDir, "tasks"),
        join(bwflowDir, "workspace"),
        join(bwflowDir, "scripts"),
    ];
    console.log(chalk.cyan("📂 创建目录:\n"));
    for (const dir of dirsToCreate) {
        const relPath = relative(cwd, dir);
        fs.ensureDirSync(dir);
        console.log(chalk.gray(`  ✓ ${relPath}/`));
    }
    // 复制 scripts 模板
    const srcScriptsDir = join(templatesDir, "scripts");
    const destScriptsDir = join(bwflowDir, "scripts");
    console.log(chalk.cyan("\n📁 复制 Scripts 模板:\n"));
    if (fs.existsSync(srcScriptsDir)) {
        copyDirectoryRecursive(srcScriptsDir, destScriptsDir, cwd);
    }
    // 复制 hooks 模板
    const srcHooksDir = join(templatesDir, "hooks");
    const destHooksDir = join(bwflowDir, "scripts", "hooks");
    console.log(chalk.cyan("\n📁 复制 Hooks 模板:\n"));
    if (fs.existsSync(srcHooksDir)) {
        fs.ensureDirSync(destHooksDir);
        const hooks = fs.readdirSync(srcHooksDir);
        for (const hook of hooks) {
            if (hook.endsWith(".py")) {
                const srcFile = join(srcHooksDir, hook);
                const destFile = join(destHooksDir, hook);
                fs.copySync(srcFile, destFile, { overwrite: options.force || false });
                console.log(chalk.gray(`  ✓ ${relative(cwd, destFile)}`));
            }
        }
    }
    // 创建根蓝图 README
    const blueprintReadme = join(bwflowDir, "blueprint", "README.md");
    if (!fs.existsSync(blueprintReadme) || options.force) {
        const readmeContent = `# 项目架构蓝图

## 概述
[项目简介：一句话描述项目是什么、解决什么问题]

## 核心能力
1. [能力1]
2. [能力2]
3. [能力3]

## 目录结构
- \`src/\` - 源码目录
- \`scripts/\` - 脚本目录
- \`config/\` - 配置目录
- \`tests/\` - 测试目录

## 关键设计决策
1. [决策1]: [原因]
2. [决策2]: [原因]

## 入口点
- 主入口: [文件路径]
- CLI 入口: [文件路径]

## Change Log
- ${new Date().toISOString().split("T")[0]} Initial
`;
        fs.writeFileSync(blueprintReadme, readmeContent, "utf-8");
        console.log(chalk.gray(`  ✓ ${relative(cwd, blueprintReadme)}`));
    }
    // 创建规范索引
    const specIndex = join(bwflowDir, "spec", "index.md");
    const specIndexContent = `# 规范索引

## 目录

- \`backend/\` - 后端开发规范
- \`frontend/\` - 前端开发规范

## 使用方式

在开发前运行 \`/bw before-dev\` 读取相关规范。
`;
    fs.writeFileSync(specIndex, specIndexContent, "utf-8");
    console.log(chalk.gray(`  ✓ ${relative(cwd, specIndex)}`));
    // 创建 workflow.md
    const workflowPath = join(bwflowDir, "workflow.md");
    const workflowContent = `# bwflow 工作流

## 核心原则

1. **先读后写**：开始实现前，先阅读规范和蓝图
2. **遵循规范**：按照项目规范编写代码
3. **上下文注入**：通过任务上下文确保 agent 理解项目

## 开发流程

\`\`\`
/bw start      -> 开始会话
/bw before-dev -> 开发前读取规范
[实现功能]
/bw finish     -> 提交前检查
git commit
/bw record     -> 记录会话
\`\`\`
`;
    fs.writeFileSync(workflowPath, workflowContent, "utf-8");
    console.log(chalk.gray(`  ✓ ${relative(cwd, workflowPath)}`));
    // 同步命令到 Claude Code
    await syncCommandsToClaudeCode(cwd, templatesDir);
    console.log(chalk.green("\n✅ bwflow 初始化完成!\n"));
    console.log(chalk.cyan("下一步:"));
    console.log(chalk.gray("  1. 编辑 .bwflow/blueprint/README.md 添加项目架构"));
    console.log(chalk.gray("  2. 运行 /bw start 开始会话\n"));
}
/**
 * 递归复制目录
 */
function copyDirectoryRecursive(src, dest, cwd) {
    if (!fs.existsSync(src))
        return;
    const entries = fs.readdirSync(src, { withFileTypes: true });
    for (const entry of entries) {
        const srcPath = join(src, entry.name);
        const destPath = join(dest, entry.name);
        const relPath = relative(cwd, destPath);
        if (entry.isDirectory()) {
            fs.ensureDirSync(destPath);
            console.log(chalk.gray(`  ✓ ${relPath}/`));
            copyDirectoryRecursive(srcPath, destPath, cwd);
        }
        else if (entry.name.endsWith(".py")) {
            fs.copySync(srcPath, destPath, { overwrite: true });
            console.log(chalk.gray(`  ✓ ${relPath}`));
        }
    }
}
/**
 * 同步命令到 Claude Code
 */
async function syncCommandsToClaudeCode(cwd, templatesDir) {
    console.log(chalk.cyan("\n🔄 同步命令到 Claude Code...\n"));
    const srcCommandsDir = join(templatesDir, "commands", "trellis");
    const destCommandsDir = join(cwd, ".claude", "commands", "bwflow");
    if (!fs.existsSync(srcCommandsDir)) {
        console.log(chalk.yellow("  ⚠️  未找到命令模板"));
        return;
    }
    fs.ensureDirSync(destCommandsDir);
    const cmdDirs = fs.readdirSync(srcCommandsDir);
    let count = 0;
    for (const cmdDir of cmdDirs) {
        const srcCmdDir = join(srcCommandsDir, cmdDir);
        if (!fs.statSync(srcCmdDir).isDirectory())
            continue;
        // 只复制映射中存在的命令
        const mappedName = COMMAND_MAP[`trellis/${cmdDir}`];
        if (!mappedName)
            continue;
        const destCmdDir = join(destCommandsDir, mappedName);
        fs.ensureDirSync(destCmdDir);
        const files = fs.readdirSync(srcCmdDir);
        for (const file of files) {
            if (file.endsWith(".md")) {
                const srcFile = join(srcCmdDir, file);
                const destFile = join(destCmdDir, file);
                fs.copySync(srcFile, destFile, { overwrite: true });
                count++;
            }
        }
    }
    console.log(chalk.gray(`  ✓ ${count} 个命令 → .claude/commands/bwflow/`));
    // 创建 README
    const readmeContent = `# bwflow Commands

Claude Code 集成 bwflow 协议命令。

## 核心命令

| 命令 | 说明 |
|------|------|
| \`/bw start\` | 开始会话 |
| \`/bw before-dev\` | 开发前读取规范 |
| \`/bw finish\` | 完成任务检查 |
| \`/bw record\` | 记录会话 |

## 完整命令列表

| 命令 | 说明 |
|------|------|
| \`/bw brainstorm\` | 需求探索 |
| \`/bw check\` | 通用检查 |
| \`/bw parallel\` | 并行任务 |
| \`/bw update-spec\` | 更新规范 |

## 开发流程

\`\`\`
/bw start      -> 开始会话
/bw before-dev -> 开发前读取规范
[实现功能]
/bw finish     -> 提交前检查
git commit
/bw record     -> 记录会话
\`\`\`
`;
    const readmeFile = join(destCommandsDir, "README.md");
    fs.writeFileSync(readmeFile, readmeContent, "utf-8");
    console.log(chalk.gray(`  ✓ README.md`));
}
