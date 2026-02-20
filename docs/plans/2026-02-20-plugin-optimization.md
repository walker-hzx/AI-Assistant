# AI-Assistant 插件优化计划

> 基于 Claude Code 官方文档、superpowers 和 everything-claude-code 的分析

## 当前状态

### 已有的配置

| 类型 | 数量 | 文件 |
|------|------|------|
| Skills | 5 | `skills/*/SKILL.md` |
| Commands | 3 | `commands/*.md` |
| Agents | 1 | `agents/planner.md` |
| Hooks | 1 | `hooks/hooks.json` |
| Rules | 2 | `rules/*.md` |

### 问题分析

1. **Skills 格式** - 部分已有正确的 YAML frontmatter
2. **Agents** - planner.md 已修复
3. **缺少** - 缺少更多实用的 skills 和 agents
4. **缺少** - 缺少 contexts 目录
5. **需要优化** - hooks 配置

---

## 优化方案

### Phase 1: 修复现有格式 (10 分钟)

#### Task 1.1: 验证所有 Skills 格式

```bash
# 检查 skills 是否有正确的 frontmatter
```

**文件**: `skills/*/SKILL.md`

确保所有 skills 都有正确的 YAML frontmatter：
```yaml
---
name: skill-name
description: 描述
---
```

#### Task 1.2: 完善 planner Agent

**文件**: `agents/planner.md`

添加完整的规划流程说明，参考 everything-claude-code 的 planner。

### Phase 2: 添加核心 Skills (30 分钟)

#### Task 2.1: 添加 brainstorming Skill

从 superpowers 复制或创建类似版本。

**文件**: `skills/brainstorming/SKILL.md`

#### Task 2.2: 添加 TDD Skill

**文件**: `skills/tdd-guide/SKILL.md`

参考 everything-claude-code 的 tdd-guide agent。

#### Task 2.3: 添加 debugging Skill

**文件**: `skills/debugging/SKILL.md`

#### Task 2.4: 添加 code-review Skill

**文件**: `skills/code-review/SKILL.md`

### Phase 3: 添加 Commands (15 分钟)

#### Task 3.1: 添加更多 Commands

当前已有：
- `/discuss` - 需求讨论
- `/interaction` - 交互描述
- `/blueprint` - 蓝图更新

可以添加：
- `/plan` - 制定计划
- `/review` - 代码审查

### Phase 4: 完善 Agents (20 分钟)

#### Task 4.1: 添加 tdd-guide Agent

**文件**: `agents/tdd-guide.md`

```yaml
---
name: tdd-guide
description: TDD 专家，确保测试先行
tools: [Read, Write, Edit, Bash, Grep]
model: sonnet
---
```

#### Task 4.2: 添加 code-reviewer Agent

**文件**: `agents/code-reviewer.md`

#### Task 4.3: 添加 security-reviewer Agent

**文件**: `agents/security-reviewer.md`

### Phase 5: 完善 Hooks (15 分钟)

#### Task 5.1: 配置 SessionStart Hook

**文件**: `hooks/hooks.json`

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume",
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

### Phase 6: 添加 Contexts (10 分钟)

#### Task 6.1: 创建 contexts 目录

**文件**: `contexts/dev.md`

```markdown
# Development Context

Mode: Active development
Focus: Implementation, coding, building features

## Behavior
- Write code first, explain after
- Prefer working solutions over perfect solutions
- Run tests after changes
- Keep commits atomic
```

---

## 详细任务清单

### 任务 1: 验证 Skills 格式
- [ ] 检查 `skills/discuss-requirements/SKILL.md`
- [ ] 检查 `skills/describe-interaction/SKILL.md`
- [ ] 检查 `skills/update-blueprint/SKILL.md`
- [ ] 检查 `skills/frontend-guide/SKILL.md`
- [ ] 检查 `skills/backend-guide/SKILL.md`

### 任务 2: 完善 planner Agent
- [ ] 添加完整的规划流程
- [ ] 添加实现步骤模板
- [ ] 添加风险评估模板

### 任务 3: 添加 brainstorming Skill
- [ ] 创建 `skills/brainstorming/SKILL.md`
- [ ] 添加检查清单
- [ ] 添加设计流程

### 任务 4: 添加 tdd-guide Agent
- [ ] 创建 `agents/tdd-guide.md`
- [ ] 定义 Red-Green-Refactor 流程
- [ ] 定义测试覆盖率要求

### 任务 5: 添加 code-reviewer Agent
- [ ] 创建 `agents/code-reviewer.md`
- [ ] 定义审查清单
- [ ] 定义问题级别

### 任务 6: 配置 Hooks
- [ ] 更新 `hooks/hooks.json`
- [ ] 创建 `hooks/session-start.sh`

### 任务 7: 创建 Contexts
- [ ] 创建 `contexts/dev.md`
- [ ] 创建 `contexts/review.md`

---

## 依赖关系

```
Phase 1 (格式修复)
    ↓
Phase 2 (核心 Skills)
    ↓
Phase 3 (Commands)
    ↓
Phase 4 (Agents)
    ↓
Phase 5 (Hooks)
    ↓
Phase 6 (Contexts)
```

---

## 参考资源

- superpowers: https://github.com/superpowersrc/superpowers
- everything-claude-code: https://github.com/anthropics/everything-claude-code
- Claude Code 文档: `docs/claude-code/reference.md`
