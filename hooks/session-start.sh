#!/usr/bin/env bash
# AI Assistant 插件的 SessionStart 钩子

set -euo pipefail

# 确定插件根目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
PLUGIN_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# 读取当前项目信息
project_name=""
if [ -f "${PLUGIN_ROOT}/README.md" ]; then
    project_name=$(head -1 "${PLUGIN_ROOT}/README.md" | sed 's/^# //')
fi

# 构建欢迎消息
welcome_message="欢迎使用 AI Assistant！"

if [ -n "$project_name" ]; then
    welcome_message="${welcome_message} 当前项目: ${project_name}"
fi

# 输出欢迎消息
echo "✅ ${welcome_message}"

# 检查可用的 skills
skills_dir="${PLUGIN_ROOT}/skills"
if [ -d "$skills_dir" ]; then
    skill_count=$(find "$skills_dir" -maxdepth 1 -type d | tail -n +2 | wc -l)
    echo "📦 已加载 ${skill_count} 个 skills"
fi

# 检查可用的 agents
agents_dir="${PLUGIN_ROOT}/agents"
if [ -d "$agents_dir" ]; then
    agent_count=$(find "$agents_dir" -maxdepth 1 -name "*.md" | wc -l)
    echo "🤖 已加载 ${agent_count} 个 agents"
fi

# 检查可用的 commands
commands_dir="${PLUGIN_ROOT}/commands"
if [ -d "$commands_dir" ]; then
    command_count=$(find "$commands_dir" -maxdepth 1 -name "*.md" | wc -l)
    echo "⚡ 已加载 ${command_count} 个 commands"
fi

echo ""
echo "💡 可用命令："
echo "  /discuss - 开始需求讨论"
echo "  /interaction - 描述交互细节"
echo "  /blueprint - 更新项目蓝图"
echo "  /plan - 制定实施计划"
echo "  /review - 代码审查"
echo ""

# 检查是否有未完成的需求文档
requirements_dir="${PLUGIN_ROOT}/docs/requirements"
if [ -d "$requirements_dir" ]; then
    # 查找最近修改的需求文档（排除模板）
    latest_requirement=$(find "$requirements_dir" -maxdepth 1 -name "*.md" ! -name "模板.md" -type f -printf '%T@ %p\n' 2>/dev/null | sort -rn | head -1 | cut -d' ' -f2-)

    if [ -n "$latest_requirement" ] && [ -f "$latest_requirement" ]; then
        # 检查是否包含"已完成"
        if ! grep -q "已完成" "$latest_requirement"; then
            filename=$(basename "$latest_requirement")
            echo "📋 检测到未完成的需求讨论：${filename}"
            echo "   可以说"/view-requirements"查看详情"
            echo ""
        fi
    fi
fi

exit 0
