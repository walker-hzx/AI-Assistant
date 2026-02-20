---
title: Claude Code 配置参考
source: 基于官网文档整理
---

# Claude Code 配置参考

> 基于 Claude Code 官网文档整理

## 目录

1. [Skills 技能](#skills-技能)
2. [Commands 命令](#commands-命令)
3. [Agents 代理](#agents-代理)
4. [Hooks 钩子](#hooks-钩子)
5. [Plugins 插件](#plugins-插件)
6. [Settings 设置](#settings-设置)

---

## Skills 技能

### 目录结构

```
skills/
└── skill-name/
    └── SKILL.md
```

### YAML Frontmatter 格式

```yaml
---
name: skill-name
description: 技能描述，说明何时使用
disable-model-invocation: true  # 可选，true=只能手动调用
allowed-tools: [Read, Grep]    # 可选，限制可用工具
model: opus                   # 可选，指定模型
context: fork                # 可选，fork=在子代理中运行
agent: agent-name            # 可选，配合 context: fork 使用
user-invocable: false        # 可选，false=从菜单隐藏
argument-hint: [filename]    # 可选，参数提示
---
```

### 字段说明

| 字段 | 类型 | 描述 |
|------|------|------|
| `name` | string | 技能名称，用于 /name 调用 |
| `description` | string | 描述，Claude 用于决定何时自动加载 |
| `disable-model-invocation` | boolean | true=只能手动调用，false=可自动触发 |
| `allowed-tools` | string[] | 允许使用的工具列表 |
| `model` | string | 模型 (haiku/sonnet/opus) |
| `context` | string | `fork` 在子代理中运行 |
| `agent` | string | 子代理类型 |
| `user-invocable` | boolean | false=从 / 菜单隐藏 |

### 支持文件

技能目录可以包含额外文件：

```
my-skill/
├── SKILL.md           # 必需，主说明
├── template.md        # 可选，模板
├── examples/          # 可选，示例目录
└── scripts/          # 可选，脚本目录
```

---

## Commands 命令

### 目录结构

```
commands/
└── command-name.md
```

### 格式

```yaml
---
description: 命令描述
disable-model-invocation: true  # 可选
---
```

**注意**: Commands 不需要 `name` 字段，文件名即命令名。

---

## Agents 代理

### 目录结构

```
agents/
└── agent-name.md
```

### 格式

```yaml
---
name: agent-name
description: 代理描述，说明何时使用
tools: [Read, Grep, Glob, Task]
model: opus
---
```

---

## Hooks 钩子

### 目录结构

```
hooks/
├── hooks.json         # 必需，钩子配置
└── *.sh              # 钩子脚本
```

### hooks.json 格式

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume|clear|compact",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/session-start.sh",
            "async": false
          }
        ]
      }
    ]
  }
}
```

### 钩子事件

| 事件 | 描述 |
|------|------|
| `SessionStart` | 会话开始时触发 |
| `Stop` | 会话结束时触发 |
| `ToolUseStart` | 工具执行前触发 |
| `ToolUseEnd` | 工具执行后触发 |

---

## Plugins 插件

### marketplace.json 格式

```json
{
  "schema_version": "1.0.0",
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "插件描述",
  "author": {
    "name": "作者名",
    "email": "email@example.com"
  },
  "homepage": "https://github.com/...",
  "repository": "https://github.com/...",
  "license": "MIT",
  "keywords": ["tag1", "tag2"],
  "platforms": ["claude-code", "cursor", "opencode"],
  "compatibility": {
    "min_claude_code": "1.0"
  },
  "capabilities": {
    "skills": true,
    "agents": true,
    "commands": true,
    "hooks": true
  }
}
```

---

## Settings 设置

### 配置文件位置

| 文件 | 范围 |
|------|------|
| `~/.claude/settings.json` | 全局 |
| `~/.claude/settings.local.json` | 本地覆盖 |
| `.claude/settings.json` | 项目级 |

### 常用设置

```json
{
  "permissions": {
    "allow": ["WebSearch", "Bash(ls:*)"],
    "deny": ["Bash(rm:-rf*)"]
  }
}
```

---

## 调用方式

| 类型 | 方式 |
|------|------|
| Skill | `/skill-name` 或 Task 工具 |
| Command | `/command-name` |
| Agent | `Task: agent-name` |

---

## 字符串替换

技能支持动态值：

| 变量 | 描述 |
|------|------|
| `$ARGUMENTS` | 调用时传递的参数 |
| `${CLAUDE_SESSION_ID}` | 当前会话 ID |

---

## 高级模式

### 注入动态上下文

```yaml
---
name: pr-summary
description: Summarize pull request
context: fork
agent: Explore
allowed-tools: Bash(gh:*)
---

## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
```

`!`command`` 语法在技能执行前运行命令，输出替换占位符。
