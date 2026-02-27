---
name: review
description: "智能调度：coordinator代码审查 - coordinator 智能调度执行"
context: fork
skill: coordinator
---

# 代码审查

**【重要】此命令通过 Skill 智能调度执行**

使用 `/review` 进行代码审查，coordinator 会智能调度。

## 使用方式

```
/review
/review src/auth/login.ts
```

## 审查内容

- 正确性检查
- 安全性检查
- 性能检查
- 代码质量
- 测试覆盖

## 说明

此命令会调用 coordinator，coordinator 会：
- 分析代码
- 决定是否需要 code-reviewer
- 调度合适的角色执行
