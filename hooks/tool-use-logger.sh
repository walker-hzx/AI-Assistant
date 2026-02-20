#!/usr/bin/env bash
# AI Assistant 插件的 ToolUseStart 钩子 - 记录工具使用日志

set -euo pipefail

# 确定插件根目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
PLUGIN_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# 确保日志目录存在
LOG_DIR="${PLUGIN_ROOT}/logs"
mkdir -p "$LOG_DIR"

# 获取工具名称和参数
TOOL_NAME="${1:-unknown}"
ARGS="${2:-}"

# 获取时间戳
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# 写入日志文件
echo "[${TIMESTAMP}] Tool: ${TOOL_NAME}" >> "${LOG_DIR}/tool-use.log"

exit 0
