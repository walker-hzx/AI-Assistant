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

### Agents

| Agent | 说明 |
|-------|------|
| coordinator | 智能调度 - 任务调度和协调 |
| requirements-analyst | 需求分析师 - 理解用户真正想要什么 |
| planner | 规划专家 - 创建详细实施计划 |
| executor | 执行者 - 按计划实现代码 |
| qa | 质量保证 - 验证功能正确 |
| code-reviewer | 代码审查 - 确保代码质量 |
| debugger | 调试专家 - 定位和修复 bug |
| thinking-coach | 思维教练 - 反思思维方式 |
| strategist | 策略分析师 - 深度分析决策 |
| architect | 架构师 - 系统设计决策 |
| database-expert | 数据库专家 - 数据库设计优化 |
| performance-expert | 性能专家 - 性能分析优化 |
| refactoring-expert | 重构专家 - 代码重构 |
| security-reviewer | 安全审查 - 漏洞检测 |
| test-designer | 测试设计 - 设计测试用例 |
| code-analyst | 代码分析师 - 系统分析代码 |
| project-researcher | 项目调研 - 中途接手项目 |
| web-researcher | 网页研究 - 爬取网页分析 |
| e2e-tester | E2E 测试 - 执行端到端测试 |

### Commands

| Command | 说明 |
|---------|------|
| /assistant | 智能助手 - 一句话需求，智能调度 |
| /brainstorming | 需求分析 - 将想法转化为需求 |
| /writing-plans | 制定实施计划 |
| /verification | 验证 - 确认代码正确实现需求 |
| /code-review | 代码审查 |
| /team-generator | 团队生成 - 创建多角色协作团队 |
| /thinking | 思维反思 - 使用 thinking-coach 技能 |

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
需求 → 规划 → 执行 → 验证 → 审查
  ↓      ↓      ↓      ↓      ↓
coordinator → planner → executor → qa → code-reviewer
```

### 完整流程

1. **需求阶段**
   - `/assistant` - 一句话需求，智能调度
   - 或 `/brainstorming` - 需求分析，明确要做什么

2. **规划阶段**
   - coordinator-planning - 制定执行方案
   - coordinator-dispatch - 任务派发

3. **执行阶段**
   - executor - 按计划实现代码
   - 使用 TDD 方法开发
   - 每个任务完成后更新进度

4. **验证阶段**
   - qa - 功能验证
   - e2e-tester - E2E 测试

5. **审查阶段**
   - code-reviewer - 代码审查，确保代码质量
   - 完成后更新 `docs/蓝图.md`

## 项目结构

```
AI-Assistant/
├── skills/                  # Skills (34个)
│   ├── assistant/
│   ├── brainstorming/
│   ├── coordinator-intent/
│   ├── coordinator-planning/
│   ├── coordinator-dispatch/
│   ├── writing-plans/
│   ├── executing-plans/
│   ├── verification/
│   ├── code-review/
│   ├── debugging/
│   ├── thinking-coach/
│   ├── web-researcher/
│   ├── e2e-tester/
│   └── ...
├── agents/                  # Agents (18个)
│   ├── coordinator.md
│   ├── requirements-analyst.md
│   ├── planner.md
│   ├── executor.md
│   ├── qa.md
│   ├── code-reviewer.md
│   ├── debugger.md
│   ├── e2e-tester.md
│   ├── web-researcher.md
│   └── ...
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

自主设计的 Claude Code 插件，基于团队协作理念：

- **管家调度**：Coordinator 协调分析、计划、执行
- **角色分工**：不同角色负责不同阶段
- **文档驱动**：每个阶段产出明确文档

## 参考文档

- [Claude Code 官方文档](./docs/claude-code/)
- [配置规范草稿](./docs/config-draft.md)
- [项目蓝图](./docs/蓝图.md)

## 更新日志

See [CHANGELOG.md](./CHANGELOG.md)

## License

MIT
