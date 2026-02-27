---
name: assistant
description: "智能助手入口 - 一句话需求，智能调度执行"
context: fork
skill: coordinator
---

# 智能助手

**【重要】此命令通过 Skill 智能调度执行**

使用 `/assistant [需求]` 让管家帮你处理任务。

## 使用方式

```
/assistant 帮我加个用户登录功能
```

## 说明

此命令会调用 coordinator skill，coordinator 会：
- 创建调度记录
- 分析需求意图
- 制定执行方案
- 调度合适的角色执行（需求分析 → 计划 → 执行 → 验证 → 审查）
- 监控进度并收集结果
- 每个阶段生成对应文档
