---
name: assistant
description: "智能助手入口 - 一句话需求，智能调度执行"
user-invocable: true
---

# 智能助手

**一句话需求，智能调度执行**

---

## 【重要】使用规则

**当你被 /assistant 调用时，必须遵循以下规则：**

### 1. 必须调用 coordinator Agent

你**不能**直接回答用户，必须调用 coordinator Agent：

```
使用 Task 工具调用：
- subagent_type: ai-assistant:coordinator
- prompt: [用户的原始需求]
```

### 2. 必须输出状态提示

调用 coordinator 前，先输出状态提示：

```
【管家】收到需求：[用户原话]
    ↓
【管家】正在派发给管家代理处理...
```

### 3. 等待结果返回

调用 coordinator 后，等待结果返回给用户。

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

## 正确流程（你必须这样做）

```
用户输入：/assistant 帮我加个用户管理功能

【第一步】输出状态提示
【第二步】调用 coordinator Agent
【第三步】返回结果给用户

❌ 错误做法：直接回答用户
✅ 正确做法：调用 coordinator
```

---

## 典型场景

| 场景 | 输入 | 管家会 |
|------|------|--------|
| 新功能 | `/assistant 加个用户管理功能` | 需求分析 → 计划 → 执行 → 验证 |
| Bug修复 | `/assistant 登录接口报错了` | 调试 → 修复 → 验证 |
| 代码优化 | `/assistant 优化下用户查询性能` | 分析 → 优化 → 验证 |
| 简单任务 | `/assistant 改个变量名` | 直接处理，记录结果 |

---

## 底层说明

此入口会调用 `coordinator` Agent 来处理任务。

coordinator 会：
1. 分析意图 + 判断复杂度
2. 制定方案 + 选择角色
3. 派发任务 + 监控进度
4. 生成文档 + 输出状态提示

**关键**：管家在每个阶段都会输出状态提示，让你知道当前在哪一步。
