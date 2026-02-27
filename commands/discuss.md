---
name: discuss
description: "智能调度：coordinator开始需求讨论 - 帮助明确需求，coordinator 智能调度执行"
context: fork
agent: coordinator
---

# 需求讨论

**【重要】此命令通过 coordinator 智能调度执行**

使用 `/discuss` 开始需求讨论，coordinator 会根据需求智能调度。

## 功能

1. 询问背景（目标、用户、价值）
2. 探索功能（核心功能、用户流程、输入输出）
3. 识别边界（异常情况、边界条件）
4. 记录需求

## 使用方式

```
/discuss
/discuss 帮我加个用户登录功能
```

## 说明

此命令会调用 coordinator，coordinator 会分析需求并决定调用哪个角色：
- 需求不清晰 → 调用 requirements-analyst
- 需要计划 → 调用 planner
- 需要实现 → 调用 executor
