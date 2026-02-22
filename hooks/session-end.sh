#!/usr/bin/env bash
# AI Assistant 插件的 SessionEnd 钩子
# 简洁地检查任务状态，避免过度打扰

set -euo pipefail

# 确定插件根目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
PLUGIN_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# 获取当前项目目录
current_dir="${CLAUDE_PROJECT_DIR:-$(pwd)}"

# 检查是否有进度文件
plans_dir="${current_dir}/docs/plans"
progress_file="${plans_dir}/progress.md"

# 只在有进度文件且有未完成任务时才显示提示
if [ -f "$progress_file" ]; then
    # 检查是否有 in_progress 状态的任务
    if grep -qE "in_progress|🔄" "$progress_file" 2>/dev/null; then
        echo ""
        echo "📝 有进行中的任务，下次可用 /plan 继续"
    elif grep -qE "pending|待处理" "$progress_file" 2>/dev/null; then
        echo ""
        echo "✅ 任务完成，下次可用 /discuss 开始新任务"
    fi
fi

# 简洁结束，不显示冗长提示
# 避免过度打扰用户

exit 0
