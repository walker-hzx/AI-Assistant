# Coordinator 调度流程分析报告

> 分析日期：2026-02-27
> 分析范围：coordinator, coordinator-intent, coordinator-planning, coordinator-dispatch 及相关被调度技能

---

## 执行摘要

Coordinator 调度流程整体设计合理，采用"意图分析 → 方案规划 → 任务派发"的三阶段架构，通过文档驱动机制确保流程可追溯。主要优点包括：
- 流程完整性较好，每个阶段都有文档产出
- 强制使用 Skill 而非 Task，避免了上下文丢失
- 具备基本的异常处理机制（循环重试、检查点验证）

但也存在**职责边界不清晰、协作机制不完整、文档定义混乱**等问题，可能导致调度流程失控。

---

## 一、流程完整性分析

### 1.1 链路完整性

| 阶段 | 子技能 | 产出文档 | 状态 |
|------|--------|----------|------|
| 意图分析 | coordinator-intent | `docs/intent/xxx-intent.md` | ✅ 完整 |
| 方案规划 | coordinator-planning | `docs/plans/xxx-plan.md` | ✅ 完整 |
| 任务派发 | coordinator-dispatch | 多个文档 | ⚠️ 混乱 |

**整体链路完整**，但任务派发阶段包含过多内容（需求→计划→执行→验证→审查），导致职责模糊。

### 1.2 文档驱动机制

| 阶段 | 要求的文档 | 位置定义 | 一致性 |
|------|-----------|----------|--------|
| 调度记录 | coordinator.md | `docs/plans/` | - |
| 意图分析 | coordinator-intent.md | `docs/intent/` | ❌ 位置不一致 |
| 执行计划 | coordinator-planning.md | `docs/plans/` | ✅ |
| 执行日志 | coordinator-dispatch.md | `docs/plans/` | ✅ |
| 验证报告 | verification.md | `docs/verification/` | ✅ |
| 审查报告 | code-review.md | `docs/reviews/` | ✅ |

---

## 二、职责边界分析

### 2.1 各子技能职责

| 技能 | 声称职责 | 实际职责 | 边界清晰度 |
|------|----------|----------|------------|
| coordinator-intent | 意图分析 | 意图分析、任务分类、复杂度评估 | ✅ 清晰 |
| coordinator-planning | 方案规划 | 角色选择、阶段划分、里程碑设计 | ⚠️ 部分模糊 |
| coordinator-dispatch | 任务派发 | **全部执行流程**（需求→计划→执行→验证→审查） | ❌ 严重模糊 |

### 2.2 关键问题：coordinator-dispatch 职责越权

**问题描述**：
- `coordinator-dispatch/SKILL.md` 声称"只负责执行派发，不决定派发给谁"
- 但实际内容包含完整的执行流程（第171-201行）：
  ```
  【管家】调度 requirements-analyst（需求分析）
  【管家】调度 planner（制定计划）
  【管家】调度 executor（执行）
  【管家】调度 qa（验证功能）
  【管家】调度 code-reviewer（代码审查）
  ```

**影响**：
- coordinator-dispatch 实际上变成了"小 coordinator"，承担了过多职责
- 与 coordinator-planning 的"角色选择"职责重叠
- 违反了"管家是调度者，不是执行者"的核心原则

---

## 三、协作机制分析

### 3.1 角色调用方式

| 调用方 | 被调用方 | 调用方式 | 正确性 |
|--------|----------|----------|--------|
| coordinator | coordinator-intent | Skill | ✅ |
| coordinator | coordinator-planning | Skill | ✅ |
| coordinator | coordinator-dispatch | Skill | ✅ |
| coordinator-dispatch | brainstorming | Skill | ✅ 强制要求 |
| coordinator-dispatch | writing-plans | Skill | ✅ 强制要求 |
| coordinator-dispatch | executing-plans | Skill | ✅ |
| coordinator-dispatch | verification | Skill | ⚠️ 描述为"调度qa" |
| coordinator-dispatch | code-review | Skill | ⚠️ 描述为"调度code-reviewer" |

### 3.2 任务转交机制（设计 vs 实现）

**设计意图**（coordinator-dispatch 第51-83行）：
```
其他角色不能直接调用其他角色，只能向 Coordinator 报告
```

**实际执行情况**：
| 技能 | 实际行为 | 是否报告 Coordinator |
|------|----------|---------------------|
| brainstorming | 提示"下一步是 writing-plans" | ❌ |
| writing-plans | 提示"下一步是 executing-plans" | ❌ |
| executing-plans | 提示"请调用 /verification" | ❌ |
| verification | 提示"下一步是 code-review" | ❌ |

**问题**：虽然 coordinator-dispatch 定义了任务转交机制，但被调度的技能并未遵循，而是直接引导用户进入下一阶段。

### 3.3 "回不到 Coordinator"风险

**风险等级**：🔴 HIGH

**原因**：
1. Skill 调用虽然在同一个上下文，但被调用技能没有"回归 coordinator"的机制
2. 每个技能完成时都是提示用户"下一步是什么"，而不是回到 coordinator
3. 如果用户在中间阶段直接调用下一个技能，会绕过 coordinator 的检查点

---

## 四、异常处理分析

### 4.1 已有的机制

| 机制 | 位置 | 描述 |
|------|------|------|
| 执行循环 | coordinator-dispatch 第221-298行 | 验证失败后自动修复，最多3次 |
| 检查点验证 | coordinator 主技能 | 检查文档是否存在 |
| 阶段门禁 | coordinator 主技能 | 每个检查点必须验证通过 |
| 文档缺失处理 | coordinator 主技能 | 报错并停止流程 |

### 4.2 缺失的机制

| 机制 | 缺失影响 | 严重程度 |
|------|---------|----------|
| 循环中需求变更处理 | 可能继续实现过时需求 | 🔴 HIGH |
| 验证失败后计划调整 | 可能盲目重试 | 🟡 MEDIUM |
| 子技能超时处理 | 可能卡在某个阶段 | 🟡 MEDIUM |
| 用户中断处理 | 中断后无法恢复 | 🟡 MEDIUM |

---

## 五、发现的问题汇总

### 问题 1：文档位置定义不一致

- **位置**：
  - `coordinator/SKILL.md` 第65行
  - `coordinator-intent/SKILL.md` 第269行
  - `coordinator-dispatch/SKILL.md` 第310行
- **问题描述**：同一份"调度记录"文档，三个文件定义的保存位置不同
- **影响**：开发者可能困惑，不知道应该保存在哪里
- **建议修复**：统一文档位置定义，建议都在 `docs/plans/` 下

---

### 问题 2：coordinator-dispatch 职责越权

- **位置**：`coordinator-dispatch/SKILL.md` 第87-201行
- **问题描述**：
  - 声称"只负责执行派发"
  - 实际包含了完整的执行流程（需求分析→计划制定→执行→验证→审查）
  - 与 coordinator-planning 的"角色选择"职责重叠
- **影响**：
  - 违反了"管家是调度者，不是执行者"原则
  - coordinator-dispatch 变成了"小 coordinator"
  - 职责边界模糊导致流程失控风险
- **建议修复**：
  - 明确 coordinator-dispatch **只负责按计划调度角色执行**
  - 将"决定调度谁"的职责完全剥离给 coordinator-planning
  - 简化 coordinator-dispatch 为纯调度器

---

### 问题 3：任务转交机制名存实亡

- **位置**：
  - `coordinator-dispatch/SKILL.md` 第51-83行（设计）
  - `brainstorming/SKILL.md` 第170行（实现）
  - `writing-plans/SKILL.md` 第300行（实现）
- **问题描述**：
  - coordinator-dispatch 设计了"任务转交机制"，要求其他角色向 Coordinator 报告
  - 但实际被调度的技能（brainstorming, writing-plans 等）都是直接提示用户"下一步是 xxx"
  - 没有"回归 coordinator"的机制
- **影响**：
  - 🔴 **可能导致流程失控**：用户可以直接跳过 coordinator 调用后续技能
  - 检查点机制失效
- **建议修复**：
  - 所有被调度技能完成时，必须提示"回到 coordinator"或"等待 coordinator 调度"
  - 或者在 coordinator-dispatch 中明确：被调度技能完成后**自动回归 coordinator**，不依赖用户手动操作

---

### 问题 4：验证阶段调度方式不明确

- **位置**：
  - `coordinator-dispatch/SKILL.md` 第192行：调度 qa
  - `executing-plans/SKILL.md` 第275行：告知用户调用 /verification
- **问题描述**：
  - coordinator-dispatch 说"调度 qa（验证功能）"
  - executing-plans 说"请调用 /verification"
  - verification 是一个独立的 Skill，需要用户手动调用
- **影响**：
  - 自动化流程中断
  - 可能出现用户忘记调用 verification 的情况
- **建议修复**：
  - 统一调度方式：由 coordinator-dispatch **自动调度** verification Skill
  - 删除 executing-plans 中"告知用户调用 verification"的描述

---

### 问题 5：检查点机制仅在主技能定义

- **位置**：`coordinator/SKILL.md` 第88-124行
- **问题描述**：
  - 检查点验证只在 coordinator 主技能中定义
  - 子技能（coordinator-intent, coordinator-planning, coordinator-dispatch）没有检查点概念
  - 如果直接调用子技能，可以绕过检查点
- **影响**：
  - 🔴 **安全隐患**：可以绕过检查点直接执行
- **建议修复**：
  - 在每个子技能中添加"前置检查点验证"逻辑
  - 或者确保只能通过 coordinator 主技能调用子技能

---

### 问题 6：执行循环中的需求变更风险

- **位置**：`coordinator-dispatch/SKILL.md` 第221-298行
- **问题描述**：
  - 执行循环（最多3次）会在验证失败后自动尝试修复
  - 但不检查需求是否变更、计划是否需要调整
  - 可能盲目重试过时的方案
- **影响**：
  - 浪费资源做无用功
  - 可能引入新的问题
- **建议修复**：
  - 每次循环前检查：需求文档是否有变更
  - 如果需求变更，提示用户重新规划
  - 循环2次后强制提示人工介入

---

### 问题 7：文档模板重复定义

- **位置**：
  - `coordinator-planning/SKILL.md` 第284-367行
  - `coordinator-dispatch/SKILL.md` 第315-347行
- **问题描述**：两个文件都定义了"管家调度记录"模板，内容几乎相同
- **影响**：维护困难，可能导致版本不一致
- **建议修复**：将模板统一到一个地方，用引用方式使用

---

### 问题 8：验证与审查之间的衔接

- **位置**：
  - `coordinator-dispatch/SKILL.md` 第171-201行（流程图中包含 verification 和 code-review）
  - `verification/SKILL.md` 第107行（下一步是 code-review）
- **问题描述**：
  - coordinator-dispatch 的流程图包含验证和审查
  - 但 coordinator 主技能的检查点3只检查"验证报告"和"审查报告"，没有明确谁调度谁
- **影响**：流程不清晰，可能导致重复调度或遗漏
- **建议修复**：明确 coordinator-dispatch 负责按顺序调度 verification 和 code-review

---

## 六、风险评估

| 问题 | 风险等级 | 影响范围 | 建议 |
|------|----------|----------|------|
| 职责越权 | 🔴 HIGH | 整个流程 | 紧急修复 |
| 任务转交机制失效 | 🔴 HIGH | 流程失控 | 紧急修复 |
| 检查点可绕过 | 🔴 HIGH | 安全 | 紧急修复 |
| 验证调度不明确 | 🟡 MEDIUM | 自动化 | 重要修复 |
| 文档位置不一致 | 🟢 LOW | 开发体验 | 建议修复 |
| 模板重复定义 | 🟢 LOW | 维护性 | 建议修复 |

---

## 七、建议方案

### 方案 A：精简 coordinator-dispatch（推荐）

**思路**：将 coordinator-dispatch 职责精简为纯调度器

| 职责 | 处理方式 |
|------|----------|
| 决定调度谁 | 保留给 coordinator-planning |
| 按顺序调度执行 | 移交给 coordinator-dispatch |
| 验证功能 | 由 coordinator-dispatch 自动调度 verification |
| 代码审查 | 由 coordinator-dispatch 自动调度 code-review |
| 循环重试 | 保留在 coordinator-dispatch |

**优点**：
- 职责边界清晰
- 符合"管家是调度者"原则
- 自动化程度高

**缺点**：
- 需要修改较多文件

---

### 方案 B：强化任务转交机制

**思路**：确保每个被调度技能完成后都回归 coordinator

| 修改点 | 内容 |
|--------|------|
| 被调度技能 | 移除"下一步是 xxx"的提示 |
| 被调度技能 | 改为"执行完成，等待 coordinator 调度" |
| coordinator-dispatch | Skill 调用完成后自动继续执行 |

**优点**：
- 保持现有职责划分
- 确保流程可控

**缺点**：
- 需要修改所有被调度技能
- 可能影响用户体验（增加交互次数）

---

## 八、总结

### 整体评价

| 维度 | 评分 | 说明 |
|------|------|------|
| 流程完整性 | 7/10 | 基本完整，但验证阶段调度不明确 |
| 职责清晰度 | 5/10 | 存在严重职责越权 |
| 协作机制 | 4/10 | 任务转交机制基本失效 |
| 异常处理 | 6/10 | 有基本机制，但不够完善 |
| 文档一致性 | 5/10 | 位置定义混乱 |

### 优先修复项

1. 🔴 **紧急**：修复任务转交机制，确保流程可控
2. 🔴 **紧急**：明确 coordinator-dispatch 职责边界
3. 🔴 **紧急**：加强检查点机制，防止绕过
4. 🟡 **重要**：统一文档位置定义
5. 🟡 **重要**：明确验证阶段调度方式

---

*报告结束*
