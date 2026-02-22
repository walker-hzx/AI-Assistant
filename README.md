# AI Assistant

个人开发助手 - 基于 Claude Code 的定制插件。

## 简介

这是一个为你的开发工作流程定制的 Claude Code 插件，整合了你的代码规范、工作流程和开发习惯。

## 功能

### Skills

| Skill | 说明 |
|-------|------|
| discuss-requirements | 需求讨论助手 - 帮助明确需求 |
| describe-interaction | 交互描述助手 - 描述核心交互 |
| brainstorming | 头脑风暴 - 将想法转化为设计 |
| writing-plans | 详细实施计划 - 创建分阶段实施计划 |
| executing-plans | 执行计划 - 按计划执行任务 |
| test-planner | 测试设计 - 设计测试场景 |
| update-blueprint | 蓝图更新助手 - 更新项目蓝图 |
| verification-before-completion | 完成前验证 - 确保工作真正完成 |
| execution-validation | 需求对照验收 - 验证实现完整性 |
| docs-sync | 框架文档同步 - 爬取官方文档 |

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
| /discuss | 开始需求讨论 |
| /interaction | 描述交互细节 |
| /blueprint | 更新项目蓝图 |
| /plan | 制定实施计划 |
| /review | 代码审查 |
| /view-requirements | 查看需求文档 |
| /workflow-check | 检查流程是否正确 |
| /config-retrospect | 复盘配置使用情况 |

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
需求 → 规划 → 执行 → 审查 → 验证 → 完成
  ↓      ↓      ↓      ↓      ↓
discuss  brainstorming  writing-plans  executing-plans  verification  update-blueprint
         →writing-plans        →execution-validation   →blueprint
```

### 完整流程

1. **需求阶段**
   - `/discuss` - 需求讨论，明确要做什么
   - `/interaction` - 描述核心交互

2. **规划阶段**
   - `/brainstorming` - 头脑风暴，转化想法为设计
   - `/plan` - 创建详细实施计划

3. **执行阶段**
   - 使用 TDD 方法开发
   - 每个任务完成后更新进度

4. **审查阶段**
   - `/review` - 代码审查
   - 安全审查（如需要）

5. **验证阶段**
   - 验证代码是否正常运行
   - 验证实现是否满足需求

6. **完成阶段**
   - `/blueprint` - 更新项目蓝图
   - 提交代码

## 项目结构

```
AI-Assistant/
├── .claude-plugin/        # 插件清单
├── skills/                 # Skills
│   ├── discuss-requirements/
│   ├── brainstorming/
│   ├── writing-plans/
│   ├── executing-plans/
│   └── ...
├── agents/                 # Agents
│   ├── planner.md
│   ├── code-reviewer.md
│   └── ...
├── commands/              # Commands
│   ├── discuss.md
│   ├── blueprint.md
│   └── ...
├── hooks/                 # Hooks
│   ├── hooks.json
│   ├── session-start.sh
│   └── session-end.sh
├── docs/                  # 文档
│   ├── requirements/      # 需求文档
│   ├── plans/             # 计划文档
│   └── claude-code/       # Claude Code 官方文档
└── tests/                 # 测试
    └── e2e/
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
