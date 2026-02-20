# 需求实时记录功能实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 在需求讨论过程中，实时记录确认的需求点到文档，确保长沟通过程不遗漏

**Architecture:** 通过修改 Skills 的工作流程，在讨论过程中自动创建和更新需求文档

**Tech Stack:** Claude Code Skills (Markdown), 文件系统操作

---

## Task 1: 创建需求文档模板

**Files:**
- Create: `docs/requirements/模板.md`

**Step 1: 创建需求文档模板**

```markdown
# 需求讨论：<主题>

> 创建时间：{timestamp}

## 确认的需求点

### {time} - 第 {n} 轮
-

## 待确认
- [ ]

## 讨论进度
- 当前阶段：
- 上次讨论位置：
```

**Step 2: 提交**

```bash
git add docs/requirements/模板.md
git commit -m "docs: 添加需求文档模板"
```

---

## Task 2: 修改 discuss-requirements skill - 添加文档创建逻辑

**Files:**
- Modify: `skills/discuss-requirements/SKILL.md`

**Step 1: 在 SKILL.md 开头添加文档创建逻辑**

在 `## 使用场景` 之前添加：

```markdown
## 文档管理

### 创建需求文档

当用户开始新的需求讨论时：

1. 解析讨论主题（用户输入或默认"未命名需求"）
2. 创建文档 `docs/requirements/YYYY-MM-DD-<主题>-需求.md`
3. 写入初始模板内容

### 实时记录

在讨论过程中：

1. 每当用户确认一个需求点 → 追加到"确认的需求点"
2. 每当产生一个待确认问题 → 追加到"待确认"
3. 记录当前讨论阶段到"讨论进度"

### 查看需求

当用户说"查看需求"时：
1. 读取当前需求文档
2. 展示给用户
```

**Step 2: 修改 Step 4 为自动记录**

将原来的手动记录改为：

```markdown
### Step 4: 记录需求

当需求讨论到一定程度后：

1. 读取当前需求文档
2. 将确认的需求点追加到"确认的需求点"部分
3. 将待确认问题追加到"待确认"部分
4. 更新"讨论进度"
```

**Step 3: 提交**

```bash
git add skills/discuss-requirements/SKILL.md
git commit -m "feat: discuss-requirements 添加实时记录功能"
```

---

## Task 3: 修改 describe-interaction skill - 集成记录功能

**Files:**
- Modify: `skills/describe-interaction/SKILL.md`

**Step 1: 在 SKILL.md 开头添加文档管理说明**

```markdown
## 文档管理

继续使用 discuss-requirements 创建的需求文档。

### 追加记录

1. 读取当前需求文档
2. 追加交互细节到"确认的需求点"
3. 更新"讨论进度"为"交互设计"
```

**Step 2: 在工作流程中添加记录点**

在关键步骤后添加"记录到文档"的提示

**Step 3: 提交**

```bash
git add skills/describe-interaction/SKILL.md
git commit -m "feat: describe-interaction 集成需求记录功能"
```

---

## Task 4: 添加"查看需求"命令

**Files:**
- Modify: `commands/view-requirements.md`

**Step 1: 创建命令文件**

```markdown
---
name: view-requirements
description: 查看当前需求讨论记录
---

# 查看需求

查看当前正在进行的需求讨论记录。

## 使用方式

```
/view-requirements
```

或者直接说"查看需求"

## 功能

1. 查找当前最新的需求文档
2. 读取并展示给用户
3. 如果有多个未完成的需求，展示列表让用户选择
```

**Step 2: 提交**

```bash
git add commands/view-requirements.md
git commit -m "feat: 添加查看需求命令"
```

---

## Task 5: 修改 writing-plans skill - 追加计划到需求文档

**Files:**
- Modify: `skills/writing-plans/SKILL.md`

**Step 1: 添加文档追加逻辑**

在创建计划后：

```markdown
## 关联需求文档

创建实施计划后：

1. 查找当前相关的需求文档（根据主题）
2. 在文档末尾追加：
   - 实施计划概要
   - 计划文件链接
3. 更新"讨论进度"为"已完成"
```

**Step 2: 提交**

```bash
git add skills/writing-plans/SKILL.md
git commit -m "feat: writing-plans 追加计划到需求文档"
```

---

## Task 6: 新会话恢复逻辑

**Files:**
- Modify: `hooks/session-start.sh`

**Step 1: 修改 session-start hook**

在会话开始时：

1. 扫描 `docs/requirements/` 目录
2. 查找"未完成"状态的需求文档
3. 如果有，询问用户是否继续

**Step 2: 提交**

```bash
git add hooks/session-start.sh
git commit -m "feat: 添加新会话需求恢复逻辑"
```

---

## 执行方式

**Plan complete and saved to `docs/plans/2026-02-20-requirements-recording-implementation.md`. Two execution options:**

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

**Which approach?**
