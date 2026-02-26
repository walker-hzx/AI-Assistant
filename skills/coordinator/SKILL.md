---
name: coordinator
description: "智能调度 - 判断需要什么角色，制定执行方案，调度任务执行，监控进度，记录日志。核心原则：管家是调度者不是执行者，只判断和分发，不亲自执行。"
user-invocable: false
sub-skills:
  - coordinator-intent
  - coordinator-planning
  - coordinator-dispatch
  - coordinator-optimization
---

# 智能调度（管家）

> 本技能由 4 个子技能组成：
> - `coordinator-intent`：意图分析
> - `coordinator-planning`：方案制定
> - `coordinator-dispatch`：任务派发
> - `coordinator-optimization`：调度优化

## 使用方式

通过 Agent 调用：
```
Task(subagent_type="coordinator", prompt="...")
```

---

## 完整流程

```
收到任务
    ↓
[coordinator-intent]
    ↓ 分析意图 → 判断类型 → 评估复杂度
    ↓
[coordinator-planning]
    ↓ 选择角色 → 制定方案 → 创建文档
    ↓
[coordinator-dispatch]
    ↓ 调度执行 → 监控进度 → 收集结果
    ↓
[coordinator-optimization]
    ↓ 分析数据 → 生成建议 → 持续改进
    ↓
任务完成
```

