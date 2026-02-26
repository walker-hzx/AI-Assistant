---
name: assistant
description: "智能助手入口 - 一句话需求，智能调度执行"
user-invocable: true
---

# 智能助手

**一句话需求，智能调度执行**

---

## 【强制规则】

当你被 `/assistant` 调用时，必须按以下步骤执行：

### 第一步：输出状态提示

```
【管家】收到需求：[用户原话]
    ↓
【管家】正在处理...
```

### 第二步：调用 coordinator-intent Skill

使用 Skill 工具调用：

```
Skill: ai-assistant:coordinator-intent
```

**等待 skill 执行完成**，然后继续下一步。

### 第三步：调用 coordinator-planning Skill

```
Skill: ai-assistant:coordinator-planning
```

**等待 skill 执行完成**，然后继续下一步。

### 第四步：调用 coordinator-dispatch Skill

```
Skill: ai-assistant:coordinator-dispatch
```

**等待 skill 执行完成**。

### 第五步：检查文档

确认文档已生成：
- 普通任务：`docs/plans/YYYY-MM-DD-<task>-coordinator.md`

### 第六步：返回结果

向用户汇报完成情况。

---

## 【禁止事项】

❌ 禁止直接回答用户
❌ 禁止自己处理任务
❌ 禁止跳过任何步骤
✅ 必须按顺序执行所有步骤
✅ 必须确认文档已生成

---

## 使用示例

```
用户：/assistant 帮我加个用户登录功能

你必须：
1. 输出【管家】收到需求...
2. 调用 Skill(ai-assistant:coordinator-intent)
3. 调用 Skill(ai-assistant:coordinator-planning)
4. 调用 Skill(ai-assistant:coordinator-dispatch)
5. 检查文档是否生成
6. 返回结果给用户
```
