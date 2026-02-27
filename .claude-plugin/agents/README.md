# 角色体系（Subagents）

> 定义 11 个角色子智能体，每个角色映射到一个 Skill

## 核心角色（线性流程）

| 角色 | 职责 | Skill |
|------|------|-------|
| requirements-analyst | 理解用户真正想要什么 | brainstorming |
| planner | 把需求变成可执行计划 | writing-plans |
| executor | 按计划实现代码 | executing-plans |
| qa | 验证实现是否符合需求 | verification |
| code-reviewer | 确保代码质量 | code-review |

## 辅助角色（按需调用）

| 角色 | 职责 | Skill |
|------|------|-------|
| thinking-coach | 思维方式指导 | thinking-coach |
| debugger | Bug 定位修复 | debugging |
| code-analysis | 代码问题分析 | code-analysis |
| security-reviewer | 安全问题审查 | security-review |
| test-designer | 测试用例设计 | test-planner |

## 管家说明

> **Coordinator 现在是 Skill，不是 Agent**
>
> 管家通过 Skill 调用：`skill: coordinator`
> - 完整流程：意图分析 → 方案规划 → 执行调度 → 结果收集
> - 所有命令都使用 `skill: coordinator` 调用

## 使用方式

### 1. 管家调度

当用户提出任务时，Coordinator 根据任务类型选择合适的角色：

```
用户：帮我做一个用户登录功能
    ↓
Coordinator 分析：
- 需求不清晰 → 需要 requirements-analyst
- 有需求后 → 需要 planner
- 有计划后 → 需要 executor
    ↓
按顺序调度角色执行
```

### 2. 管家调度

所有任务都应通过 Coordinator 调度，由 Coordinator 判断需要哪些角色。

```
用户：帮我做一个用户登录功能
    ↓
Coordinator 分析任务类型
    ↓
Coordinator 调度合适的角色执行
```

### 3. 直接调用（仅用于测试）

仅在明确知道需要哪个角色时使用，复杂任务仍应通过 Coordinator。

```
# 不推荐 - 复杂任务
Use the requirements-analyst to clarify what the user wants

# 推荐 - 通过 Coordinator
./assistant 一句话需求
```

## 文件结构

```
.claude/agents/
├── requirements-analyst.md  # 需求分析师
├── planner.md              # 计划制定者
├── executor.md             # 执行者
├── qa.md                   # 质量保证
├── code-reviewer.md        # 代码审查
├── thinking-coach.md       # 思维教练
├── debugger.md             # 调试专家
├── code-analysis.md         # 代码分析师
├── security-reviewer.md    # 安全审查
└── test-designer.md        # 测试设计
```

> 注意：Coordinator 是 Skill（skills/coordinator），不是 Agent

## Subagent 配置说明

每个 Subagent 文件使用 YAML frontmatter 定义配置：

```yaml
---
name: requirements-analyst      # 唯一标识符
description: "需求分析师 - ..."  # 描述何时调用
model: inherit                 # 使用继承的模型
skills:                        # 预加载的 skills
- brainstorming
---

# 系统 prompt
...
```

## 线性工作流

```
用户任务
    ↓
[coordinator] 判断类型
    ↓
[requirements-analyst] 需求分析 (brainstorming)
    ↓
[planner] 制定计划 (writing-plans)
    ↓
[executor] 实现代码 (executing-plans)
    ↓
[qa] 验证功能 (verification)
    ↓
[code-reviewer] 代码审查 (code-review)
    ↓
完成
```

## 辅助调用

> **重要**：所有角色都不能直接调用其他角色，只能向 Coordinator 报告，由 Coordinator 决定是否调度。

**遇到以下情况时，应向 Coordinator 报告**：

| 情况 | 报告内容 |
|------|---------|
| 思维困惑 | 发现需要 thinking-coach 协助分析思维方式 |
| 代码 bug | 发现需要 debugger 协助定位修复 |
| 代码分析 | 发现需要 code-analysis 协助系统分析 |
| 安全问题 | 发现需要 security-reviewer 协助安全审查 |
| 测试设计 | 发现需要 test-designer 协助测试用例设计 |

**报告格式**：
```
【需要 [角色名] 协助】

【原因】：
[描述为什么需要该角色]

【问题描述】：
[具体问题]

【等待 Coordinator 决策】
```
