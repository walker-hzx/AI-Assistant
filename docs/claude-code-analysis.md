# Claude Code 配置系统分析

## 概述

本文档详细分析 Claude Code 的配置系统，并对比 superpowers 和 everything-claude-code 两个参考项目的实现方式。

---

## 一、Claude Code 配置系统核心概念

### 1.1 配置作用域（优先级）

Claude Code 使用四级作用域系统，优先级从高到低：

| 作用域 | 位置 | 影响范围 | 是否共享 |
|--------|------|----------|----------|
| Managed | 系统目录 | 全组织 | 由 IT 部署 |
| Local | .claude/settings.local.json | 当前项目（个人） | 否 |
| Project | .claude/settings.json | 项目团队 | 是 |
| User | ~/.claude/settings.json | 个人所有项目 | 否 |

**优先级规则**：更具体的作用域覆盖更广泛的作用域

### 1.2 核心配置文件

```
~/.claude/
├── settings.json          # 用户级配置
├── agents/                # 自定义子代理
├── skills/                # 自定义技能
├── hooks/                 # 自定义钩子
├── CLAUDE.md              # 记忆文件
├── rules/                 # 规则文件
└── plugins/               # 已安装插件

项目目录/
├── .claude/
│   ├── settings.json      # 项目级配置
│   ├── agents/            # 项目级代理
│   ├── skills/            # 项目级技能
│   ├── hooks/             # 项目级钩子
│   └── CLAUDE.md         # 项目记忆文件
└── .mcp.json             # MCP 服务器配置
```

### 1.3 核心配置组件

#### 1. Skills（技能）

- **位置**：`~/.claude/skills/<skill-name>/SKILL.md` 或 `.claude/skills/`
- **调用方式**：`/skill-name` 或 Claude 自动加载
- **核心字段**：
  - `name`: 技能名称（变成 / 命令）
  - `description`: 描述（用于自动触发）
  - `disable-model-invocation`: 禁止自动触发
  - `allowed-tools`: 限制可用工具
  - `context`: 设为 `fork` 可在子代理中运行

#### 2. Agents（代理）

- **位置**：`~/.claude/agents/<agent-name>.md` 或 `.claude/agents/`
- **定义格式**：YAML frontmatter + Markdown 正文
- **核心字段**：
  - `name`: 代理名称
  - `description`: 描述
  - `tools`: 允许使用的工具列表
  - `model`: 使用的模型

#### 3. Hooks（钩子）

- **配置位置**：`settings.json` 中的 `hooks` 字段
- **事件类型**：
  - `PreToolUse`: 工具执行前
  - `PostToolUse`: 工具执行后
  - `Stop`: 会话结束时
  - `SessionStart`: 会话开始时
  - `SessionEnd`: 会话结束时
  - `UserPromptSubmit`: 用户提交提示时

#### 4. Rules（规则）

- **位置**：`~/.claude/rules/` 目录
- **用途**：始终遵循的编码规范和最佳实践
- **格式**：Markdown 文件

### 1.4 settings.json 核心配置项

```json
{
  "env": {
    "ANTHROPIC_MODEL": "MiniMax-M2.5",
    "MAX_THINKING_TOKENS": "10000"
  },
  "permissions": {
    "allow": ["Bash(git:*)"],
    "deny": ["Read(./.env)"]
  },
  "hooks": { ... },
  "enabledPlugins": {
    "everything-claude-code@everything-claude-code": true
  }
}
```

---

## 二、superpowers 项目分析

### 2.1 项目结构

```
superpowers/
├── .claude/              # 插件配置
├── agents/               # 自定义代理 (15个)
├── commands/             # 斜杠命令 (33个)
├── contexts/            # 动态上下文
├── hooks/               # 钩子配置
├── mcp-configs/         # MCP 配置
├── rules/               # 规则
├── schemas/             # JSON Schema
├── skills/              # 技能 (45个)
├── tests/               # 测试
└── scripts/             # 脚本
```

### 2.2 核心技能（Skills）

| 类别 | 技能名称 | 用途 |
|------|----------|------|
| **测试** | test-driven-development | 红-绿-重构 TDD 流程 |
| **调试** | systematic-debugging | 四阶段根因分析 |
| **调试** | verification-before-completion | 确保问题真正修复 |
| **协作** | brainstorming | 苏格拉底式设计精炼 |
| **协作** | writing-plans | 详细实现计划 |
| **协作** | executing-plans | 带检查点的批量执行 |
| **协作** | dispatching-parallel-agents | 并发子代理工作流 |
| **协作** | requesting-code-review | 预审查检查清单 |
| **协作** | receiving-code-review | 响应反馈 |
| **协作** | using-git-worktrees | 并行开发分支 |
| **协作** | finishing-a-development-branch | 合并/PR 决策 |
| **协作** | subagent-driven-development | 快速迭代与两阶段审查 |
| **元技能** | writing-skills | 创建新技能 |
| **元技能** | using-superpowers | 技能系统介绍 |

### 2.3 工作流理念

```
brainstorming → using-git-worktrees → writing-plans →
subagent-driven-development → test-driven-development →
requesting-code-review → finishing-a-development-branch
```

### 2.4 关键特性

- **强制工作流**：智能体在执行任务前必须检查相关技能
- **子代理驱动开发**：通过子代理并行执行任务
- **两阶段审查**：规格合规性 → 代码质量
- **YAGNI 原则**：严格避免过度工程

---

## 三、everything-claude-code 项目分析

### 3.1 项目结构

```
everything-claude-code/
├── .claude-plugin/       # 插件清单
├── agents/               # 子代理 (13个)
├── commands/             # 斜杠命令 (31个)
├── contexts/             # 动态上下文
├── hooks/                # 钩子配置
├── lib/                 # 共享库
├── mcp-configs/         # MCP 配置
├── rules/               # 规则 (多语言)
├── skills/              # 技能 (43个)
└── tests/               # 测试
```

### 3.2 核心代理（Agents）

| 代理 | 用途 |
|------|------|
| planner | 功能实现规划 |
| architect | 系统设计决策 |
| tdd-guide | 测试驱动开发 |
| code-reviewer | 代码质量审查 |
| security-reviewer | 安全漏洞分析 |
| build-error-resolver | 构建错误修复 |
| e2e-runner | Playwright E2E 测试 |
| refactor-cleaner | 死代码清理 |
| doc-updater | 文档同步 |
| go-reviewer | Go 代码审查 |
| go-build-resolver | Go 构建错误修复 |
| python-reviewer | Python 代码审查 |
| database-reviewer | 数据库/Supabase 审查 |

### 3.3 技能分类

| 类别 | 技能示例 |
|------|----------|
| 语言模式 | golang-patterns, python-patterns, java-coding-standards |
| 框架模式 | django-patterns, springboot-patterns, frontend-patterns |
| 测试 | golang-testing, python-testing, django-tdd |
| 安全 | security-review, django-security, springboot-security |
| 部署 | deployment-patterns, docker-patterns |
| 数据库 | postgres-patterns, clickhouse-io |
| 验证 | verification-loop, django-verification, springboot-verification |
| 学习 | continuous-learning, continuous-learning-v2 |

### 3.4 规则架构

```
rules/
├── common/              # 通用规则 (8个)
│   ├── coding-style.md
│   ├── git-workflow.md
│   ├── testing.md
│   ├── performance.md
│   ├── patterns.md
│   ├── hooks.md
│   ├── agents.md
│   └── security.md
├── typescript/          # TypeScript 规则
├── python/              # Python 规则
└── golang/              # Go 规则
```

### 3.5 关键特性

- **Token 优化**：模型选择、环境变量配置
- **连续学习**：从会话中自动提取模式
- **多语言支持**：TypeScript、Python、Go、Java、Django、Spring Boot
- **多平台支持**：Claude Code、Cursor、OpenCode

---

## 四、对比分析

### 4.1 配置系统对比

| 特性 | Claude Code 原生 | superpowers | everything-claude-code |
|------|-----------------|-------------|------------------------|
| Skills | ✅ 基础支持 | ✅ 45 个技能 | ✅ 43 个技能 |
| Agents | ✅ 基础支持 | ✅ 15 个代理 | ✅ 13 个代理 |
| Hooks | ✅ 完整支持 | ✅ 有配置 | ✅ 有配置 |
| Rules | ❌ 无原生支持 | ❌ | ✅ 完整规则系统 |
| 插件 | ✅ Plugin 系统 | ✅ | ✅ |

### 4.2 工作流对比

| 特性 | superpowers | everything-claude-code |
|------|-------------|------------------------|
| 核心流程 | 头脑风暴 → 计划 → 执行 → 审查 | 灵活组合 |
| TDD | 强制执行 | 可选使用 |
| 子代理 | 两阶段审查 | 多种代理类型 |
| 学习 | 无 | 连续学习系统 |

### 4.3 规则系统对比

| 规则类型 | superpowers | everything-claude-code | 你的现有规则 |
|----------|-------------|------------------------|--------------|
| 编码风格 | 无 | ✅ | ✅ |
| Git 工作流 | 无 | ✅ | ✅ |
| 测试 | ✅ TDD 技能 | ✅ | ✅ |
| 性能 | 无 | ✅ | ✅ |
| Hooks | 无 | ✅ | ✅ |
| 代理 | 无 | ✅ | ✅ |
| 安全 | 无 | ✅ | ✅ |
| 模式 | 无 | ✅ | ✅ |

---

## 五、你的现有配置

### 5.1 当前安装的插件

```json
{
  "enabledPlugins": {
    "everything-claude-code@everything-claude-code": true,
    "superpowers@superpowers-marketplace": true
  }
}
```

### 5.2 当前规则

位于 `~/.claude/rules/`：

```
rules/
├── common/              # 8 个通用规则
│   ├── agents.md
│   ├── coding-style.md
│   ├── git-workflow.md
│   ├── hooks.md
│   ├── patterns.md
│   ├── performance.md
│   ├── security.md
│   └── testing.md
├── python/              # Python 规则
│   ├── coding-style.md
│   ├── hooks.md
│   ├── patterns.md
│   ├── security.md
│   └── testing.md
└── typescript/          # TypeScript 规则
    ├── coding-style.md
    ├── hooks.md
    ├── patterns.md
    ├── security.md
    └── testing.md
```

---

## 六、配置系统总结图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Claude Code 配置系统                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │
│  │   Skills    │    │   Agents    │    │   Hooks    │        │
│  │  (/命令)    │    │  (子代理)   │    │  (钩子)    │        │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘        │
│         │                  │                  │                │
│         └──────────────────┼──────────────────┘                │
│                            ▼                                     │
│                   ┌─────────────────┐                          │
│                   │  settings.json   │                          │
│                   │  (权限/环境变量) │                          │
│                   └─────────────────┘                          │
│                            │                                     │
│         ┌──────────────────┼──────────────────┐                 │
│         ▼                  ▼                  ▼                 │
│  ┌────────────┐    ┌────────────┐    ┌────────────┐           │
│  │   User     │    │  Project   │    │  Managed   │           │
│  │  (~/.claude)│    │ (.claude/) │    │ (系统目录)  │           │
│  └────────────┘    └────────────┘    └────────────┘           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      你的当前配置                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  已安装插件：                                                   │
│  ├── everything-claude-code (43 skills, 13 agents)             │
│  └── superpowers (45 skills, 15 agents)                        │
│                                                                 │
│  你的规则 (~/.claude/rules/):                                  │
│  ├── common/  (8 个规则)                                       │
│  ├── python/  (5 个规则)                                       │
│  └── typescript/ (5 个规则)                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 七、下一步

根据以上分析，你目前已经：

1. ✅ 安装了 superpowers 和 everything-claude-code 两个插件
2. ✅ 配置了一套完整的规则（common + python + typescript）
3. ✅ 有 Claude Code 原生配置

**需要确认的问题**：

1. 你最常用的开发语言是什么？（这影响规则的选择）
2. 你更倾向于 superpowers 的"强制工作流"还是 everything-claude-code 的"灵活组合"？
3. 你是否需要连续学习功能（从会话中提取模式）？
4. 你的团队协作需求是什么？（个人使用 vs 团队共享）

---

*文档生成时间：2026-02-19*
*数据来源：Claude Code 官方文档 + superpowers 项目 + everything-claude-code 项目*
