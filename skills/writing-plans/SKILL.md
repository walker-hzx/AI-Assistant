---
name: writing-plans
description: 当你有规格说明或多步骤任务的需求时，在接触代码之前使用此技能创建详细实施计划
---

# 编写实施计划

## 概述

编写全面的实现计划，假设工程师对你的代码库毫无了解。记录他们需要知道的一切：每个任务要接触哪些文件、代码、测试、如何测试。将整个计划作为小任务呈现。

**开始时声明：** "我正在使用 writing-plans skill 来创建实现计划。"

**保存计划到：** `docs/plans/YYYY-MM-DD-<feature-name>.md`

## 小任务粒度

**每个步骤是一个动作（2-5 分钟）：**
- "编写失败的测试" - 步骤
- "运行它以确认失败" - 步骤
- "编写使测试通过的最小代码" - 步骤
- "运行测试确保通过" - 步骤
- "提交" - 步骤

## 计划文档头部

**每个计划必须以此头部开头：**

```markdown
# [功能名称] 实现计划

> **For Claude:** 必需子技能：使用 executing-plans 逐个任务实现此计划。

**目标：** [一句话描述要构建什么]

**架构：** [2-3 句话描述方法]

**技术栈：** [关键技术/库]

---
```

## 任务结构

```markdown
### 任务 N：[组件名称]

**文件：**
- 创建：`exact/path/to/file.ts`
- 修改：`exact/path/to/existing.ts:123-145`
- 测试：`tests/exact/path/to/test.ts`

**步骤 1：编写失败的测试**

```typescript
function test_specific_behavior() {
  const result = function(input)
  expect(result).toBe(expected)
}
```

**步骤 2：运行测试验证失败**

运行：`npm test tests/path/test.ts`
预期：FAIL with "function not defined"

**步骤 3：编写最小实现**

```typescript
function function(input) {
  return expected
}
```

**步骤 4：运行测试验证通过**

运行：`npm test tests/path/test.ts`
预期：PASS

**步骤 5：提交**

```bash
git add tests/path/test.ts src/path/file.ts
git commit -m "feat: add specific feature"
```
```

## 记住

- 始终使用精确的文件路径
- 完整代码在计划中（不是"添加验证"）
- 精确命令带预期输出
- DRY, YAGNI, TDD, 频繁提交

## 执行交接

保存计划后，提供执行选择：

**"计划完成并保存到 `docs/plans/<filename>.md`。两个执行选项：**

**1. 子代理驱动（本会话）** - 每个任务分配新的子代理，任务间审查，快速迭代

**2. 并行会话（单独）** - 在新会话中打开 executing-plans，批量执行带检查点

**选择哪个方法？"**

**如果选择子代理驱动：**
- 使用 subagent-driven-development 技能
- 保持在本会话
- 每个任务 + 代码审查的新子代理

**如果选择并行会话：**
- 引导用户在 worktree 中打开新会话
- 新会话使用 executing-plans 技能

## 技术栈

- **前端**: Vue 3 + TypeScript + Vite + Vitest
- **后端**: Python + FastAPI + pytest
- **测试覆盖率**: 80%

## 工作流集成

1. **brainstorming** → 理解需求
2. **writing-plans** → 创建实施计划
3. **executing-plans** → 执行计划
4. **code-review** → 代码审查
5. **update-blueprint** → 更新蓝图
