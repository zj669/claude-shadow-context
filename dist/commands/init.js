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
// bwflow 核心目录（dist/commands/ -> dist -> 项目根 -> bwflow）
const BWFLOW_SOURCE = join(__dirname, "..", "..", "bwflow");
// 工具模板目录（dist/commands/ -> dist/templates/）
const TEMPLATES_DIR = join(__dirname, "..", "templates");
const SUPPORTED_TYPES = ["claude", "cursor", "kiro"];
/**
 * 初始化 bwflow 结构
 */
export async function initCommand(options) {
    const cwd = process.cwd();
    console.log(chalk.blue("\n🔷 bwflow 初始化\n"));
    console.log(chalk.gray(`目标目录: ${cwd}`));
    // 确定初始化类型
    const initType = options.type;
    if (!SUPPORTED_TYPES.includes(initType)) {
        console.log(chalk.red(`\n❌ 不支持的类型: ${initType}`));
        console.log(chalk.gray(`支持的类型: ${SUPPORTED_TYPES.join(", ")}\n`));
        return;
    }
    console.log(chalk.gray(`初始化类型: ${initType}\n`));
    // 1. 复制 bwflow 核心到 .bwflow/
    initBwflow(cwd, options.user);
    // 2. 复制工具模板到对应目录
    initToolIntegration(cwd, initType);
    console.log(chalk.green("\n✅ bwflow 初始化完成!\n"));
    console.log(chalk.cyan("下一步:"));
    console.log(chalk.gray("  1. 编辑 .bwflow/blueprint/README.md 添加项目架构"));
    console.log(chalk.gray("  2. 运行 /bw start 开始会话\n"));
}
/**
 * 复制 bwflow 核心到 .bwflow/
 */
function initBwflow(cwd, userName) {
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
    // 如果提供了用户名，更新 config.yaml
    if (userName) {
        const configPath = join(destDir, "config.yaml");
        if (fs.existsSync(configPath)) {
            try {
                const configContent = fs.readFileSync(configPath, "utf-8");
                const updatedConfig = configContent.replace(/developer:\s*\n\s*name:\s*.*/, `developer:\n  name: ${userName}`);
                fs.writeFileSync(configPath, updatedConfig, "utf-8");
                console.log(chalk.gray(`  ✓ 设置开发者: ${userName}\n`));
            }
            catch (err) {
                console.log(chalk.yellow(`  ⚠️  无法更新开发者配置\n`));
            }
        }
    }
}
/**
 * 复制工具模板到对应目录
 */
function initToolIntegration(cwd, type) {
    console.log(chalk.cyan(`\n🔧 初始化 ${type} 集成...\n`));
    const toolTemplateDir = join(TEMPLATES_DIR, type);
    if (!fs.existsSync(toolTemplateDir)) {
        console.log(chalk.yellow(`⚠️  未找到 ${type} 模板目录`));
        return;
    }
    // 根据类型选择目标目录
    let destDir;
    if (type === "cursor") {
        destDir = join(cwd, ".cursor");
    }
    else if (type === "kiro") {
        destDir = join(cwd, ".kiro");
    }
    else {
        destDir = join(cwd, ".claude");
    }
    copyDirectory(toolTemplateDir, destDir, cwd, {
        excludeDirs: ["__pycache__"],
    });
    // 设置脚本执行权限（仅 Unix 系统）
    if (process.platform !== "win32") {
        const hooksDir = join(destDir, "hooks");
        if (fs.existsSync(hooksDir)) {
            const files = fs.readdirSync(hooksDir);
            for (const file of files) {
                const filePath = join(hooksDir, file);
                try {
                    fs.chmodSync(filePath, 0o755);
                }
                catch {
                    // 忽略权限设置失败
                }
            }
        }
        const scriptsDir = join(destDir, "scripts");
        if (fs.existsSync(scriptsDir)) {
            const files = fs.readdirSync(scriptsDir);
            for (const file of files) {
                if (file.endsWith(".py")) {
                    const filePath = join(scriptsDir, file);
                    try {
                        fs.chmodSync(filePath, 0o755);
                    }
                    catch {
                        // 忽略权限设置失败
                    }
                }
            }
        }
    }
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
