---
name: implement
description: "实现功能 - 直接告诉 executor 实现一个功能或改动"
context: fork
agent: ai-assistant:executor
---

实现以下功能或改动。

## 任务描述

$ARGUMENTS

## 要求

1. 先读取相关代码，理解现有结构
2. 确认任务假设成立（发现不对立即反馈）
3. 最小修改原则，TDD 驱动
4. 边界条件和异常情况都要处理
5. 完成后运行测试验证
