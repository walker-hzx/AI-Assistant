---
name: verification
description: "智能调度：coordinator验证功能 - coordinator 智能调度执行"
context: fork
skill: coordinator
---

# 功能验证

**【重要】此命令通过 Skill 智能调度执行**

使用 `/verification` 验证功能是否正确实现，coordinator 会智能调度。

## 使用方式

```
/verification
/verification 登录功能
```

## 功能

1. **代码质量检查** - 格式化、类型检查
2. **测试执行** - 单元测试、集成测试
3. **覆盖率检查** - 确保 80%+ 覆盖率
4. **安全扫描** - 检查漏洞和硬编码密钥

## 说明

此命令会调用 coordinator，coordinator 会：
- 分析需求和实现
- 决定是否需要 qa
- 调度合适的角色验证
