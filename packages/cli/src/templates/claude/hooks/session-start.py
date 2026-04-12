#!/usr/bin/env python3
"""
Session Start Hook for bwflow
在 Claude Code 会话开始时注入项目上下文
"""

import os
import sys
from pathlib import Path

# 路径常量
DIR_WORKFLOW = "bwflow"
DIR_BLUEPRINT = "blueprint"
FILE_BLUEPRINT_README = "README.md"
FILE_CURRENT_TASK = ".current-task"
DIR_SHADOW_CONTEXT = ".claude-shadow-context"
FILE_LAST_SESSION = "last-session.md"


def get_blueprint_readme() -> Path:
    """获取蓝图入口文件"""
    return Path(DIR_WORKFLOW) / DIR_BLUEPRINT / FILE_BLUEPRINT_README


def get_current_task() -> str | None:
    """获取当前任务"""
    task_file = Path(FILE_CURRENT_TASK)
    if task_file.exists():
        return task_file.read_text().strip()
    return None


def read_blueprint() -> str:
    """读取根蓝图"""
    blueprint_path = get_blueprint_readme()
    if blueprint_path.exists():
        return blueprint_path.read_text()
    return ""


def read_last_session() -> str:
    """读取上次会话摘要"""
    session_file = Path(DIR_SHADOW_CONTEXT) / FILE_LAST_SESSION
    if session_file.exists():
        return session_file.read_text()
    return ""


def main():
    """主入口"""
    print("\n" + "=" * 60)
    print("🔷 bwflow Session Start")
    print("=" * 60)

    # 读取蓝图
    blueprint = read_blueprint()
    if blueprint:
        print("\n📋 项目架构 (Blueprint):")
        print("-" * 40)
        # 只显示前 50 行
        lines = blueprint.split("\n")[:50]
        for line in lines:
            print(f"  {line}")
        if len(blueprint.split("\n")) > 50:
            print("  ... (更多内容见 bwflow/blueprint/README.md)")
    else:
        print("\n⚠️  未找到项目蓝图")
        print("  运行 'bw init' 初始化项目")

    # 读取当前任务
    current_task = get_current_task()
    if current_task:
        print(f"\n📌 当前任务: {current_task}")
    else:
        print("\n📌 当前任务: 无")

    # 读取上次会话
    last_session = read_last_session()
    if last_session:
        print("\n📜 上次会话摘要:")
        print("-" * 40)
        # 只显示前 20 行
        lines = last_session.split("\n")[:20]
        for line in lines:
            print(f"  {line}")
        if len(last_session.split("\n")) > 20:
            print("  ... (更多内容见 .claude-shadow-context/last-session.md)")
    else:
        print("\n📜 上次会话: 无记录")

    print("\n" + "=" * 60)
    print("💡 使用 '/bw align' 检查蓝图对齐")
    print("💡 使用 '/bw finish' 完成任务")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
