#!/bin/bash
# Commit Message Hook
# 规范化提交信息格式

INPUT_FILE="$1"

# 读取提交信息
COMMIT_MSG=$(cat "$INPUT_FILE")

# 检查是否符合格式
if [[ ! "$COMMIT_MSG" =~ ^(feat|fix|refactor|docs|test|chore|perf|ci): ]]; then
    echo "错误：提交信息格式不正确"
    echo "正确格式：feat: 添加新功能"
    echo "可用类型：feat, fix, refactor, docs, test, chore, perf, ci"
    exit 1
fi

exit 0
