---
name: project-analyzer
description: Claude Code 插件项目分析专家。分析 GitHub 上的插件项目，生成对比报告，找出当前项目的优化点。
disable-model-invocation: false
---

# 项目分析专家

分析 Claude Code 插件项目，生成对比报告，并提供优化建议。

## 使用场景

- 想了解其他插件项目的设计思路
- 想找出当前项目的不足和优化点
- 想学习其他项目的最佳实践

## 使用方法

用户提供 GitHub 仓库地址，然后：

1. 克隆项目到临时目录
2. 分析项目结构和配置
3. 与当前项目对比
4. 生成优化建议报告

## 分析流程

### Step 1: 克隆项目

```bash
# 克隆到临时目录
cd /tmp
git clone [仓库地址] project-analysis
cd project-analysis
```

### Step 2: 结构分析

检查项目的目录结构：

```bash
ls -la
find . -type f -name "*.md" | head -20
```

识别关键文件和目录：
- `.claude-plugin/plugin.json` - 插件清单
- `agents/` - Agent 配置
- `skills/` - Skill 配置
- `commands/` - 命令配置
- `hooks/` - Hook 配置
- `README.md` - 项目文档

### Step 3: 配置分析

#### 3.1 分析 plugin.json

读取并分析插件配置文件：

```json
{
  "name": "xxx",
  "version": "1.0.0",
  "agents": [...],
  "skills": [...],
  "commands": [...]
}
```

**检查项：**
- 字段是否完整
- 版本管理
- Agent/Skill 数量

#### 3.2 分析 Agents

读取每个 Agent 文件：

```bash
ls agents/
```

分析每个 Agent：
- name 和 description
- tools 配置
- model 选择
- prompt 质量

**检查项：**
- 是否有清晰的 description（支持 proactively 触发）
- tools 是否合理（最小权限原则）
- model 选择是否合适
- prompt 内容是否有深度

#### 3.3 分析 Skills

读取每个 Skill 文件：

```bash
ls skills/
```

分析每个 Skill：
- 触发方式（name）
- description 是否清晰
- disable-model-invocation 设置
- 内容质量

**检查项：**
- 是否有多个 Skills
- Skill 设计是否有亮点
- 是否有独特的模式

#### 3.4 分析 Commands

```bash
ls commands/
```

检查命令设计：
- 触发方式
- 参数处理

### Step 4: 对比当前项目

读取当前项目配置：

```bash
# 当前项目的 agents
ls agents/

# 当前项目的 skills
ls skills/
```

**对比维度：**

| 维度 | 分析项 |
|------|--------|
| **数量对比** | Agent/Skill 数量差距 |
| **质量对比** | prompt 深度、工具配置 |
| **完整性** | 是否缺少某些能力 |
| **最佳实践** | 是否遵循官方推荐模式 |

### Step 5: 生成报告

生成结构化的分析报告：

```markdown
# 项目分析报告：[项目名称]

## 项目概述
- **GitHub 地址**：[URL]
- **Star 数**：[数量]
- **主要功能**：[描述]

## 目录结构
```
[目录树]
```

## 配置分析

### plugin.json
| 字段 | 值 | 当前项目对比 |
|------|-----|-------------|
| name | xxx | 当前：xxx |
| version | xxx | 当前：xxx |
| agents | N 个 | 当前：N 个 |
| skills | N 个 | 当前：N 个 |

### Agents 分析
| Agent | 功能 | 亮点 | 可借鉴点 |
|-------|------|------|----------|
| xxx | xxx | xxx | xxx |

### Skills 分析
| Skill | 触发方式 | 特点 | 可借鉴点 |
|-------|----------|------|----------|
| xxx | xxx | xxx | xxx |

## 与当前项目对比

### 优势（当前项目可借鉴）
1. **xxx**：xxx
2. **xxx**：xxx

### 当前项目的优势
1. **xxx**：xxx
2. **xxx**：xxx

### 差距分析
- **Agent 数量**：当前 N 个 vs 目标 N 个
- **Skill 覆盖**：当前 xxx vs 目标 xxx
- **配置完整性**：xxx

## 优化建议

### 高优先级
1. **建议 1**：xxx
   - 理由：xxx
   - 参考：xxx

### 中优先级
1. **建议 2**：xxx

### 低优先级
1. **建议 3**：xxx

## 总结
[总结分析结论]
```

## 输出要求

1. **保存报告**到：`docs/plans/YYYY-MM-DD-[project-name]-analysis.md`
2. **不要修改**任何现有文件
3. **不要创建**任何新文件到目标项目
4. 只做**只读分析**

## 注意事项

- 分析过程保持**只读**，不修改任何文件
- 如果项目较大，可以选择性分析关键文件
- 重点关注**可借鉴的点**，而非盲目复制
- 结合**当前项目特点**提出建议
