#!/bin/bash
# hooks/permission-guard.sh
# PreToolUse 钩子 - 在危险操作前验证

TOOL_NAME="$1"
COMMAND="$2"

# 危险命令黑名单
DANGEROUS_COMMANDS=("rm -rf" "git push --force" "DROP TABLE")

for cmd in "${DANGEROUS_COMMANDS[@]}"; do
  if echo "$COMMAND" | grep -q "$cmd"; then
    echo "BLOCKED: Dangerous command detected: $cmd"
    exit 1
  fi
done

exit 0
