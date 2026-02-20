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
| update-blueprint | 蓝图更新助手 - 更新项目蓝图 |
| frontend-guide | 前端开发指南 - Vue3 + TypeScript 规范 |
| backend-guide | 后端开发指南 - Python + FastAPI 规范 |

## 安装

将插件安装到 Claude Code：

```bash
# 方法 1: 链接本地插件
ln -s /path/to/AI-Assistant ~/.claude/plugins/ai-assistant

# 方法 2: 复制到插件目录
cp -r AI-Assistant ~/.claude/plugins/
```

## 使用方法

### 需求讨论

当有新功能需求时：

```
/discuss-requirements
```

### 交互描述

需求明确后，描述交互：

```
/describe-interaction
```

### 更新蓝图

每个关键节点更新项目蓝图：

```
/update-blueprint
```

### 前端开发

开发前端时参考规范：

```
/frontend-guide
```

### 后端开发

开发后端时参考规范：

```
/backend-guide
```

## 项目结构

```
AI-Assistant/
├── .claude-plugin/        # 插件清单
├── skills/                # Skills
│   ├── discuss-requirements/
│   ├── describe-interaction/
│   ├── update-blueprint/
│   ├── frontend-guide/
│   └── backend-guide/
├── agents/                 # Agents（待添加）
├── commands/              # Commands（待添加）
├── hooks/                 # Hooks（待添加）
├── rules/                 # Rules（待添加）
└── docs/
    ├── config-draft.md   # 配置规范草稿
    └── 蓝图.md          # 项目蓝图
```

## 依赖插件

本插件结合了以下插件的功能：

- [superpowers](https://github.com/superpoweredai/superpowers) - 工作流核心
- [everything-claude-code](https://github.com/anthropics/everything-claude-code) - 语言 patterns

## 工作流程

```
1. 需求沟通
   └── /discuss-requirements

2. 交互描述
   └── /describe-interaction

3. 技术方案
   └── 参考 /backend-guide 或 /frontend-guide

4. 编码实现
   └── 使用 TDD 方法

5. 更新蓝图
   └── /update-blueprint

6. 代码审查
   └── 使用 code-reviewer agent
```

## 文档

- [配置规范草稿](./docs/config-draft.md) - 完整的工作流规范
- [项目蓝图](./docs/蓝图.md) - 项目现状记录

## 更新日志

### v1.0.0

- 初始版本
- 创建核心 Skills
- 整理代码规范

## License

MIT
