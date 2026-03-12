# 角色体系（Subagents）

> 7 核心角色 + 2 可选角色，命令直达对应 Agent（v5.0 直达自治模式）

## 核心角色

| 角色 | 模型 | 记忆 | 职责 | Skills | 直达命令 |
|------|------|------|------|--------|---------|
| analyst | opus | project | 需求分析、策略制定、思维引导 | requirement-analysis, requirement-understanding, requirement-validation, thinking-coach, brainstorming | /thinking |
| executor | inherit | project | 代码实现、功能开发、代码重构 | code-implementation, tdd, vue3-vite-guide, python-fastapi-guide, refactoring | /implement, /refactor |
| tester | inherit | project | 测试设计、执行、功能验证 | tdd, verification, e2e-tester | /verification, /test-planner |
| reviewer | inherit | project | 代码审查、安全审查、质量评估 | code-review, security-review | /review, /security-review |
| researcher | inherit | project | 代码分析、技术调研、文档编写 | code-analysis, project-researcher, web-researcher, doc-writing | /learn-concept, /analyze, /docs |
| debugger | inherit | project | Bug 定位和修复 | debugging, browser-debugger | /debugging |
| scout | haiku | — | 外部资源获取 | web-researcher, docs-sync | /docs-sync |

## 可选角色

| 角色 | 职责 | 使用场景 |
|------|------|---------|
| skeptics | 建设性质疑 | 对方案进行挑战，发现盲点 |
| ui-ux-reviewer | UI/UX 审查 | 前端页面视觉和交互审查 |

## 直达模式

无 Coordinator，每个命令直达对应 Agent 或加载 Skill：

```
用户 → /implement → executor（独立子会话）
用户 → /plan → writing-plans skill（主线程加载）
用户 → /discuss → brainstorming skill（主线程加载）
```

## 文件结构

```
agents/
├── analyst.md           # 分析师（需求 + 策略 + 思维 + 头脑风暴）
├── executor.md          # 执行者（代码实现 + 重构）
├── tester.md            # 测试员（单元/集成/E2E）
├── reviewer.md          # 审查员（代码 + 安全 + 质量）
├── researcher.md        # 调研员（代码分析 + 调研 + 文档编写）
├── debugger.md          # 调试专家
├── scout.md             # 侦察员（外部资源获取）
├── skeptics.md          # 质疑者（可选）
├── ui-ux-reviewer.md    # UI/UX 审查（可选）
├── _archived/           # 旧版 agent 归档
└── README.md
```
