---
name: executing-plans
description: "执行计划 - 按照实施计划逐步执行，带审查检查点"
skill: coordinator
---

# 执行计划

**【重要】此命令通过 Skill 智能调度执行**

使用 `/executing-plans` 根据计划执行开发任务，coordinator 会智能调度。

## 使用方式

```
/executing-plans
/executing-plans 用户登录功能
```

## 功能

1. 读取计划文件（`docs/plans/YYYY-MM-DD-<feature>-*.md`）
2. 按任务列表逐步执行
3. 每个任务完成后更新状态
4. 遇到问题进行调试修复

## 说明

此命令会调用 coordinator，coordinator 会：
- 读取计划文件
- 分析当前进度
- 决定是否需要 executor
- 调度合适的角色执行
