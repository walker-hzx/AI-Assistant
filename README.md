# AI Assistant

个人开发助手 - 基于 Claude Code 的定制插件。

## 简介

这是一个为你的开发工作流程定制的 Claude Code 插件，整合了你的代码规范、工作流程和开发习惯。

## 功能

### Skills

| Skill | 说明 |
|-------|------|
| assistant | 智能助手入口 - 一句话需求，智能调度 |
| brainstorming | 需求分析 - 将想法转化为需求 |
| requirement-understanding | 需求理解 - 澄清用户真正意图 |
| requirement-analysis | 需求分析 - 多角度分析需求 |
| requirement-validation | 需求验证 - 确认需求完整 |
| writing-plans | 详细实施计划 - 创建分阶段实施计划 |
| task-splitting | 任务拆分 - 拆分为小任务 |
| dependency-analysis | 依赖分析 - 识别任务依赖 |
| milestone-planning | 里程碑规划 - 划分执行阶段 |
| executing-plans | 执行计划 - 按计划执行任务 |
| code-implementation | 代码实现 - 按步骤编写代码 |
| tdd | 测试驱动开发 - 先写测试再写实现 |
| progress-tracking | 进度追踪 - 记录执行状态 |
| verification | 功能验证 - 确认代码正确实现需求 |
| security-verification | 安全验证 - 检查安全漏洞 |
| code-review | 代码审查 - 确保代码质量 |
| debugging | 调试 - 系统化调试修复 bug |
| code-analysis | 代码分析 - 系统分析代码问题 |
| security-review | 安全审查 - 识别安全漏洞 |
| test-planner | 测试设计 - 设计测试场景 |
| thinking-coach | 思维教练 - 反思思维方式 |
| strategist | 策略分析师 - 深度分析决策 |
| project-researcher | 项目调研 - 中途接手项目分析 |
| web-researcher | 网页研究 - 爬取网页分析 |
| e2e-testing | E2E 测试 - 执行端到端测试 |
| learn-concept | 学习概念 - 搜索学习不熟悉的技术 |
| team-generator | 团队生成 - 动态生成 Agent Team |
| docs-sync | 框架文档同步 - 爬取官方文档 |
| claude-code-docs | Claude Code 文档 - 爬取官方文档 |
| update-blueprint | 更新蓝图 - 记录项目状态 |
| python-fastapi-guide | Python FastAPI 开发指南 |
| vue3-vite-guide | Vue3 Vite 开发指南 |

### Agents（6 核心 + 2 可选）

| Agent | 说明 |
|-------|------|
| analyst | 需求理解、问题分析、策略制定 |
| executor | 代码实现、功能开发 |
| tester | 测试设计、执行、功能验证 |
| reviewer | 代码审查、安全审查、质量评估 |
| researcher | 代码分析、项目调研、文档查阅 |
| debugger | Bug 定位和修复 |
| skeptics | 建设性质疑（可选） |
| ui-ux-reviewer | UI/UX 审查（可选） |

### Commands

| Command | 说明 |
|---------|------|
| /brainstorming | 需求分析 - 将想法转化为需求 |
| /writing-plans | 制定实施计划 |
| /verification | 验证 - 确认代码正确实现需求 |
| /code-review | 代码审查 |
| /team-generator | 团队生成 - 创建多角色协作团队 |
| /thinking | 思维反思 - 使用 analyst 角色 |

## 安装

将插件安装到 Claude Code：

```bash
# 方法 1: 链接本地插件
ln -s /path/to/AI-Assistant ~/.claude/plugins/ai-assistant

# 方法 2: 复制到插件目录
cp -r AI-Assistant ~/.claude/plugins/
```

## 工作流程

```
S 档（简单）: 理解 → 直接执行 → 完成
M 档（中等）: 理解 → 计划 → executor → 验证 → 完成
L 档（复杂）: 理解 → analyst → 计划 → executor → tester → reviewer → 完成
```

### 三档自适应

1. **S 档（简单任务）**
   - Coordinator 直接执行，无需调度

2. **M 档（中等任务）**
   - 使用 TodoWrite 跟踪进度
   - 调度 1-2 个角色完成

3. **L 档（复杂任务）**
   - 完整调度流程
   - analyst 分析需求
   - executor 实现代码
   - tester 验证功能
   - reviewer 审查质量

## 项目结构

```
AI-Assistant/
├── skills/                  # Skills
│   ├── coordinator/        # 智能管家（核心调度）
│   ├── brainstorming/
│   ├── writing-plans/
│   ├── executing-plans/
│   ├── verification/
│   ├── code-review/
│   ├── debugging/
│   ├── code-analysis/
│   ├── web-researcher/
│   ├── e2e-tester/
│   └── ...
├── agents/                  # Agents（6 核心 + 2 可选）
│   ├── analyst.md
│   ├── executor.md
│   ├── tester.md
│   ├── reviewer.md
│   ├── researcher.md
│   ├── debugger.md
│   ├── skeptics.md
│   ├── ui-ux-reviewer.md
│   └── _archived/          # 旧版 agent 归档
├── commands/               # Commands
├── docs/                   # 文档
│   ├── requirements/       # 需求文档
│   ├── plans/             # 计划文档
│   ├── verification/      # 验收报告
│   ├── completed/         # 完成总结
│   ├── claude-code/       # Claude Code 文档
│   └── frameworks/        # 框架文档
├── scripts/                # 辅助脚本
│   ├── web/               # 网页爬取脚本
│   └── fetch-docs/        # 文档爬取脚本
└── contexts/               # 上下文配置
```

## 进度追踪

本插件支持**文件式进度追踪**：

- **自动检测**：Session 开始时自动检查上次进度
- **自动创建**：brainstorming/writing-plans 自动创建进度文件
- **自动更新**：executing-plans 执行时自动更新任务状态
- **Session 恢复**：结束 session 时提示未完成任务

进度文件位置：`docs/plans/progress.md`

## 项目理念

自主设计的 Claude Code 插件，基于自适应协作理念：

- **管家调度**：Coordinator 根据任务复杂度自适应选择 S/M/L 档流程
- **角色精简**：6 核心角色 + 2 可选角色，各司其职
- **上下文驱动**：信息在会话中流转，仅在 L 档任务创建文档

## 参考文档

- [Claude Code 官方文档](./docs/claude-code/)
- [配置规范草稿](./docs/config-draft.md)
- [项目蓝图](./docs/蓝图.md)

## 更新日志

See [CHANGELOG.md](./CHANGELOG.md)

## License

MIT
