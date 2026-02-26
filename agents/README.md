# 角色体系（Subagents）

> 定义 18 个角色子智能体，每个角色负责特定职责

## 核心角色（线性流程）

| 角色 | 职责 | Skill |
|------|------|-------|
| requirements-analyst | 理解用户真正想要什么 | requirement-understanding, requirement-analysis |
| planner | 把需求变成可执行计划 | task-splitting, dependency-analysis |
| executor | 按计划实现代码 | code-implementation, tdd |
| qa | 验证实现是否符合需求 | verification, security-verification |
| code-reviewer | 确保代码质量 | code-review |

## 辅助角色（按需调用）

| 角色 | 职责 | Skill |
|------|------|-------|
| coordinator | 智能调度，判断用什么角色 | coordinator-intent, coordinator-planning, coordinator-dispatch |
| thinking-coach | 思维方式指导 | thinking-coach |
| strategist | 深度分析、决策支持 | strategist |
| debugger | Bug 定位修复 | debugging |
| code-analyst | 代码问题系统分析 | code-analysis |
| security-reviewer | 安全问题审查 | security-review |
| test-designer | 测试用例设计 | test-planner |
| architect | 技术选型、架构设计 | architect |
| database-expert | 数据库设计优化 | database-expert |
| performance-expert | 性能分析优化 | performance-expert |
| refactoring-expert | 代码重构 | refactoring-expert |
| project-researcher | 项目调研 | project-researcher |
| web-researcher | 网页研究 | web-researcher |
| e2e-tester | E2E 测试执行 | e2e-testing |

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

### 2. 直接调用

可以直接调用某个角色：

```
Use the requirements-analyst to clarify what the user wants
Use the planner to create an implementation plan
Use the executor to implement the code
```

## 文件结构

```
agents/
├── coordinator.md          # 智能调度（管家）
├── requirements-analyst.md  # 需求分析师
├── planner.md            # 计划制定者
├── executor.md           # 执行者
├── qa.md                 # 质量保证
├── code-reviewer.md      # 代码审查
├── thinking-coach.md     # 思维教练
├── strategist.md         # 策略分析师
├── debugger.md           # 调试专家
├── code-analyst.md       # 代码分析师
├── security-reviewer.md  # 安全审查
├── test-designer.md     # 测试设计
├── architect.md         # 架构师
├── database-expert.md    # 数据库专家
├── performance-expert.md # 性能专家
├── refactoring-expert.md # 重构专家
├── project-researcher.md # 项目调研
├── web-researcher.md    # 网页研究
└── e2e-tester.md        # E2E 测试
```

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

在任何阶段，如果遇到以下情况，可以调用辅助角色：

| 情况 | 调用角色 | 使用 Skill |
|------|---------|-----------|
| 思维困惑 | thinking-coach | thinking-coach |
| 代码 bug | debugger | debugging |
| 代码分析 | code-analyst | code-analysis |
| 安全问题 | security-reviewer | security-review |
| 测试设计 | test-designer | test-planner |
