---
name: assistant
description: "智能助手入口 - 一句话需求，智能调度执行"
user-invocable: true
---

# 智能助手

**一句话需求，智能调度执行**

---

## 使用方式

```
/assistant [你的需求]

例如：
/assistant 帮我加个用户登录功能
/assistant 修复登录页面的拼写错误
/assistant 帮我优化下接口性能
```

---

## 工作流程

当你输入需求后：

1. **理解需求** - 分析你真正想要什么
2. **制定方案** - 选择合适的角色组合
3. **执行** - 调度角色完成任务
4. **记录** - 创建执行文档

---

## 典型场景

| 场景 | 输入 | 管家会 |
|------|------|--------|
| 新功能 | `/assistant 加个用户管理功能` | 需求分析 → 计划 → 执行 → 验证 |
| Bug修复 | `/assistant 登录接口报错了` | 调试 → 修复 → 验证 |
| 代码优化 | `/assistant 优化下用户查询性能` | 分析 → 优化 → 验证 |
| 简单任务 | `/assistant 改个变量名` | 直接处理，记录结果 |

---

## 底层实现

此入口会调用 `coordinator` Agent 来处理任务。

具体流程由 coordinator 的子技能完成：
- coordinator-intent：意图分析
- coordinator-planning：方案制定
- coordinator-dispatch：任务派发
- coordinator-optimization：调度优化
