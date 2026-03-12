---
name: verification
description: "功能验证 - 在声称完成前验证代码是否正确实现需求"
context: fork
agent: ai-assistant:tester
---

验证功能是否正确实现。

## 验证范围

$ARGUMENTS

## 验证清单

1. **代码质量** - 格式化、类型检查（lint/typecheck 通过）
2. **测试执行** - 运行单元测试和集成测试
3. **覆盖率** - 核心逻辑 100%，整体 ≥ 80%
4. **安全扫描** - 检查硬编码密钥和明显漏洞
5. **需求对照** - 逐条核对原始需求是否满足
