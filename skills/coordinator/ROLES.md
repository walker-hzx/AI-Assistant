# 角色定义

> 本文档定义管家可调度的所有角色及其能力

---

## 角色列表

### 需求类

| 角色 | 用途 | Skill 调用 |
|------|------|-----------|
| brainstorming | 需求讨论 - 快速澄清需求，明确做什么 | `ai-assistant:brainstorming` |
| requirement-analysis | 需求分析 - 多角度分析需求完整性和可实现性 | `ai-assistant:requirement-analysis` |
| requirement-validation | 需求验证 - 确认需求完整、清晰、可执行 | `ai-assistant:requirement-validation` |

### 计划类

| 角色 | 用途 | Skill 调用 |
|------|------|-----------|
| writing-plans | 制定计划 - 将需求拆分为可执行的任务 | `ai-assistant:writing-plans` |
| milestone-planning | 里程碑划分 - 定义阶段性检查点 | `ai-assistant:milestone-planning` |
| task-splitting | 任务拆分 - 拆分为 2-5 分钟的小任务 | `ai-assistant:task-splitting` |
| dependency-analysis | 依赖分析 - 识别并行/串行关系 | `ai-assistant:dependency-analysis` |

### 执行类

| 角色 | 用途 | Skill 调用 |
|------|------|-----------|
| code-implementation | 代码实现 - 按计划编写代码 | `ai-assistant:code-implementation` |
| executing-plans | 执行计划 - 调度多个任务执行 | `ai-assistant:executing-plans` |

### 验证类

| 角色 | 用途 | Skill 调用 |
|------|------|-----------|
| verification | 功能验证 - 确认代码正确实现需求 | `ai-assistant:verification` |
| e2e-tester | E2E 测试 - 端到端测试 | `ai-assistant:e2e-tester` |

### 审查类

| 角色 | 用途 | Skill 调用 |
|------|------|-----------|
| code-review | 代码审查 - 验证代码质量 | `ai-assistant:code-review` |
| security-review | 安全审查 - 检查安全漏洞 | `ai-assistant:security-review` |

### 调试类

| 角色 | 用途 | Skill 调用 |
|------|------|-----------|
| debugging | 调试专家 - 定位和修复 bug | `ai-assistant:debugging` |
| browser-debugger | 浏览器调试 - 捕获前端错误 | `ai-assistant:browser-debugger` |

### 分析类

| 角色 | 用途 | Skill 调用 |
|------|------|-----------|
| code-analysis | 代码分析 - 系统分析代码问题 | `ai-assistant:code-analysis` |
| project-researcher | 项目调研 - 调研项目现状 | `ai-assistant:project-researcher` |
| web-researcher | 网页研究 - 爬取和研究网页 | `ai-assistant:web-researcher` |

### 辅助类

| 角色 | 用途 | Skill 调用 |
|------|------|-----------|
| thinking-coach | 思维教练 - 厘清思路 | `ai-assistant:thinking-coach` |
| strategist | 策略分析师 - 分析方案选择 | `ai-assistant:strategist` |
| team-generator | 团队生成 - 创建多角色协作团队 | `ai-assistant:team-generator` |
| tdd | 测试驱动开发 - TDD 流程 | `ai-assistant:tdd` |
| test-planner | 测试设计 - 设计测试用例 | `ai-assistant:test-planner` |

---

## 角色选择指南

### 按任务类型选择

| 任务类型 | 推荐角色组合 |
|----------|-------------|
| 新功能开发 | brainstorming → writing-plans → code-implementation → verification → code-review |
| Bug 修复 | debugging → verification → code-review |
| 需求不明确 | thinking-coach → brainstorming → requirement-analysis |
| 代码优化 | code-analysis → planning → implementation → verification |
| 安全相关 | security-review → verification |

### 按复杂度选择

| 复杂度 | 角色组合 |
|--------|---------|
| 简单 | brainstorming → writing-plans → code-implementation → verification |
| 普通 | requirement-analysis → writing-plans → code-implementation → verification → code-review |
| 复杂 | requirement-analysis → writing-plans → executing-plans → verification → code-review → security-review |

---

## 调用规则

### 必须使用 Skill 工具

所有角色调用必须使用 Skill 工具，不能使用 Task：

```
✅ 正确：
Skill: ai-assistant:brainstorming
Skill: ai-assistant:writing-plans

❌ 错误：
Task(subagent_type="brainstorming", prompt="...")
```

### 调用格式

```
【调度角色】
Skill: ai-assistant:<角色名>

【等待完成】
- 等待 Skill 执行完成
- 收集输出文档
- 检查执行结果
```
