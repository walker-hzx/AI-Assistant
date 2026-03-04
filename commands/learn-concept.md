---
name: learn-concept
description: "学习概念 - 搜索并学习不确定的技术概念"
context: fork
skill: coordinator
---

# 学习概念

**【重要】此命令通过 Skill 智能调度执行**

使用 `/learn-concept` 搜索并学习不确定的概念，coordinator 会智能调度。

## 使用方式

```
/learn-concept
/learn-concept 什么是 CQRS
```

## 功能

1. **概念解释** - 用通俗易懂的语言解释概念
2. **相关知识** - 提供相关的学习资源
3. **实际应用** - 给出代码示例和应用场景
4. **对比分析** - 与相似概念进行对比

## 说明

此命令会调用 coordinator，coordinator 会：
- 分析要学习的概念
- 决定是否需要 researcher 查资料
- 调度合适的角色协助
