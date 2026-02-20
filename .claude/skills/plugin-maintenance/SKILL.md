---
name: plugin-maintenance
description: "用于维护和管理 AI-Assistant 项目配置。创建新技能/代理/命令、优化现有配置、验证格式。结合 superpowers 和 everything-claude-code 的最佳实践。"
---

# 插件维护技能

## 概述

用于维护和管理 AI-Assistant 项目的 Claude Code 配置（skills、agents、commands、hooks）。

## 核心功能

### 1. 创建新技能/代理/命令

根据需求创建新的配置：

**创建 Skill：**
```bash
# 目录结构
skills/
└── skill-name/
    └── SKILL.md
```

**创建 Agent：**
```bash
agents/
└── agent-name.md
```

**创建 Command：**
```bash
commands/
└── command-name.md
```

### 2. 优化现有配置

检查并优化现有配置：
- 检查 YAML frontmatter 格式
- 补充缺失字段
- 优化内容结构
- 确保符合规范

### 3. 格式验证

验证配置文件格式：

**Skill 格式：**
```yaml
---
name: skill-name
description: 描述
disable-model-invocation: true  # 可选
allowed-tools: [Read, Grep]     # 可选
model: sonnet                   # 可选
---
```

**Agent 格式：**
```yaml
---
name: agent-name
description: 描述
tools: [Read, Grep]
model: sonnet
---
```

**Command 格式：**
```yaml
---
description: 命令描述
disable-model-invocation: true  # 可选
---
```

## 工作流程

### 创建新配置

1. **确定类型**：skill / agent / command
2. **检查现有**：避免重复
3. **参考规范**：查看 `docs/claude-code/reference.md`
4. **创建文件**：按模板创建
5. **验证格式**：确保符合规范

### 优化现有配置

1. **扫描现有**：列出所有配置
2. **检查格式**：验证 YAML frontmatter
3. **分析内容**：检查是否完整
4. **提出建议**：列出优化项
5. **执行优化**：用户确认后执行

### 格式验证

1. **读取文件**：检查 YAML frontmatter
2. **验证字段**：name、description 等
3. **检查内容**：确保非空
4. **报告结果**：列出问题

## 参考资源

- Claude Code 规范：`docs/claude-code/reference.md`
- superpowers 参考：`/Users/huangzhixin/Desktop/Code/AI/superpowers/`
- everything-claude-code 参考：`/Users/huangzhixin/Desktop/Code/AI/everything-claude-code/`

## 检查清单

### 创建前
- [ ] 明确配置类型
- [ ] 检查是否已存在
- [ ] 确定放置位置

### 创建时
- [ ] 使用正确模板
- [ ] 添加必要字段
- [ ] 遵循命名规范

### 创建后
- [ ] 验证格式正确
- [ ] 检查内容完整
- [ ] 确认可正常加载

## 命名规范

| 类型 | 命名规范 | 示例 |
|------|----------|------|
| Skill | kebab-case | `plugin-maintenance` |
| Agent | kebab-case | `security-reviewer` |
| Command | kebab-case | `plan` |

## 常用命令

```bash
# 列出所有 skills
ls skills/

# 列出所有 agents
ls agents/

# 列出所有 commands
ls commands/

# 验证格式
# 检查 YAML frontmatter 是否正确
```

## 注意事项

- 项目级配置放在 `.claude/` 目录
- 插件级配置放在项目根目录
- 确保描述清晰，便于 Claude 自动加载
- 优先使用 disable-model-invocation: true 防止误触发
