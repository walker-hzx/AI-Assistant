---
name: workflow-check
description: 检查项目开发流程是否正确使用 AI-Assistant 配置
disable-model-invocation: true
---

# 流程检查

检查当前项目的开发流程是否正确使用 AI-Assistant 配置。

## 使用方式

```
/workflow-check
```

或者直接说"检查流程"、"检查配置使用"

## 功能

1. **检查使用的技能是否正确** - 在当前场景下使用的技能是否合适
2. **检查流程顺序** - 是否按正确顺序执行（需求 → 设计 → 计划 → 执行 → 验证）
3. **检查遗漏** - 是否有该做的步骤被跳过了
4. **检查关联** - 需求、计划、实现的关联是否完整

## 检查流程

### 1. 检查需求文档

- 是否有需求文档（`docs/requirements/`）
- 需求是否与计划关联

### 2. 检查计划文档

- 是否有实施计划（`docs/plans/`）
- 计划是否与需求关联

### 3. 检查代码实现

- 是否遵循计划
- 是否有验证步骤

### 4. 检查流程顺序

检查是否按正确顺序：
1. discuss-requirements（需求不明确时）
2. brainstorming（需求明确后）
3. writing-plans（创建计划）
4. executing-plans（执行计划）
5. verification-before-completion（代码验证）
6. execution-validation（需求验证）
7. update-blueprint（更新蓝图）

## 输出格式

```markdown
## 流程检查报告

### 整体评估
[流程完整度：X%]

### 发现的问题
1. [问题描述]
2. [问题描述]

### 遗漏的步骤
- [遗漏的步骤]

### 建议
- [改进建议]

### 流程图
需求文档 → 计划文档 → 代码实现 → 验证
```

## 检查原则

- 指出问题，但不强制要求修改
- 提供改进建议
- 尊重用户的选择
