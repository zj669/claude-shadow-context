/**
 * Template Loader
 * 模板加载器 - 从源目录读取模板文件
 */

import { readFileSync, readdirSync, existsSync, statSync } from "node:fs";
import { join, resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = fileURLToPath(new URL(".", import.meta.url));

// 在 dist 环境中，从 ../ 源目录读取模板
// 在 dev 环境中，从 ./src/templates 读取
function findTemplatesBase(): string {
  // 优先从源目录加载（开发和生产都适用）
  const srcDir = resolve(__dirname, "..", "templates");
  if (existsSync(srcDir)) {
    return srcDir;
  }

  // 回退到当前目录
  return __dirname;
}

/**
 * 获取模板目录的绝对路径
 */
export function getTemplatesDir(): string {
  return findTemplatesBase();
}

/**
 * 获取 Claude 模板目录的绝对路径
 */
export function getClaudeTemplatesDir(): string {
  return join(getTemplatesDir(), "claude");
}

/**
 * 加载模板文件内容
 */
export function loadTemplate(relativePath: string): string {
  const fullPath = join(getTemplatesDir(), relativePath);
  if (!existsSync(fullPath)) {
    throw new Error(`Template not found: ${relativePath}`);
  }
  return readFileSync(fullPath, "utf-8");
}

/**
 * 获取模板目录下的所有文件
 */
export function listTemplates(dir: string = ""): string[] {
  const baseDir = dir ? join(getTemplatesDir(), dir) : getTemplatesDir();
  const files: string[] = [];

  function walk(directory: string, prefix: string = "") {
    try {
      const entries = readdirSync(directory);
      for (const entry of entries) {
        const fullPath = join(directory, entry);
        const relativePath = prefix ? `${prefix}/${entry}` : entry;

        if (statSync(fullPath).isDirectory()) {
          walk(fullPath, relativePath);
        } else {
          files.push(relativePath);
        }
      }
    } catch {
      // 忽略无法访问的目录
    }
  }

  walk(baseDir, dir);
  return files;
}

/**
 * 检查模板文件是否存在
 */
export function templateExists(relativePath: string): boolean {
  const fullPath = join(getTemplatesDir(), relativePath);
  return existsSync(fullPath);
}

/**
 * 获取模板文件的绝对路径
 */
export function getTemplatePath(relativePath: string): string {
  return join(getTemplatesDir(), relativePath);
}
