---
name: assistant
description: "智能助手入口 - 一句话需求，智能调度执行"
user-invocable: true
---

# 智能助手

**一句话需求，智能调度执行**

---

## 【强制规则】

当你被 `/assistant` 调用时：

### 第一步：立即输出状态提示

```
【管家】收到需求：[用户原话]
    ↓
【管家】正在派发给管家代理处理...
```

### 第二步：必须调用 coordinator

使用 Task 工具调用：

```
Task(
  subagent_type="ai-assistant:coordinator",
  prompt="[用户的原始需求]"
)
```

### 第三步：返回结果

等待 coordinator 处理完成，返回结果给用户。

---

## 【禁止事项】

❌ 禁止直接回答用户
❌ 禁止自己处理任务
✅ 必须调用 coordinator

---

## 使用示例

```
用户：/assistant 帮我加个用户登录功能

你必须：
1. 输出【管家】收到需求...
2. 调用 Task(ai-assistant:coordinator, prompt="帮我加个用户登录功能")
3. 返回结果
```
