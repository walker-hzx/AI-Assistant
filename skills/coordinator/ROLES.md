# Subagent 角色定义

> 本文档定义 Coordinator 可调度的 Subagent 角色

---

## 角色列表

### 分析类

| 角色 | 用途 | Skill 调用 | 典型场景 |
|------|------|-----------|---------|
| thinking-coach | 思维教练 - 厘清思路，给出方向 | `ai-assistant:thinking-coach` | 需求不清晰、方向不明 |
| strategist | 策略分析师 - 深度分析，评估方案 | `ai-assistant:strategist` | 多个方案需要选择 |
| code-analysis | 代码分析 - 系统分析代码问题 | `ai-assistant:code-analysis` | 代码有问题需要分析 |
| project-researcher | 项目调研 - 调研项目现状 | `ai-assistant:project-researcher` | 需要了解项目现状 |
| web-researcher | 网页研究 - 爬取和研究网页 | `ai-assistant:web-researcher` | 需要查资料/文档 |

### 需求类

| 角色 | 用途 | Skill 调用 | 典型场景 |
|------|------|-----------|---------|
| requirement-analysis | 需求分析 - 多角度分析需求完整性 | `ai-assistant:requirement-analysis` | 需求需要详细分析 |
| requirement-validation | 需求验证 - 确认需求完整可执行 | `ai-assistant:requirement-validation` | 需求需要验证 |

### 计划类

| 角色 | 用途 | Skill 调用 | 典型场景 |
|------|------|-----------|---------|
| milestone-planning | 里程碑划分 - 定义阶段性检查点 | `ai-assistant:milestone-planning` | 需要划分里程碑 |
| task-splitting | 任务拆分 - 拆分为 2-5 分钟小任务 | `ai-assistant:task-splitting` | 任务需要拆分 |
| dependency-analysis | 依赖分析 - 识别并行/串行关系 | `ai-assistant:dependency-analysis` | 需要分析依赖 |

### 实现类

| 角色 | 用途 | Skill 调用 | 典型场景 |
|------|------|-----------|---------|
| code-implementation | 代码实现 - 按计划编写代码 | `ai-assistant:code-implementation` | 需要编写代码 |

### 验证类

| 角色 | 用途 | Skill 调用 | 典型场景 |
|------|------|-----------|---------|
| e2e-tester | E2E 测试 - 端到端测试 | `ai-assistant:e2e-tester` | 需要 E2E 测试 |
| test-planner | 测试设计 - 设计测试用例 | `ai-assistant:test-planner` | 需要设计测试用例 |

### 审查类

| 角色 | 用途 | Skill 调用 | 典型场景 |
|------|------|-----------|---------|
| security-review | 安全审查 - 检查安全漏洞 | `ai-assistant:security-review` | 需要安全审查 |

### 调试类

| 角色 | 用途 | Skill 调用 | 典型场景 |
|------|------|-----------|---------|
| debugging | 调试专家 - 定位和修复 bug | `ai-assistant:debugging` | 需要调试 bug |
| browser-debugger | 浏览器调试 - 捕获前端错误 | `ai-assistant:browser-debugger` | 前端需要调试 |

### 辅助类

| 角色 | 用途 | Skill 调用 | 典型场景 |
|------|------|-----------|---------|
| team-generator | 团队生成 - 创建多角色协作团队 | `ai-assistant:team-generator` | 需要并行任务 |

---

## 按阶段调用指南

| 阶段 | 可能调用的 Subagent |
|------|---------------------|
| 需求分析 | thinking-coach, requirement-analysis, requirement-validation, web-researcher, project-researcher |
| 任务规划 | milestone-planning, task-splitting, dependency-analysis, strategist |
| 代码执行 | code-implementation, web-researcher |
| 测试验证 | test-planner, e2e-tester |
| 安全审查 | security-review |
| 问题调试 | debugging, browser-debugger, code-analysis |
| 复杂决策 | strategist, team-generator |

---

## 调用规则

### 必须使用 Skill 工具

```
Skill: ai-assistant:<角色名>
```

### 调用格式

```
【调度角色】
Skill: ai-assistant:<角色名>

【等待完成】
- 等待 Skill 执行完成
- 收集输出
- 检查执行结果
```
