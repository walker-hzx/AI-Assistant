#!/usr/bin/env bash
# AI Assistant 插件的 SessionEnd 钩子
# 检查任务完成状态并建议下一步

set -euo pipefail

# 确定插件根目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
PLUGIN_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# 获取当前项目目录
current_dir="${CLAUDE_PROJECT_DIR:-$(pwd)}"

echo ""
echo "📊 检查任务完成状态..."

# 检查是否有进行中的任务
plans_dir="${current_dir}/docs/plans"
progress_file="${plans_dir}/progress.md"

if [ -f "$progress_file" ]; then
    # 检查是否有 in_progress 状态的任务
    if grep -qE "in_progress|🔄|进行中" "$progress_file" 2>/dev/null; then
        echo "⚠️  检测到进行中的任务"

        # 提取进行中的任务
        in_progress_tasks=$(grep -E "in_progress|🔄|进行中" "$progress_file" 2>/dev/null | head -3 || true)
        if [ -n "$in_progress_tasks" ]; then
            echo "   未完成的任务："
            echo "$in_progress_tasks" | sed 's/^/   - /'
        fi

        echo ""
        echo "💡 下次可以："
        echo "   - 说'/plan'继续执行当前任务"
        echo "   - 说'/blueprint'查看项目整体状态"
    else
        # 检查是否有待处理的任务
        if grep -qE "pending|待处理|未开始" "$progress_file" 2>/dev/null; then
            echo "✅ 当前任务已完成！"
            echo ""
            echo "💡 下次可以："
            echo "   - 开始新任务：'/discuss' 或 '/brainstorming'"
            echo "   - 更新蓝图：'/blueprint'"
            echo "   - 代码审查：'/review'"
        else
            echo "✅ 会话结束，感谢使用 AI Assistant！"
        fi
    fi
else
    echo "✅ 会话结束，感谢使用 AI Assistant！"
fi

echo ""

exit 0
