---
name: plugin-architecture
description: "用于规划和设计 AI-Assistant 项目架构。设计目录结构、管理技能依赖、设计新功能工作流。结合 superpowers 和 everything-claude-code 的最佳实践。"
---

# 插件架构技能

## 概述

用于规划和设计 AI-Assistant 项目的整体架构和功能布局。

## 核心功能

### 1. 结构规划

设计项目目录结构：

```
AI-Assistant/
├── .claude/              # 项目级配置
│   ├── skills/           # 项目技能
│   ├── agents/           # 项目代理
│   ├── commands/         # 项目命令
│   ├── contexts/         # 上下文
│   └── settings.json     # 项目设置
├── skills/               # 插件级技能
├── agents/               # 插件级代理
├── commands/             # 插件级命令
├── hooks/                # 钩子配置
├── contexts/             # 上下文配置
├── rules/                # 代码规范
├── docs/                 # 文档
│   ├── claude-code/      # Claude Code 参考
│   └── plans/            # 实施计划
└── scripts/              # 脚本
```

### 2. 依赖管理

管理技能/代理之间的依赖关系：

```
brainstorming → writing-plans → executing-plans → code-review → update-blueprint
                                                    ↓
                                            verification-before-completion
```

### 3. 新功能设计

设计新功能的工作流：

1. **需求分析**：理解要做什么
2. **架构设计**：确定数据结构、API、组件
3. **依赖规划**：确定依赖项
4. **实施计划**：分解为可执行步骤
5. **验证策略**：确定测试方案

### 4. 整合建议

结合 superpowers 和 everything-claude-code 的最佳实践：

| 来源 | 优势 | 可借鉴内容 |
|------|------|------------|
| superpowers | 完整的开发流程 | brainstorming → planning → execution |
| everything-claude-code | 丰富的 agents | security-reviewer, architect, tdd-guide |

## 当前架构

### 已有的配置

| 类型 | 数量 | 说明 |
|------|------|------|
| Skills | 12 | 开发辅助技能 |
| Agents | 4 | 专业代理 |
| Commands | 5 | 斜杠命令 |
| Hooks | 2 | 会话钩子 |
| Contexts | 2 | 上下文 |

### 技能工作流

```
需求阶段: discuss → interaction → blueprint
            ↓
规划阶段: brainstorming → writing-plans
            ↓
执行阶段: executing-plans → tdd-guide
            ↓
验证阶段: code-review → verification-before-completion
            ↓
完成阶段: update-blueprint
```

## 规划流程

### 1. 需求收集

- 理解目标
- 确定范围
- 识别约束

### 2. 架构设计

- 设计目录结构
- 确定组件关系
- 规划数据流

### 3. 实施规划

- 分解任务
- 确定依赖
- 制定时间表

### 4. 验证方案

- 测试策略
- 质量标准
- 验收条件

## 参考资源

- superpowers: `/Users/huangzhixin/Desktop/Code/AI/superpowers/`
- everything-claude-code: `/Users/huangzhixin/Desktop/Code/AI/everything-claude-code/`
- Claude Code 规范: `docs/claude-code/reference.md`

## 检查清单

### 规划前
- [ ] 明确目标
- [ ] 了解约束
- [ ] 确定范围

### 规划时
- [ ] 设计合理结构
- [ ] 管理依赖关系
- [ ] 考虑扩展性

### 规划后
- [ ] 文档化架构
- [ ] 更新蓝图
- [ ] 验证可行性

## 常用分析

### 对比分析
- 当前 vs 参考项目
- 差距识别
- 优化建议

### 依赖分析
- 技能依赖链
- 执行顺序
- 瓶颈识别

### 风险分析
- 技术风险
- 依赖风险
- 资源风险

## 命名规范

| 类型 | 位置 | 说明 |
|------|------|------|
| 项目级 | `.claude/` | 仅当前项目可用 |
| 插件级 | 根目录 | 插件启用时可用 |

## 最佳实践

1. **保持简洁**：技能/代理专注于单一职责
2. **清晰依赖**：明确技能之间的调用关系
3. **文档完善**：每个配置都有清晰描述
4. **持续优化**：定期检查和更新配置
