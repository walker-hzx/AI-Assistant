# Claude Code Plugin 全面优化计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 全面优化 AI-Assistant Claude Code 插件配置，包括 Hooks 增强、Skills 配置优化、新技能补充

**Architecture:** 基于 Claude Code 官方文档最佳实践，优化现有配置并补充缺失功能

**Tech Stack:** YAML, JSON, Shell Scripts

---

## 任务总览

| 任务 | 描述 | 优先级 |
||
| 1------|------|-------- | 添加 ToolUseStart/ToolUseEnd Hooks | P0 |
| 2 | 添加 PreToolUse 权限验证 Hook | P0 |
| 3 | 为关键 Skills 添加配置参数 | P1 |
| 4 | 验证所有配置格式正确性 | P1 |
| 5 | 更新 analysis.md 文档 | P2 |

---

## Task 1: 添加 ToolUseStart Hook

**Files:**
- Modify: `hooks/hooks.json`
- Create: `hooks/tool-use-logger.sh`

**Step 1: 创建工具使用日志 Hook 脚本**

```bash
#!/bin/bash
# hooks/tool-use-logger.sh
# 记录工具使用日志

TOOL_NAME="$1"
ARGS="$2"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

echo "[$TIMESTAMP] Tool: $TOOL_NAME" >> "${CLAUDE_PLUGIN_ROOT}/logs/tool-use.log"
```

**Step 2: 更新 hooks.json 添加 ToolUseStart**

```json
{
  "hooks": {
    "ToolUseStart": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/tool-use-logger.sh ${tool_name} ${tool_input}",
            "async": true,
            "description": "Log tool usage"
          }
        ]
      }
    ]
  }
}
```

**Step 3: 合并到现有 hooks.json**

Run: 手动合并两个配置块
Expected: hooks.json 包含 SessionStart, Stop, ToolUseStart 三个事件

**Step 4: Commit**

```bash
git add hooks/hooks.json hooks/tool-use-logger.sh
git commit -m "feat: add ToolUseStart hook for logging"
```

---

## Task 2: 添加 PreToolUse 权限验证 Hook

**Files:**
- Create: `hooks/permission-guard.sh`

**Step 1: 创建权限验证脚本**

```bash
#!/bin/bash
# hooks/permission-guard.sh
# PreToolUse 钩子 - 在危险操作前验证

TOOL_NAME="$1"
COMMAND="$2"

# 危险命令黑名单
DANGEROUS_COMMANDS=("rm -rf" "git push --force" "DROP TABLE")

for cmd in "${DANGEROUS_COMMANDS[@]}"; do
  if echo "$COMMAND" | grep -q "$cmd"; then
    echo "BLOCKED: Dangerous command detected: $cmd"
    exit 1
  fi
done

exit 0
```

**Step 2: 更新 hooks.json 添加 PreToolUse**

Run: 在 hooks.json 中添加 PreToolUse 事件
Expected: hooks.json 包含 4 个事件

**Step 3: Commit**

```bash
git add hooks/permission-guard.sh hooks/hooks.json
git commit -m "feat: add PreToolUse permission guard"
```

---

## Task 3: 为关键 Skills 添加配置参数

**Files:**
- Modify: `skills/tdd-guide/SKILL.md`
- Modify: `skills/brainstorming/SKILL.md`
- Modify: `skills/debugging/SKILL.md`

**Step 1: 更新 tdd-guide 添加 model 和 allowed-tools**

```yaml
---
name: tdd-guide
description: Test-driven development guide
model: sonnet
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---
```

**Step 2: 更新 brainstorming 添加 user-invocable**

```yaml
---
name: brainstorming
description: 将想法转化为设计
user-invocable: true
---
```

**Step 3: Commit**

```bash
git add skills/tdd-guide/SKILL.md skills/brainstorming/SKILL.md
git commit -m "feat: add model and allowed-tools to key skills"
```

---

## Task 4: 验证所有配置格式正确性

**Files:**
- Verify: `skills/*/SKILL.md`
- Verify: `agents/*.md`
- Verify: `commands/*.md`
- Verify: `hooks/hooks.json`

**Step 1: 验证 Skills 格式**

Run: `grep -L "^---\nname:" skills/*/SKILL.md`
Expected: 无输出（所有文件都有 name）

**Step 2: 验证 Agents 格式**

Run: `grep -L "^---\nname:" agents/*.md`
Expected: 无输出

**Step 3: 验证 Commands 格式**

Run: `grep -L "^---\ndescription:" commands/*.md`
Expected: 无输出

**Step 4: 验证 hooks.json 格式**

Run: `python3 -m json.tool hooks/hooks.json > /dev/null`
Expected: 无错误

**Step 5: Commit**

```bash
git commit -m "chore: verify all config formats"
```

---

## Task 5: 更新 analysis.md 文档

**Files:**
- Modify: `docs/claude-code/analysis.md`

**Step 1: 更新配置统计**

```markdown
| 类型 | 数量 | 格式正确 |
|------|------|----------|
| Skills | 14 | ✅ |
| Agents | 6 | ✅ |
| Commands | 5 | ✅ |
| Hooks | 4 | ✅ |
```

**Step 2: 添加新增功能说明**

```markdown
### 新增功能

- ToolUseStart Hook: 工具使用日志
- PreToolUse Hook: 权限验证
```

**Step 3: Commit**

```bash
git commit -m "docs: update analysis.md with new features"
```

---

## 实施顺序

1. Task 1 → Task 2 (先添加 Hooks)
2. Task 3 → Task 4 (优化 Skills 并验证)
3. Task 5 (最后更新文档)

---

## Plan complete and saved to `docs/plans/2026-02-20-claude-code-plugin-optimization.md`

Two execution options:

1. **Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

2. **Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

Which approach?
