# Claude Code 配置规范分析

> 基于 Claude Code 官网文档整理

## 配置文件位置

| 类型 | 位置 | 说明 |
|------|------|------|
| Skills | `skills/<name>/SKILL.md` | 技能目录 |
| Commands | `commands/<name>.md` | 命令文件 |
| Agents | `agents/<name>.md` | 代理文件 |
| Hooks | `hooks/hooks.json` + `hooks/*.sh` | 钩子配置 |

## 格式规范

### Skills YAML Frontmatter

```yaml
---
name: skill-name
description: 技能描述
disable-model-invocation: true  # 可选
allowed-tools: [Read, Grep]   # 可选
model: opus                   # 可选
---
```

### Commands 格式

```yaml
---
description: 命令描述
disable-model-invocation: true  # 可选
---
```

### Agents 格式

```yaml
---
name: agent-name
description: 代理描述
tools: [Read, Grep]
model: opus
---
```

### Hooks 格式

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "pattern",
        "hooks": [
          {
            "type": "command",
            "command": "...",
            "async": false
          }
        ]
      }
    ]
  }
}
```

## 当前项目分析

### 配置统计

| 类型 | 数量 | 格式正确 |
|------|------|----------|
| Skills | 14 | ✅ |
| Agents | 6 | ✅ |
| Commands | 5 | ✅ |
| Hooks | 4 | ✅ |

### 新增功能

- ToolUseStart Hook: 工具使用日志记录
- PreToolUse Hook: 权限验证，阻止危险命令

### 用户开发流程

```
需求阶段: discuss → interaction → blueprint
    ↓
规划阶段: brainstorming → writing-plans → planner
    ↓
执行阶段: executing-plans → tdd-guide
    ↓
审查阶段: requesting-code-review → code-review → receiving-code-review
    ↓
验证阶段: verification-before-completion
    ↓
完成阶段: update-blueprint
```

### 流程覆盖分析

| 阶段 | 技能 | 状态 |
|------|------|------|
| 需求 | discuss, interaction, blueprint | ✅ |
| 规划 | brainstorming, writing-plans, planner | ✅ |
| 执行 | executing-plans, tdd-guide | ✅ |
| 审查 | requesting-code-review, code-review, receiving-code-review | ✅ |
| 验证 | verification-before-completion | ✅ |
| 完成 | update-blueprint | ✅ |

## 需要补充的内容

### 根据 Claude Code 规范

| 项目 | 说明 | 优先级 |
|------|------|--------|
| CLAUDE.md | 项目根目录的全局上下文文件 | ⭐⭐ |
| .claude/CLAUDE.md | 项目级配置 | ⭐⭐ |

### 根据流程完善

| 项目 | 说明 | 优先级 |
|------|------|--------|
| architect | 架构设计（在规划阶段使用） | ⭐⭐ |
| dispatching-parallel-agents | 并行任务处理 | ⭐ |
| finishing-a-development-branch | 分支完成处理 | ⭐ |

## 建议

### 1. 添加 CLAUDE.md

在项目根目录添加 `CLAUDE.md`，定义项目的全局上下文。

### 2. 完善 architect 使用

在 planning 阶段可以使用 architect agent 进行架构设计。

### 3. 当前配置已较完善

- ✅ Skills 格式正确
- ✅ Agents 格式正确
- ✅ Commands 格式正确
- ✅ Hooks 配置正确
- ✅ 流程覆盖完整
