---
name: assistant
description: 智能助手 - 一句话需求，智能调度执行
context: fork
agent: coordinator
---

# 智能助手

使用 `/assistant [需求]` 让管家帮你处理任务。

## 使用方式

```
/assistant 帮我加个用户登录功能
```

## 说明

此命令会调用 coordinator，coordinator 会：
- 分析需求
- 制定执行方案
- 调度合适的角色执行
- 监控进度并收集结果
