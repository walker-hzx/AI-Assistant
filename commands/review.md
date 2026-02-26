---
name: review
description: 代码审查 - 智能调度执行
context: fork
agent: coordinator
---

# 代码审查

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
