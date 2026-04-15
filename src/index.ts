#!/usr/bin/env node

/**
 * bwflow CLI
 * Blueprint Workflow CLI - 蓝图驱动的结构化 AI 开发伴侣
 * 基于 Trellis + 蓝图层
 */

import { Command } from "commander";
import chalk from "chalk";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { initCommand } from "./commands/init.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// 从 package.json 读取版本号
const packageJson = JSON.parse(
  readFileSync(join(__dirname, "..", "package.json"), "utf-8")
);

const program = new Command();

program
  .name("bw")
  .description("bwflow - Blueprint Workflow CLI (Trellis + Blueprint Layer)")
  .version(packageJson.version);

// init - 初始化项目
program
  .command("init")
  .description("初始化 bwflow 结构到当前项目")
  .requiredOption("-t, --type <type>", "初始化类型 (claude/cursor/kiro)")
  .option("-u, --user <name>", "开发者名称")
  .option("-y, --yes", "跳过确认提示")
  .option("-f, --force", "强制覆盖已存在的文件")
  .action(async (options) => {
    await initCommand(options);
  });

// sync - 同步到平台（alias for init）
program
  .command("sync")
  .description("同步 bwflow 配置")
  .action(async () => {
    console.log(chalk.blue("\n🔄 bwflow 同步\n"));
    console.log(chalk.gray("运行 'bw init' 已包含同步功能\n"));
  });

program.parse();
