# Subagent 角色定义

> 本文档定义 Coordinator 可调度的 Subagent 角色（基于 Agent 定义）

---

## 角色列表

### 分析类

| 角色 | 用途 | Agent | Skill 调用 | 典型场景 |
|------|------|-------|-----------|---------|
| thinking-coach | 思维教练 - 厘清思路，给出方向 | thinking-coach | `ai-assistant:thinking-coach` | 需求不清晰、方向不明 |
| strategist | 策略分析师 - 深度分析，评估方案 | strategist | `ai-assistant:strategist` | 多个方案需要选择 |
| code-analysis | 代码分析 - 系统分析代码问题 | code-analysis | `ai-assistant:code-analysis` | 代码有问题需要分析 |
| project-researcher | 项目调研 - 调研项目现状 | project-researcher | `ai-assistant:project-researcher` | 需要了解项目现状 |
| web-researcher | 网页研究 - 爬取和研究网页 | web-researcher | `ai-assistant:web-researcher` | 需要查资料/文档 |

### 需求类

| 角色 | 用途 | Agent | Skill 调用 | 典型场景 |
|------|------|-------|-----------|---------|
| requirement-analysis | 需求分析 - 多角度分析需求完整性 | requirements-analyst | `ai-assistant:requirement-analysis` | 需求需要详细分析 |

### 实现类

| 角色 | 用途 | Agent | Skill 调用 | 典型场景 |
|------|------|-------|-----------|---------|
| code-implementation | 代码实现 - 按计划编写代码 | executor | `ai-assistant:code-implementation` | 需要编写代码 |

### 验证类

| 角色 | 用途 | Agent | Skill 调用 | 典型场景 |
|------|------|-------|-----------|---------|
| e2e-tester | E2E 测试 - 端到端测试 | e2e-tester | `ai-assistant:e2e-tester` | 需要 E2E 测试 |
| test-planner | 测试设计 - 设计测试用例 | test-designer | `ai-assistant:test-planner` | 需要设计测试用例 |
| unit-tester | 单元测试 - 编写单元测试 | qa | `ai-assistant:unit-tester` | 需要单元测试 |

### 审查类

| 角色 | 用途 | Agent | Skill 调用 | 典型场景 |
|------|------|-------|-----------|---------|
| security-review | 安全审查 - 检查安全漏洞 | security-reviewer | `ai-assistant:security-review` | 需要安全审查 |
| code-review | 代码审查 - 验证代码质量 | code-reviewer | `ai-assistant:code-review` | 需要代码审查 |

### 调试类

| 角色 | 用途 | Agent | Skill 调用 | 典型场景 |
|------|------|-------|-----------|---------|
| debugging | 调试专家 - 定位和修复 bug | debugger | `ai-assistant:debugging` | 需要调试 bug |
| browser-debugger | 浏览器调试 - 捕获前端错误 | browser-debugger | `ai-assistant:browser-debugger` | 前端需要调试 |

### 辅助类

| 角色 | 用途 | Agent | Skill 调用 | 典型场景 |
|------|------|-------|-----------|---------|
| team-generator | 团队生成 - 创建多角色协作团队 | - | `ai-assistant:team-generator` | 需要并行任务 |

---

## 按阶段调用指南

| 阶段 | 可能调用的 Subagent |
|------|---------------------|
| 需求分析 | thinking-coach, requirement-analysis, web-researcher, project-researcher |
| 任务规划 | milestone-planning, task-splitting, dependency-analysis, strategist |
| 代码执行 | code-implementation, web-researcher |
| 测试验证 | test-planner, e2e-tester, unit-tester |
| 安全审查 | security-review |
| 代码审查 | code-review |
| 问题调试 | debugging, browser-debugger, code-analysis |
| 复杂决策 | strategist, team-generator |

---

## 调用规则

### 必须使用 Task 工具

根据 Claude Code 文档，调用 Subagent 使用 Task 工具：

```
Task(<角色名>, prompt="<任务描述>")
```

### 调用格式

```
【调度角色】
Task(<角色名>, prompt="""<任务描述>""")

【等待完成】
- 等待 Task 执行完成
- 收集输出
- 检查执行结果
```

### 角色与 Agent 对照

| 角色名 | Agent 文件 | 可用工具 |
|--------|-----------|---------|
| thinking-coach | thinking-coach.md | Task, Read |
| strategist | strategist.md | Task, Read, WebSearch |
| code-analysis | code-analysis.md | Task, Read, Glob, Grep |
| project-researcher | project-researcher.md | Task, Read, Glob, Grep |
| web-researcher | web-researcher.md | Task, WebFetch, WebSearch |
| requirement-analysis | requirements-analyst.md | Task, Read, Glob, Grep |
| executor | executor.md | Task, Read, Write, Glob, Grep |
| e2e-tester | e2e-tester.md | Task, Read, Bash |
| test-designer | test-designer.md | Task, Read, Glob, Grep |
| qa | qa.md | Task, Read, Bash |
| security-reviewer | security-reviewer.md | Task, Read, Glob, Grep |
| code-reviewer | code-reviewer.md | Task, Read, Glob, Grep |
| debugger | debugger.md | Task, Read, Bash |
| browser-debugger | browser-debugger.md | Task, Read, Bash |
