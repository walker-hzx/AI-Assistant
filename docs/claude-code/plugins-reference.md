# Plugins 参考 - Claude Code

**来源**: https://code.claude.com/docs/zh-CN/plugins-reference

> 本文档包含 Plugins 参考的完整技术规范，包括组件架构、CLI 命令和开发工具。

---

## 目录

- [插件概述](#插件概述)
- [Plugin 组件参考](#plugin-组件参考)
  - [Skills](#skills)
  - [Agents](#agents)
  - [Hooks](#hooks)
  - [MCP servers](#mcp-servers)
  - [LSP servers](#lsp-servers)
- [Plugin 安装范围](#plugin-安装范围)
- [Plugin 清单架构](#plugin-清单架构)
- [Plugin 目录结构](#plugin-目录结构)
- [CLI 命令参考](#cli-命令参考)
- [调试和开发工具](#调试和开发工具)

---

## 插件概述

Plugin 是一个自包含的组件目录，用于扩展 Claude Code 的自定义功能。插件组件包括 skills、agents、hooks、MCP servers 和 LSP servers。

---

## Plugin 组件参考

### Skills

Plugins 向 Claude Code 添加 skills，创建可由您或 Claude 调用的 `/name` 快捷方式。

- **位置**: 插件根目录中的 `skills/` 或 `commands/` 目录
- **文件格式**: Skills 是包含 `SKILL.md` 的目录；commands 是简单的 markdown 文件

**Skill 结构**:

```
skills/
├── pdf-processor/
│   ├── SKILL.md
│   ├── reference.md (可选)
│   └── scripts/ (可选)
└── code-reviewer/
    └── SKILL.md
```

**集成行为**:
- 安装插件时会自动发现 Skills 和 commands
- Claude 可以根据任务上下文自动调用它们
- Skills 可以在 SKILL.md 旁边包含支持文件

---

### Agents

Plugins 可以为特定任务提供专门的 subagents，Claude 可以在适当时自动调用。

- **位置**: 插件根目录中的 `agents/` 目录
- **文件格式**: 描述 agent 功能的 Markdown 文件

**Agent 结构**:

```yaml
---
name: agent-name
description: 该 agent 的专长以及 Claude 应何时调用它
---

详细的系统提示，描述 agent 的角色、专业知识和行为。
```

**集成点**:
- Agents 出现在 `/agents` 界面中
- Claude 可以根据任务上下文自动调用 agents
- Agents 可以由用户手动调用
- Plugin agents 与内置 Claude agents 一起工作

---

### Hooks

Plugins 可以提供事件处理程序，自动响应 Claude Code 事件。

- **位置**: 插件根目录中的 `hooks/hooks.json`，或在 `plugin.json` 中内联
- **格式**: 具有事件匹配器和操作的 JSON 配置

**Hook 配置**:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format-code.sh"
          }
        ]
      }
    ]
  }
}
```

**可用事件**:
| 事件 | 描述 |
|------|------|
| PreToolUse | Claude 使用任何工具之前 |
| PostToolUse | Claude 成功使用任何工具之后 |
| PostToolUseFailure | Claude 工具执行失败之后 |
| PermissionRequest | 显示权限对话框时 |
| UserPromptSubmit | 用户提交提示时 |
| Notification | Claude Code 发送通知时 |
| Stop | Claude 尝试停止时 |
| SubagentStart | subagent 启动时 |
| SubagentStop | subagent 尝试停止时 |
| SessionStart | 会话开始时 |
| SessionEnd | 会话结束时 |
| TeammateIdle | agent 团队队友即将空闲时 |
| TaskCompleted | 任务被标记为已完成时 |
| PreCompact | 对话历史被压缩之前 |

**Hook 类型**:
- `command`: 执行 shell 命令或脚本
- `prompt`: 使用 LLM 评估提示（使用 `$ARGUMENTS` 占位符表示上下文）
- `agent`: 运行具有工具的 agentic 验证器以完成复杂验证任务

---

### MCP servers

Plugins 可以捆绑 Model Context Protocol (MCP) servers 以将 Claude Code 与外部工具和服务连接。

- **位置**: 插件根目录中的 `.mcp.json`，或在 `plugin.json` 中内联
- **格式**: 标准 MCP server 配置

**MCP server 配置**:

```json
{
  "mcpServers": {
    "plugin-database": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_PATH": "${CLAUDE_PLUGIN_ROOT}/data"
      }
    },
    "plugin-api-client": {
      "command": "npx",
      "args": ["@company/mcp-server", "--plugin-mode"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}"
    }
  }
}
```

**集成行为**:
- 启用插件时，Plugin MCP servers 会自动启动
- Servers 在 Claude 的工具包中显示为标准 MCP 工具
- Server 功能与 Claude 的现有工具无缝集成

---

### LSP servers

Plugins 可以提供 Language Server Protocol (LSP) servers，在处理代码库时为 Claude 提供实时代码智能。

**LSP 集成提供**:
- 即时诊断：Claude 在每次编辑后立即看到错误和警告
- 代码导航：转到定义、查找引用和悬停信息
- 语言感知：代码符号的类型信息和文档

- **位置**: 插件根目录中的 `.lsp.json`，或在 `plugin.json` 中内联
- **格式**: 将语言服务器名称映射到其配置的 JSON 配置

**.lsp.json 文件格式**:

```json
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

**必需字段**:
| 字段 | 描述 |
|------|------|
| command | 要执行的 LSP 二进制文件（必须在 PATH 中） |
| extensionToLanguage | 将文件扩展名映射到语言标识符 |

**可选字段**:
| 字段 | 描述 |
|------|------|
| args | LSP server 的命令行参数 |
| transport | 通信传输：stdio（默认）或 socket |
| env | 启动 server 时要设置的环境变量 |
| initializationOptions | 在初始化期间传递给 server 的选项 |
| settings | 通过 workspace/didChangeConfiguration 传递的设置 |
| workspaceFolder | server 的工作区文件夹路径 |
| startupTimeout | 等待 server 启动的最长时间（毫秒） |
| shutdownTimeout | 等待正常关闭的最长时间（毫秒） |
| restartOnCrash | server 崩溃时是否自动重启 |
| maxRestarts | 放弃前的最大重启尝试次数 |

**可用的 LSP plugins**:
| Plugin | 语言服务器 | 安装命令 |
|--------|------------|----------|
| pyright-lsp | Pyright (Python) | `pip install pyright` 或 `npm install -g pyright` |
| typescript-lsp | TypeScript Language Server | `npm install -g typescript-language-server typescript` |
| rust-lsp | rust-analyzer | 参阅 rust-analyzer 安装 |

---

## Plugin 安装范围

安装 plugin 时，您选择一个范围，确定 plugin 的可用位置以及谁可以使用它：

| 范围 | 设置文件 | 用例 |
|------|----------|------|
| user | ~/.claude/settings.json | 在所有项目中可用的个人 plugins（默认） |
| project | .claude/settings.json | 通过版本控制共享的团队 plugins |
| local | .claude/settings.local.json | 项目特定的 plugins，gitignored |
| managed | Managed settings | 托管 plugins（只读，仅更新） |

---

## Plugin 清单架构

`.claude-plugin/plugin.json` 文件定义了您的 plugin 的元数据和配置。

### 完整架构

```json
{
  "name": "plugin-name",
  "version": "1.2.0",
  "description": "Brief plugin description",
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "url": "https://github.com/author"
  },
  "homepage": "https://docs.example.com/plugin",
  "repository": "https://github.com/author/plugin",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "commands": ["./custom/commands/special.md"],
  "agents": "./custom/agents/",
  "skills": "./custom/skills/",
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "outputStyles": "./styles/",
  "lspServers": "./.lsp.json"
}
```

### 必需字段

如果包含清单，`name` 是唯一必需的字段。

| 字段 | 类型 | 描述 | 示例 |
|------|------|------|------|
| name | string | 唯一标识符（kebab-case，无空格） | "deployment-tools" |

### 元数据字段

| 字段 | 类型 | 描述 | 示例 |
|------|------|------|------|
| version | string | 语义版本 | "2.1.0" |
| description | string | plugin 目的的简要说明 | "Deployment automation tools" |
| author | object | 作者信息 | {"name": "Dev Team", "email": "dev@company.com"} |
| homepage | string | 文档 URL | "https://docs.example.com" |
| repository | string | 源代码 URL | "https://github.com/user/plugin" |
| license | string | 许可证标识符 | "MIT"、"Apache-2.0" |
| keywords | array | 发现标签 | ["deployment", "ci-cd"] |

### 组件路径字段

| 字段 | 类型 | 描述 | 示例 |
|------|------|------|------|
| commands | string\|array | 其他命令文件/目录 | "./custom/cmd.md" |
| agents | string\|array | 其他 agent 文件 | "./custom/agents/reviewer.md" |
| skills | string\|array | 其他 skill 目录 | "./custom/skills/" |
| hooks | string\|array\|object | Hook 配置路径或内联配置 | "./my-extra-hooks.json" |
| mcpServers | string\|array\|object | MCP 配置路径或内联配置 | "./my-extra-mcp-config.json" |
| outputStyles | string\|array | 其他输出样式文件/目录 | "./styles/" |
| lspServers | string\|array\|object | LSP 配置 | "./.lsp.json" |

### 环境变量

`${CLAUDE_PLUGIN_ROOT}`: 包含 plugin 目录的绝对路径。在 hooks、MCP servers 和脚本中使用此变量。

---

## Plugin 目录结构

### 标准 plugin 布局

```
enterprise-plugin/
├── .claude-plugin/           # 元数据目录（可选）
│   └── plugin.json             # plugin 清单
├── commands/                 # 默认命令位置
│   ├── status.md
│   └── logs.md
├── agents/                   # 默认 agent 位置
│   ├── security-reviewer.md
│   ├── performance-tester.md
│   └── compliance-checker.md
├── skills/                   # Agent Skills
│   ├── code-reviewer/
│   │   └── SKILL.md
│   └── pdf-processor/
│       ├── SKILL.md
│       └── scripts/
├── hooks/                    # Hook 配置
│   ├── hooks.json           # 主 hook 配置
│   └── security-hooks.json  # 其他 hooks
├── settings.json            # plugin 的默认设置
├── .mcp.json                # MCP server 定义
├── .lsp.json                # LSP server 配置
├── scripts/                 # Hook 和实用脚本
│   ├── security-scan.sh
│   ├── format-code.py
│   └── deploy.js
├── LICENSE                  # 许可证文件
└── CHANGELOG.md             # 版本历史
```

### 文件位置参考

| 组件 | 默认位置 | 目的 |
|------|----------|------|
| 清单 | .claude-plugin/plugin.json | Plugin 元数据和配置（可选） |
| 命令 | commands/ | Skill Markdown 文件 |
| Agents | agents/ | Subagent Markdown 文件 |
| Skills | skills/ | 具有 `<name>/SKILL.md` 结构的 Skills |
| Hooks | hooks/hooks.json | Hook 配置 |
| MCP servers | .mcp.json | MCP server 定义 |
| LSP servers | .lsp.json | 语言服务器配置 |
| 设置 | settings.json | 启用 plugin 时应用的默认配置 |

---

## CLI 命令参考

### plugin install

从可用市场安装 plugin。

```bash
claude plugin install <plugin> [options]
```

**参数**:
- `<plugin>`: Plugin 名称或 `plugin-name@marketplace-name` 用于特定市场

**选项**:
| 选项 | 描述 | 默认值 |
|------|------|--------|
| -s, --scope \<scope\> | 安装范围：user、project 或 local | user |

**示例**:
```bash
# 安装到用户范围（默认）
claude plugin install formatter@my-marketplace

# 安装到项目范围（与团队共享）
claude plugin install formatter@my-marketplace --scope project

# 安装到本地范围（gitignored）
claude plugin install formatter@my-marketplace --scope local
```

---

### plugin uninstall

删除已安装的 plugin。

```bash
claude plugin uninstall <plugin> [options]
```

**参数**:
- `<plugin>`: Plugin 名称或 plugin-name@marketplace-name

**选项**:
| 选项 | 描述 | 默认值 |
|------|------|--------|
| -s, --scope \<scope\> | 从范围卸载：user、project 或 local | user |

**别名**: remove, rm

---

### plugin enable

启用已禁用的 plugin。

```bash
claude plugin enable <plugin> [options]
```

---

### plugin disable

禁用 plugin 而不卸载它。

```bash
claude plugin disable <plugin> [options]
```

---

### plugin update

将 plugin 更新到最新版本。

```bash
claude plugin update <plugin> [options]
```

---

## 调试和开发工具

### 调试命令

使用 `claude --debug`（或 TUI 中的 `/debug`）查看 plugin 加载详情：

这显示：
- 正在加载哪些 plugins
- plugin 清单中的任何错误
- 命令、agent 和 hook 注册
- MCP server 初始化

---

## 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| Plugin 未加载 | 无效的 plugin.json | 使用 `claude plugin validate` 验证 JSON 语法 |
| 命令未出现 | 目录结构错误 | 确保 commands/ 在根目录，而不是在 .claude-plugin/ 中 |
| Hooks 未触发 | 脚本不可执行 | 运行 `chmod +x script.sh` |
| MCP server 失败 | 缺少 ${CLAUDE_PLUGIN_ROOT} | 对所有 plugin 路径使用变量 |
| 路径错误 | 使用了绝对路径 | 所有路径必须是相对的，并以 `./` 开头 |
| LSP Executable not found in $PATH | 语言服务器未安装 | 安装二进制文件 |

---

## 版本管理

遵循语义版本控制进行 plugin 发布：

```json
{
  "name": "my-plugin",
  "version": "2.1.0"
}
```

**版本格式**: MAJOR.MINOR.PATCH
- MAJOR: 破坏性更改（不兼容的 API 更改）
- MINOR: 新功能（向后兼容的添加）
- PATCH: 错误修复（向后兼容的修复）

**最佳实践**:
- 从 1.0.0 开始进行第一个稳定版本
- 在分发更改之前更新 plugin.json 中的版本
- 在 CHANGELOG.md 文件中记录更改
- 使用预发布版本，如 2.0.0-beta.1 进行测试

---

## 相关链接

- [Plugins 教程](https://code.claude.com/docs/zh-CN/plugins)
- [Plugin marketplaces](https://code.claude.com/docs/zh-CN/plugin-marketplaces)
- [Skills](https://code.claude.com/docs/zh-CN/skills)
- [Subagents](https://code.claude.com/docs/zh-CN/sub-agents)
- [Hooks](https://code.claude.com/docs/zh-CN/hooks)
- [MCP](https://code.claude.com/docs/zh-CN/mcp)
- [Settings](https://code.claude.com/docs/zh-CN/settings)
