/**
 * Init Command
 * 初始化 bwflow 结构到用户项目
 */
import chalk from "chalk";
import fs from "fs-extra";
import { join, dirname, relative } from "node:path";
import { fileURLToPath } from "node:url";
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
// bwflow 核心目录（dist/commands/ -> dist -> packages/cli -> packages -> 项目根 -> .bwflow）
const BWFLOW_SOURCE = join(__dirname, "..", "..", "..", "..", ".bwflow");
// 工具模板目录（dist/commands/ -> dist/templates/）
const TEMPLATES_DIR = join(__dirname, "..", "templates");
const SUPPORTED_TYPES = ["claude"];
/**
 * 初始化 bwflow 结构
 */
export async function initCommand(options) {
    const cwd = process.cwd();
    console.log(chalk.blue("\n🔷 bwflow 初始化\n"));
    console.log(chalk.gray(`目标目录: ${cwd}`));
    // 确定初始化类型
    const initType = options.type || "claude";
    if (!SUPPORTED_TYPES.includes(initType)) {
        console.log(chalk.red(`不支持的类型: ${initType}`));
        console.log(chalk.gray(`支持的类型: ${SUPPORTED_TYPES.join(", ")}\n`));
        return;
    }
    console.log(chalk.gray(`初始化类型: ${initType}\n`));
    // 1. 复制 bwflow 核心到 .bwflow/
    initBwflow(cwd);
    // 2. 复制工具模板到 .claude/
    initToolIntegration(cwd, initType);
    console.log(chalk.green("\n✅ bwflow 初始化完成!\n"));
    console.log(chalk.cyan("下一步:"));
    console.log(chalk.gray("  1. 编辑 .bwflow/blueprint/README.md 添加项目架构"));
    console.log(chalk.gray("  2. 运行 /bw start 开始会话\n"));
}
/**
 * 复制 bwflow 核心到 .bwflow/
 */
function initBwflow(cwd) {
    console.log(chalk.cyan("📦 初始化 bwflow 核心...\n"));
    // 检查 bwflow 源目录
    if (!fs.existsSync(BWFLOW_SOURCE)) {
        console.log(chalk.red(`❌ 找不到 bwflow 源目录: ${BWFLOW_SOURCE}`));
        return;
    }
    // 复制整个 bwflow 目录到 .bwflow
    const destDir = join(cwd, ".bwflow");
    copyDirectory(BWFLOW_SOURCE, destDir, cwd, {
        excludeDirs: ["__pycache__", ".git"],
        excludeFiles: ["README.md"], // 不复制 bwflow 自己的 README
    });
}
/**
 * 复制工具模板到 .claude/
 */
function initToolIntegration(cwd, type) {
    console.log(chalk.cyan(`\n🔧 初始化 ${type} 集成...\n`));
    const toolTemplateDir = join(TEMPLATES_DIR, type);
    if (!fs.existsSync(toolTemplateDir)) {
        console.log(chalk.yellow(`⚠️  未找到 ${type} 模板目录`));
        return;
    }
    const destDir = join(cwd, ".claude");
    copyDirectory(toolTemplateDir, destDir, cwd, {
        excludeDirs: ["__pycache__"],
    });
}
/**
 * 递归复制目录
 */
function copyDirectory(src, dest, cwd, options = {}) {
    if (!fs.existsSync(src))
        return;
    const { excludeDirs = [], excludeFiles = [] } = options;
    const entries = fs.readdirSync(src, { withFileTypes: true });
    for (const entry of entries) {
        // 跳过排除的目录
        if (excludeDirs.includes(entry.name))
            continue;
        // 跳过排除的文件
        if (excludeFiles.includes(entry.name))
            continue;
        const srcPath = join(src, entry.name);
        const destPath = join(dest, entry.name);
        const relPath = relative(cwd, destPath);
        if (entry.isDirectory()) {
            fs.ensureDirSync(destPath);
            console.log(chalk.gray(`  ✓ ${relPath}/`));
            copyDirectory(srcPath, destPath, cwd, options);
        }
        else {
            fs.copySync(srcPath, destPath);
            console.log(chalk.gray(`  ✓ ${relPath}`));
        }
    }
}
