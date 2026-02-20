# 计划和执行优化方案

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 优化计划和执行工作流，增加迭代调整机制和需求-实现对照验收

**Architecture:** 在现有流程中嵌入迭代式计划和需求验收环节

**Tech Stack:** 修改 SKILL.md 文件

---

## 背景分析

### 当前流程

```
brainstorming → writing-plans → executing-plans → verification-before-completion
     需求明确        创建计划         执行计划          代码质量验证
```

### 用户核心需求

1. **迭代式计划**：从大计划到细化，不断调整
2. **需求-实现对照验收**：代码完成后与原始需求对比

---

## 方案对比

### 方案 A：扩展现有 skill

| 方案 | 优点 | 缺点 |
|------|------|------|
| 扩展 writing-plans | 改动小 | 功能混杂 |
| 扩展 verification-before-completion | 复用现有 | 职责不清晰 |

### 方案 B：创建新 skill（推荐）

| 方案 | 优点 | 缺点 |
|------|------|------|
| 创建 execution-validation skill | 职责清晰，专门做需求对照 | 需要新文件 |

### 方案 C：混合方案（推荐）

| 改进点 | 方式 | 说明 |
|--------|------|------|
| writing-plans | 增加迭代机制 | 计划可以分阶段细化 |
| 创建 execution-validation | 新 skill | 专门做需求-实现对照 |
| executing-plans | 增加调整机制 | 执行中可以调整计划 |

---

## 推荐方案：方案 C

### 改进 1：writing-plans 增加迭代计划机制

**修改文件：** `skills/writing-plans/SKILL.md`

增加：
- 计划分层：阶段计划 → 里程碑 → 任务
- 每个里程碑后可以评审和调整
- 计划应该是活的，可以细化

### 改进 2：创建 execution-validation skill

**创建文件：** `skills/execution-validation/SKILL.md`

职责：
- 读取原始需求（design doc 或 brainstorming 结果）
- 对照检查每个需求的实现状态
- 明确标注：已完成 / 部分完成 / 未实现

### 改进 3：executing-plans 增加调整机制

**修改文件：** `skills/executing-plans/SKILL.md`

增加：
- 每个里程碑后可以暂停、评审、调整
- 计划调整后需要重新确认

---

## 任务总览

| 任务 | 描述 | 优先级 |
|------|------|--------|
| 1 | 修改 writing-plans 增加迭代计划机制 | P0 |
| 2 | 创建 execution-validation skill | P0 |
| 3 | 修改 executing-plans 增加调整机制 | P1 |
| 4 | 更新工作流文档 | P2 |

---

## Task 1: 修改 writing-plans 增加迭代计划机制

**Files:**
- Modify: `skills/writing-plans/SKILL.md`

**增加内容：**

1. **计划分层结构：**
```markdown
## 迭代式计划结构

### 第一阶段：高层计划
- 目标：明确要做什么
- 粗略步骤：3-5 个主要阶段
- 不需要细节

### 第二阶段：里程碑细化
- 每个里程碑独立成计划
- 可以逐个细化

### 第三阶段：任务细化
- 每个任务 = 1 个独立步骤
- 最细粒度：2-5 分钟可完成
```

2. **计划调整机制：**
```markdown
## 计划调整

每个里程碑完成后：
1. 对照原始需求检查
2. 如有需要，调整后续计划
3. 与用户确认后再继续
```

---

## Task 2: 创建 execution-validation skill

**Files:**
- Create: `skills/execution-validation/SKILL.md`

**内容结构：**

```markdown
---
name: execution-validation
description: 需求-实现对照验收 - 代码完成后对照原始需求验证实现完整性
---

# 需求-实现对照验收

## 概述

在代码完成后，对照原始需求验证实现完整性。

**核心原则：** 需求即契约，实现必须满足契约。

## 工作流程

### 1. 读取原始需求

- 查找 design doc: `docs/plans/*-design.md`
- 查找 brainstorming 结果
- 提取验收标准

### 2. 逐项对照检查

| 需求项 | 实现状态 | 说明 |
|--------|----------|------|
| 功能 A | ✅ 已实现 | 位置：xxx |
| 功能 B | ⚠️ 部分实现 | xxx |
| 功能 C | ❌ 未实现 | 原因：xxx |

### 3. 输出验收报告

```markdown
## 验收报告

### 已完成
- [ ] 需求 1

### 部分完成
- [ ] 需求 2 (原因)

### 未完成
- [ ] 需求 3 (原因)

### 结论
[是否可以验收 / 需要补充什么]
```

## 验收标准

- 每个原始需求都有明确状态
- 未完成项有合理解释
- 用户确认后才能标记为完成
```

---

## Task 3: 修改 executing-plans 增加调整机制

**Files:**
- Modify: `skills/executing-plans/SKILL.md`

**增加内容：**

```markdown
## 计划调整机制

### 里程碑评审点

每个里程碑完成后：
1. 暂停执行
2. 对照原始需求检查进度
3. 如需调整计划，与用户确认
4. 继续执行或调整

### 调整触发条件

- 发现计划遗漏的步骤
- 需求有变化
- 发现新的依赖或风险
```

---

## Task 4: 更新工作流文档

**Files:**
- Modify: `docs/plans/2026-02-20-<previous-plan>.md` 或新建

**内容：**
- 更新后的完整工作流
- 说明新的 execution-validation 环节

---

## 实施顺序

1. Task 1: 修改 writing-plans
2. Task 2: 创建 execution-validation
3. Task 3: 修改 executing-plans
4. Task 4: 更新文档

---

## 优化后的工作流

```
brainstorming → writing-plans (迭代细化) → executing-plans (可调整)
                                                    ↓
                              verification-before-completion (代码质量)
                                                    ↓
                              execution-validation (需求对照) ← 关键新增
                                                    ↓
                                           update-blueprint
```

---

## Plan complete and saved to `docs/plans/2026-02-20-plan-execution-optimization.md`

Two execution options:

1. **Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

2. **Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

Which approach?
