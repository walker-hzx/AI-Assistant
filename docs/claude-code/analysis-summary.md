# Claude Code 官方文档分析汇总

> 分析日期：2026-02-25
> 来源：docs/claude-code-extracted/

---

## 一、核心概念图谱

```
Claude Code 扩展机制
├── Skills（技能）
│   ├── 定义：扩展 Claude 能力的指令集
│   ├── 调用：/skill-name 或自动触发
│   └── 优先级：高于同名 Commands
│
├── Sub-agents（子代理）
│   ├── 定义：专业化任务执行单元
│   ├── 特点：独立 context + 自定义 prompt + 工具限制
│   └── 用途：保留 context、约束工具、控制成本
│
├── Agent Teams（团队协作）
│   ├── 定义：多个 Claude 实例协同工作
│   ├── 特点：独立会话 + 直接通信 + 共享任务列表
│   └── 用途：并行探索、复杂任务、多角度分析
│
├── Commands（命令）
│   ├── 定义：快捷入口
│   └── 注意：Skill 优先于同名 Command
│
├── Hooks（钩子）
│   └── 作用：自动化工作流
│
└── Plugins（插件）
    └── 作用：打包分发配置
```

---

## 二、各组件详细说明

### 2.1 Skills（技能）

**定义**：扩展 Claude 能力的指令集，定义在 `SKILL.md` 文件中。

**核心字段**：

| 字段 | 说明 | 示例 |
|------|------|------|
| `name` | 技能名称，用于 /name 调用 | `brainstorming` |
| `description` | 描述，决定何时自动加载 | "需求分析技能" |
| `model` | 指定模型 | `sonnet` / `opus` / `haiku` |
| `user-invocable` | 是否在 / 菜单可见 | `true` / `false` |
| `disable-model-invocation` | 是否禁止自动触发 | `true` / `false` |
| `allowed-tools` | 允许的工具列表 | `[Read, Grep]` |
| `context` | 执行模式 | `fork`（子代理中运行）|
| `agent` | 配合 context: fork 使用 | `Explore` |

**存储位置**：

| 位置 | 作用域 |
|------|---------|
| `~/.claude/skills/` | 全局用户 |
| `.claude/skills/` | 项目级 |
| `<plugin>/skills/` | 插件级 |

**调用方式**：
- 直接调用：`/skill-name`
- 自动触发：根据 description 决定

**重要特性**：
- Skill 优先于同名 Command
- 支持 `$ARGUMENTS` 动态参数
- 支持 `!`command`` 动态注入

---

### 2.2 Sub-agents（子代理）

**定义**：专业化任务执行单元，运行在独立 context 中。

**核心价值**：

| 价值 | 说明 |
|------|------|
| **保留 Context** | 探索和实现不污染主对话 |
| **约束工具** | 限制某些工具的使用 |
| **跨项目复用** | 用户级配置可在所有项目使用 |
| **专业化** | 针对特定领域的系统提示 |
| **成本控制** | 路由到更便宜的模型（如 Haiku）|

**内置 Sub-agents**：

| Agent | Model | 用途 |
|-------|-------|------|
| Explore | Haiku | 代码搜索、只读探索 |
| Plan | 继承 | 计划模式研究 |
| General-purpose | 继承 | 复杂多步骤任务 |
| Bash | 继承 | 终端命令 |

**创建方式**：
- 手动创建：`~/.claude/agents/<name>.md`
- 命令创建：`/agents`

---

### 2.3 Agent Teams（团队协作）

**定义**：多个 Claude 实例协同工作，实验性功能。

**启用方式**：
```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

**最佳使用场景**：

| 场景 | 说明 |
|------|------|
| 并行探索 | 多角度同时研究 |
| 新模块开发 | 队友各自独立部分 |
| 竞争假设调试 | 并行测试不同理论 |
| 跨层协调 | 前端+后端+测试 |

**不适合场景**：
- 顺序任务
- 同一文件编辑
- 有很多依赖的工作

**与 Sub-agents 对比**：

| 特性 | Sub-agent | Agent Team |
|------|-----------|------------|
| Context | 独立 | 各自独立 |
| 通信 | 仅报告主代理 | 直接相互通信 |
| 协调 | 主代理管理 | 共享任务列表 |
| 成本 | 较低 | 较高 |
| 适合 | 专注任务 | 复杂协作 |

---

### 2.4 Commands（命令）

**定义**：快捷入口，定义在 `commands/<name>.md`。

**注意**：
- 文件名即命令名
- Skill 优先于同名 Command
- 支持 `disable-model-invocation`

---

### 2.5 Hooks（钩子）

**作用**：自动化工作流

**事件类型**：

| 事件 | 说明 |
|------|------|
| `SessionStart` | 会话开始 |
| `Stop` | 会话结束 |
| `ToolUseStart` | 工具执行前 |
| `ToolUseEnd` | 工具执行后 |
| `SubagentStart` | 子代理开始 |
| `SubagentStop` | 子代理结束 |

**类型**：
- `command`：执行 bash 命令
- `prompt`：LLM 评估

---

### 2.6 Plugins（插件）

**作用**：打包和分发配置

**必需文件**：
- `plugin.json` / `.claude-plugin/manifest.json`

---

## 三、对插件项目的优化建议

> **更新于 2026-03-04**：以下建议已根据 v3.0.0 重构结果更新

### 3.1 当前配置分析

| 配置 | 数量 | 说明 |
|------|------|------|
| Skills | 30 | 核心能力（含指南类）|
| Commands | 12 | 快捷入口 |
| Agents | 8 | 6+2 角色（6核心+2可选）|
| Teams | 6 | 团队配置 |

### 3.2 优化建议

#### ~~建议 1：删除重复的 Agents~~ ✅ 已完成（v3.0.0）

已完成重构：17角色 → 6+2角色（analyst, executor, tester, reviewer, researcher, debugger + skeptics, ui-ux-reviewer）

#### ~~建议 2：补齐 Commands~~ ✅ 已完成（v3.0.0）

当前 Commands（12个）：`discuss`, `plan`, `review`, `thinking`, `debugging`, `verification`, `executing-plans`, `team-generator`, `docs-sync`, `learn-concept`, `security-review`, `test-planner`

#### ~~建议 3：标准化 Skills Metadata~~ ✅ 已完成（2026-03-04）

已完成：
- 所有 Skills 补齐 `model` 字段
- 所有 Skills 明确设置 `user-invocable`（用户可调用 vs 内部使用）
- 修复 `project-researcher` 的 `model: inherit` → `model: sonnet`
- 修复 `e2e-tester` name 字段不匹配问题
- `coordinator` 补齐 `model: sonnet`

#### 建议 4：充分利用 Teams

已配置 6 个 Teams，符合官方最佳实践：
- requirements-incubation
- requirements-review
- development
- debugging
- code-review
- code-analysis

**待验证**：Teams 依赖实验性功能 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`，建议验证可用性。

#### 建议 5：为只读 Agents 添加工具约束（新） ✅ 已完成（2026-03-04）

已为以下 agents 添加 `allowed-tools` 约束：
- `analyst`：Read, Grep, Glob, semantic_search
- `researcher`：Read, Grep, Glob, semantic_search, fetch_webpage
- `reviewer`：Read, Grep, Glob, semantic_search
- `skeptics`：Read, Grep

---

## 四、学习总结

### 4.1 关键认知

1. **Skill 是核心**：所有能力都应该通过 Skill 定义
2. **Command 是入口**：方便用户调用，但不必须
3. **Agent 是执行**：内部使用，不需要暴露给用户
4. **Team 是协作**：复杂任务才需要团队协作

### 4.2 最佳实践

| 场景 | 推荐方式 |
|------|---------|
| 定义能力 | Skill |
| 快捷调用 | Command（补齐高频）|
| 内部执行 | Sub-agent（需要工具限制时）|
| 多实例协作 | Agent Team（复杂任务）|
| 自动化 | Hooks |

### 4.3 架构选择

```
简单场景（你当前）：
用户 → Skill → 执行
（不需要 Agent/Team）

复杂场景：
用户 → Agent Team → 多个 Skill/Agent → 结果汇总
```

---

## 五、后续行动

| 优先级 | 行动 | 状态 |
|--------|------|------|
| P1 | 删除 3 个重复 Agents | ✅ 已完成（v3.0.0 重构）|
| P2 | 补齐高频 Commands（12个）| ✅ 已完成 |
| P3 | 标准化 Skills metadata | ✅ 已完成 |
| P4 | 为只读 Agents 加 allowed-tools | ✅ 已完成 |
| P5 | 优化 Commands 描述文字 | ✅ 已完成 |
| P6 | 验证 Teams 功能 | ⏳ 待验证 |

---

## 六、相关文档

- 爬取原始文档：`docs/claude-code/`
- 提取后文档：`docs/claude-code-extracted/`
- 爬取脚本：`scripts/fetch-docs/fetch-claude-code-docs.py`
- 提取脚本：`scripts/fetch-docs/extract-claude-code-content.py`
