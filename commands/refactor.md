---
name: refactor
description: "重构代码 - 安全渐进地改善代码结构，不改变外部行为"
context: fork
agent: ai-assistant:executor
---

安全重构以下代码。

## 重构目标

$ARGUMENTS

## 要求

1. 先确认有测试覆盖（没有先补测试）
2. 评估影响范围
3. 单步重构 + 每步验证（绿灯起步，绿灯结束）
4. 不在重构中混入功能改动
5. 完成后运行完整测试套件
