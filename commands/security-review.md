---
name: security-review
description: "智能调度：coordinator安全审查专家 - coordinator 智能调度执行"
context: fork
agent: coordinator
---

# 安全审查

**【重要】此命令通过 coordinator 智能调度执行**

使用 `/security-review` 进行代码安全审查，coordinator 会智能调度。

## 使用方式

```
/security-review
/security-review src/api/auth
```

## 功能

1. **漏洞检测** - 识别 OWASP Top 10 问题
2. **密钥检测** - 查找硬编码的 API 密钥
3. **输入验证** - 检查用户输入是否经过适当清理
4. **依赖安全** - 检查有漏洞的依赖包

## 说明

此命令会调用 coordinator，coordinator 会：
- 分析代码
- 决定是否需要 security-reviewer
- 调度合适的角色执行
