---
name: team-generator
description: "智能调度：coordinator生成团队配置 - coordinator 智能调度执行"
context: fork
skill: coordinator
---

# 团队生成器

**【重要】此命令通过 Skill 智能调度执行**

使用 `/team-generator` 创建 Claude Agent Team 配置，coordinator 会智能调度。

## 使用方式

```
/team-generator
/team-generator 并行研究多个技术方案
```

## 功能

1. **分析需求** - 确定团队规模和角色
2. **生成配置** - 创建团队 JSON 配置
3. **定义任务** - 分配任务给各成员
4. **输出结果** - 生成可用的团队配置

## 说明

此命令会调用 coordinator，coordinator 会：
- 分析需求
- 决定需要哪些角色
- 调度合适的角色生成配置
