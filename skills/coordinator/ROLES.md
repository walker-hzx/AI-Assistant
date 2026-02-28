# Subagent 角色定义

> 本文档定义 Coordinator 可调度的 Subagent 角色

---

## 角色列表

### 分析类

| 角色 | 用途 | 典型场景 |
|------|------|---------|
| thinking-coach | 思维教练 - 厘清思路，给出方向 | 需求不清晰、方向不明 |
| strategist | 策略分析师 - 深度分析，评估方案 | 多个方案需要选择 |
| code-analysis | 代码分析 - 系统分析代码问题 | 代码有问题需要分析 |
| project-researcher | 项目调研 - 调研项目现状 | 需要了解项目现状 |
| web-researcher | 网页研究 - 爬取和研究网页 | 需要查资料/文档 |

### 需求类

| 角色 | 用途 | 典型场景 |
|------|------|---------|
| requirement-analysis | 需求分析 - 多角度分析需求完整性 | 需求需要详细分析 |
| requirements-miner | 需求挖掘 - 逆向分析代码提取功能 | 中途接手项目、没有需求文档 |

### 实现类

| 角色 | 用途 | 典型场景 |
|------|------|---------|
| executor | 代码实现 - 按计划编写代码 | 需要编写代码 |

### 验证类

| 角色 | 用途 | 典型场景 |
|------|------|---------|
| e2e-tester | E2E 测试 - 端到端测试 | 需要 E2E 测试 |
| test-designer | 测试设计 - 分析需求深度，挖掘复杂场景，设计测试用例 | 需要设计测试用例 |
| qa | 质量保证 - 验证功能正确性 | 需要验证功能 |

### 审查类

| 角色 | 用途 | 典型场景 |
|------|------|---------|
| security-reviewer | 安全审查 - 检查安全漏洞 | 需要安全审查 |
| code-reviewer | 代码审查 - 验证代码质量 | 需要代码审查 |
| ui-ux-reviewer | UI/UX 审查 - 分析页面视觉和交互，提供优化方案 | 需要优化页面样式和交互 |
| evaluator | 质量评估 - 评估产出物质量，生成优化建议 | 需要质量门控、流程复盘 |

### 调试类

| 角色 | 用途 | 典型场景 |
|------|------|---------|
| debugger | 调试专家 - 定位和修复 bug | 需要调试 bug |
| browser-debugger | 浏览器调试 - 捕获前端错误 | 前端需要调试 |

### 辅助类

| 角色 | 用途 | 典型场景 |
|------|------|---------|
| team-generator | 团队生成 - 创建多角色协作团队 | 需要并行任务 |

---

## 按阶段调用

| 阶段 | 可调用的 Subagent |
|------|------------------|
| 需求分析 | thinking-coach, requirement-analysis, requirements-miner, web-researcher, project-researcher |
| 任务规划 | strategist |
| 代码执行 | executor, web-researcher |
| 测试验证 | test-designer, e2e-tester, qa |
| 安全审查 | security-reviewer |
| 代码审查 | code-reviewer |
| UI/UX 优化 | ui-ux-reviewer |
| 质量评估 | evaluator |
| 问题调试 | debugger, browser-debugger, code-analysis |
| 复杂决策 | strategist, team-generator |

---

## 调用方式

使用 Task 工具调用 Subagent：

```
Task(ai-assistant:<角色名>)
```

示例：
```
Task(ai-assistant:executor)
Task(ai-assistant:debugger)
Task(ai-assistant:requirements-analyst)
```
