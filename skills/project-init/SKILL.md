---
name: project-init
description: "项目初始化 - 为当前项目初始化 Claude Code 配置，注入管家和 Subagent 上下文"
user-invocable: true
---

# 项目初始化

> 为当前项目初始化 Claude Code 配置，注入管家技能上下文

---

## 功能

1. **检查现有配置** - 查看当前项目是否已有 `.claude/CLAUDE.md`
2. **初始化/更新配置** - 注入管家和 Subagent 相关上下文
3. **生成配置** - 创建完整的项目级 Claude 配置

---

## 预定义内容

初始化时注入以下内容到 `.claude/CLAUDE.md`：

### 1. 管家（星星）说明

```markdown
## 智能管家（星星）

> 项目智能助手，调用管家处理复杂任务

### 使用方式

通过以下方式调用管家：
- 直接说"星星，帮我xxx"
- 使用 Skill：`ai-assistant:coordinator`

### 管家职责

- 接收任务，分析需求
- 制定计划，调度执行
- 监控进度，闭环管理
```

### 2. Subagent 角色说明

```markdown
## Subagent 角色

管家可调度的 Subagent：

| 角色 | 用途 |
|------|------|
| thinking-coach | 思维教练 - 厘清思路 |
| code-analysis | 代码分析 - 系统分析 |
| debugging | 调试专家 - 定位修复 bug |
| security-review | 安全审查 |
| ... | ... |
```

---

## 【强制】执行步骤

### 步骤 1：检查项目目录

```
1. 获取当前工作目录（pwd）
2. 检查是否存在 .claude/CLAUDE.md
   → 存在 → 读取现有内容
   → 不存在 → 创建新文件
```

### 步骤 2：检查 .claude 目录

```
1. 检查 .claude/ 目录是否存在
   → 不存在 → 创建目录
2. 确认 CLAUDE.md 路径：<project>/.claude/CLAUDE.md
```

### 步骤 3：生成/更新配置

```
如果文件不存在：
1. 生成完整的初始配置
2. 写入 .claude/CLAUDE.md

如果文件存在：
1. 读取现有内容
2. 检查是否已包含"智能管家"章节
   → 已包含 → 提示"已初始化，跳过"
   → 不包含 → 追加管家相关内容
3. 写入更新后的内容
```

### 步骤 4：确认结果

```
1. 读取生成的配置文件
2. 向用户确认初始化完成
3. 提示如何使用管家
```

---

## 输出

- 文件：`{当前项目}/.claude/CLAUDE.md`
- 状态：初始化成功/已存在/失败

---

## 使用示例

```
用户：帮我初始化项目配置

【Skill】项目初始化
    ↓
【检查】当前项目 .claude/CLAUDE.md
    ↓
【生成】注入管家和 Subagent 上下文
    ↓
【完成】配置已初始化到 .claude/CLAUDE.md
```
