---
name: security-review
description: "安全审查 - 识别 OWASP Top 10 漏洞，检查密钥泄露和注入风险"
context: fork
agent: ai-assistant:reviewer
---

**专注安全维度**审查以下代码。

## 审查范围

$ARGUMENTS

未指定范围时，扫描项目中的安全敏感代码（认证、授权、数据处理、API 接口）。

## 重点检查

- OWASP Top 10 漏洞
- 硬编码的 API 密钥和凭据
- 用户输入验证和清理
- SQL/XSS/命令注入风险
- 依赖包已知漏洞
