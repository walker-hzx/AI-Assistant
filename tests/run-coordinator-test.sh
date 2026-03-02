#!/bin/bash

# 测试脚本：验证 coordinator 调度流程

TEST_DIR="/Users/huangzhixin/Desktop/Code/AI/AI-Assistant/tests/samples"
PROJECT_DIR="$TEST_DIR/test-project"

# 创建测试项目目录
mkdir -p "$PROJECT_DIR"

echo "=== 开始测试 Coordinator 调度流程 ==="
echo "测试目录: $PROJECT_DIR"
echo ""

# 运行 Claude CLI，调用 coordinator skill
# 任务：创建一个简单的用户登录功能
claude -p "使用 ai-assistant:coordinator skill，帮我创建一个简单的用户登录功能。不需要询问我确认，自己完成整个流程。生成代码放在当前目录下。" "$PROJECT_DIR"

echo ""
echo "=== 测试完成 ==="
echo "检查生成的文档..."
echo ""

# 检查生成的文档
echo "--- 调度记录 ---"
ls -la "$TEST_DIR/docs/coordinator/" 2>/dev/null || echo "未找到 coordinator 目录"

echo ""
echo "--- 需求文档 ---"
ls -la "$TEST_DIR/docs/intent/" 2>/dev/null || echo "未找到 intent 目录"

echo ""
echo "--- 计划文档 ---"
ls -la "$TEST_DIR/docs/plans/" 2>/dev/null || echo "未找到 plans 目录"

echo ""
echo "--- 生成的代码 ---"
ls -la "$PROJECT_DIR/" 2>/dev/null || echo "未找到项目目录"
