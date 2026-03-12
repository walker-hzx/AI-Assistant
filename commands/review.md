---
name: review
description: "代码审查 - 审查代码质量、安全性，给出可操作改进建议"
context: fork
agent: ai-assistant:reviewer
---

审查代码质量和安全性，给出具体可操作的改进建议。

## 审查范围

$ARGUMENTS

未指定范围时，审查最近一次 git commit 的变更（使用 `git diff HEAD~1` 获取变更文件列表）。

## 审查维度

按优先级：正确性 → 安全性 → 性能 → 可维护性 → 规范

## 输出要求

- 按严重程度分级：🔴 阻断 / 🟠 重要 / 🟡 建议
- 每个问题附具体修复建议
- 最终结论：通过 / 有条件通过 / 未通过
