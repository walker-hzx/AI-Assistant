---
name: test-planner
description: "智能调度：coordinator测试设计专家 - coordinator 智能调度执行"
context: fork
skill: coordinator
---

# 测试设计

**【重要】此命令通过 Skill 智能调度执行**

使用 `/test-planner` 设计 E2E 测试场景和测试用例，coordinator 会智能调度。

## 使用方式

```
/test-planner
/test-planner 用户登录流程
```

## 功能

1. **需求分析** - 理解功能需求
2. **页面功能梳理** - 梳理页面交互和功能点
3. **测试场景设计** - 设计覆盖核心路径的测试场景
4. **测试用例编写** - 编写具体的测试用例

## 说明

此命令会调用 coordinator，coordinator 会：
- 分析测试需求
- 决定是否需要 tester
- 调度合适的角色设计测试
