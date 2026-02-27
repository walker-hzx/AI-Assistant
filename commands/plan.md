---
name: plan
description: "【必须通过管家】制定详细实施计划 - coordinator 智能调度执行"
context: fork
agent: coordinator
---

# 制定计划

**【重要】此命令必须通过 coordinator（管家）调度执行**

使用 `/plan` 制定详细实施计划，coordinator 会智能调度。

## 使用方式

```
/plan
/plan 用户登录功能
```

## 前置条件

在运行此命令之前，需要确保：
- 需求已明确
- 已完成 brainstorming（如需要）

## 说明

此命令会调用 coordinator，coordinator 会分析情况并决定：
- 需求是否明确
- 需要哪些角色
- 执行顺序是什么
