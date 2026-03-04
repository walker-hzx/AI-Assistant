# 角色体系（Subagents）

> 6 核心角色 + 2 可选角色，由 Coordinator 根据任务复杂度自适应调度

## 核心角色

| 角色 | 职责 | Skills |
|------|------|--------|
| analyst | 需求理解、问题分析、策略制定 | requirement-analysis, requirement-understanding, thinking-coach |
| executor | 代码实现、功能开发 | code-implementation, executing-plans, tdd |
| tester | 测试设计、执行、功能验证 | tdd, verification, e2e-tester |
| reviewer | 代码审查、安全审查、质量评估 | code-review, security-review |
| researcher | 代码分析、项目调研、文档查阅 | code-analysis, project-researcher, web-researcher |
| debugger | Bug 定位和修复 | debugging |

## 可选角色（增强）

| 角色 | 职责 | 使用场景 |
|------|------|---------|
| skeptics | 建设性质疑 | L 档任务中对方案进行挑战 |
| ui-ux-reviewer | UI/UX 审查 | 前端页面视觉和交互审查 |

## 调度方式

Coordinator 根据任务复杂度选择 S/M/L 档：

```
S 档: Coordinator 直接执行，不调度角色
M 档: 调度 1-2 个角色，TodoWrite 跟踪
L 档: 完整调度流程（analyst → executor → tester → reviewer）
```

## 文件结构

```
agents/
├── analyst.md           # 分析师（需求 + 策略 + 思维）
├── executor.md          # 执行者（代码实现）
├── tester.md            # 测试员（单元/集成/E2E）
├── reviewer.md          # 审查员（代码 + 安全 + 质量）
├── researcher.md        # 研究员（代码分析 + 调研）
├── debugger.md          # 调试专家
├── skeptics.md          # 质疑者（可选）
├── ui-ux-reviewer.md    # UI/UX 审查（可选）
├── _archived/           # 旧版 agent 归档
└── README.md
```

【等待 Coordinator 决策】
```
