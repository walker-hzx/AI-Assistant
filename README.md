# AI Assistant

个人开发助手 - 基于 Claude Code 的定制插件。

## 简介

这是一个为你的开发工作流程定制的 Claude Code 插件，整合了你的代码规范、工作流程和开发习惯。

## 功能

### Skills

| Skill | 说明 |
|-------|------|
| brainstorming | 需求分析 - 将想法转化为需求 |
| writing-plans | 详细实施计划 - 创建分阶段实施计划 |
| executing-plans | 执行计划 - 按计划执行任务 |
| verification | 验证 - 确认代码正确实现需求 |
| code-review | 代码审查 - 确保代码质量 |
| test-planner | 测试设计 - 设计测试场景 |
| docs-sync | 框架文档同步 - 爬取官方文档 |
| learn-concept | 学习概念 - 搜索学习不熟悉的技术 |
| thinking-coach | 思维教练 - 反思思维方式 |
| team-generator | 团队生成 - 动态生成 Agent Team |
| debugging | 调试 - 系统化调试修复 bug |

### Agents

| Agent | 说明 |
|-------|------|
| planner | 规划专家 - 创建详细实施计划 |
| architect | 架构专家 - 系统设计决策 |
| tdd-guide | TDD 专家 - 测试驱动开发 |
| code-reviewer | 代码审查 - 质量与安全检查 |
| security-reviewer | 安全审查 - 漏洞检测 |
| e2e-runner | E2E 测试 - 端到端测试 |
| debugger | 调试专家 - 定位和修复 bug |

### Commands

| Command | 说明 |
|---------|------|
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
brainstorming → writing-plans → executing-plans → verification → code-review
```

### 完整流程

1. **需求阶段**
   - `/brainstorming` - 需求分析，明确要做什么

2. **规划阶段**
   - `/writing-plans` - 创建详细实施计划

3. **执行阶段**
   - 使用 TDD 方法开发
   - 每个任务完成后更新进度

4. **验证阶段**
   - `/verification` - 验证代码是否正常运行、实现是否满足需求

5. **审查阶段**
   - `/code-review` - 代码审查，确保代码质量
   - 完成后更新 `docs/蓝图.md`

## 项目结构

```
AI-Assistant/
├── skills/                 # Skills
│   ├── brainstorming/
│   ├── writing-plans/
│   ├── executing-plans/
│   ├── verification/
│   ├── code-review/
│   ├── team-generator/
│   └── ...
├── teams/                  # Agent Teams 配置
│   ├── requirements-incubation/
│   ├── debugging/
│   └── ...
├── commands/              # Commands
├── docs/                  # 文档
│   ├── requirements/      # 需求文档
│   ├── plans/            # 计划文档
│   ├── verification/     # 验收报告
│   ├── completed/         # 完成总结
│   └── claude-code/      # Claude Code 文档
└── scripts/               # 辅助脚本
```

## 进度追踪

本插件支持**文件式进度追踪**：

- **自动检测**：Session 开始时自动检查上次进度
- **自动创建**：brainstorming/writing-plans 自动创建进度文件
- **自动更新**：executing-plans 执行时自动更新任务状态
- **Session 恢复**：结束 session 时提示未完成任务

进度文件位置：`docs/plans/progress.md`

## 依赖插件

本插件结合了以下插件的功能：

- [superpowers](https://github.com/superpoweredai/superpowers) - 工作流核心
- [everything-claude-code](https://github.com/anthropics/everything-claude-code) - 语言 patterns
- [planning-with-files](https://github.com/OthmanAdi/planning-with-files) - 文件式规划

## 参考文档

- [Claude Code 官方文档](./docs/claude-code/)
- [配置规范草稿](./docs/config-draft.md)
- [项目蓝图](./docs/蓝图.md)

## 更新日志

See [CHANGELOG.md](./CHANGELOG.md)

## License

MIT
