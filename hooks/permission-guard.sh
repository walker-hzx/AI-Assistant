#!/bin/bash
# hooks/permission-guard.sh
# PreToolUse 钩子 - 在危险操作前验证

TOOL_NAME="$1"
TOOL_INPUT_JSON="$2"

# 从 JSON 中提取 command 字段
COMMAND=$(echo "$TOOL_INPUT_JSON" | jq -r '.command // empty')

# 如果无法提取命令，直接放行
if [ -z "$COMMAND" ]; then
  exit 0
fi

# 危险命令黑名单（使用固定字符串匹配）
DANGEROUS_COMMANDS=("rm -rf" "git push --force" "DROP TABLE")

for cmd in "${DANGEROUS_COMMANDS[@]}"; do
  if echo "$COMMAND" | grep -Fq "$cmd"; then
    echo "BLOCKED: Dangerous command detected: $cmd"
    exit 1
  fi
done

exit 0
