---
name: claude-code-docs
description: "Claude Code 官方文档爬取工具 - 爬取并整理官方文档，提取关键信息。用于更新插件配置、研究新功能时获取最新官方信息。使用 Playwright 爬取，需要等待页面渲染完成。"
model: sonnet
user-invocable: true
---

# Claude Code 官方文档工具

## 概述

爬取 Claude Code 官方文档，提取关键信息并整理成结构化文档。

**使用场景：**
- 需要了解某个功能的最新官方说明
- 更新插件配置时需要参考最新文档
- 研究新功能时获取官方信息

**运行爬取脚本：**
```bash
python3 ~/.claude/plugins/marketplaces/ai-assistant/scripts/fetch-docs/fetch-claude-code-docs.py
```

**爬取结果位置：** `docs/claude-code/`

## 概述

爬取 Claude Code 官方文档，提取关键信息并整理成结构化文档。

**使用场景：**
- 需要了解某个功能的最新官方说明
- 更新插件配置时需要参考最新文档
- 研究新功能时获取官方信息

---

## 目标文档

| 文档 | URL | 优先级 |
|------|-----|--------|
| Sub-agents | https://docs.anthropic.com/en/docs/claude-code/sub-agents | P0 |
| Skills | https://docs.anthropic.com/en/docs/claude-code/skills | P0 |
| Commands | https://docs.anthropic.com/en/docs/claude-code/slash-commands | P0 |
| Hooks | https://docs.anthropic.com/en/docs/claude-code/hooks | P1 |
| Plugins | https://docs.anthropic.com/en/docs/claude-code/plugins | P1 |
| Settings | https://docs.anthropic.com/en/docs/claude-code/settings | P1 |
| Agent Teams | https://docs.anthropic.com/en/docs/claude-code/agent-teams | P1 |

---

## 爬取脚本

### 脚本位置

```
~/.claude/plugins/marketplaces/ai-assistant/scripts/fetch-docs/fetch-claude-code-docs.py
```

### 运行方式

```bash
python3 ~/.claude/plugins/marketplaces/ai-assistant/scripts/fetch-docs/fetch-claude-code-docs.py
```

### 脚本功能

1. **自动爬取** - 使用 Playwright 访问官方文档页面
2. **HTML 清理** - 去除 CSS、JS、导航等垃圾数据
3. **Markdown 转换** - 转换为标准 Markdown 格式
4. **结构化保存** - 保存到 docs/claude-code/ 目录

---

## 输出结构

```
docs/claude-code/
├── sub-agents.md     # 爬取的原始文档
├── skills.md
├── commands.md
├── hooks.md
├── plugins.md
├── settings.md
└── agent-teams.md
```

---

## 信息提取模板

爬取完成后，需要提取关键信息：

### Sub-agents 提取

```markdown
## 核心概念

### 什么是 Sub-agent
[定义]

### 何时使用
[使用场景]

### 配置选项
| 选项 | 说明 | 示例 |
|------|------|------|
| tools | 可用工具列表 | [Read, Grep] |
| model | 指定模型 | sonnet/opus/haiku |
| description | 描述 | ... |

### 与 Skills 的区别
| 特性 | Sub-agent | Skill |
|------|-----------|-------|
| ... | ... | ... |
```

### Skills 提取

```markdown
## 核心概念

### 什么是 Skill
[定义]

### 字段说明
| 字段 | 类型 | 说明 |
|------|------|------|
| name | string | 技能名称 |
| description | string | 描述 |
| model | string | 模型 |
| user-invocable | boolean | 是否可调用 |
| ... | ... | ... |

### 存储位置
| 位置 | 作用域 |
|------|---------|
| ~/.claude/skills/ | 全局 |
| .claude/skills/ | 项目级 |
| plugins/*/skills/ | 插件级 |
```

---

## 执行流程

### 步骤 1：确认目标

用户说明需要爬取的文档：
- 可以指定具体文档
- 也可以要求全部爬取

### 步骤 2：运行爬取脚本

```bash
python3 ~/.claude/plugins/marketplaces/ai-assistant/scripts/fetch-docs/fetch-claude-code-docs.py
```

### 步骤 3：提取关键信息

根据用户需求，从爬取的文档中提取：
- 核心概念
- 配置选项
- 使用场景
- 与其他功能的区别

### 步骤 4：整理输出

将提取的信息整理成结构化格式，供后续使用

---

## 常见需求

### 需求 1：了解某个功能

用户想知道某个功能怎么用：
1. 爬取相关文档
2. 提取关键信息
3. 整理成简明说明

### 需求 2：配置优化

用户想优化某个配置：
1. 爬取最新文档
2. 提取配置选项
3. 对比当前配置

### 需求 3：功能研究

用户想了解新功能：
1. 爬取官方文档
2. 提取功能说明
3. 分析使用场景

---

## 注意事项

1. **网络问题** - 如果爬取失败，记录错误并告知用户
2. **内容质量** - 官方文档可能包含动态内容，可能需要人工检查
3. **定期更新** - 建议定期爬取最新文档保持同步

---

## 后续处理

爬取完成后，可以：
- 直接回答用户问题
- 更新现有文档
- 生成配置建议
- 分析优化点
