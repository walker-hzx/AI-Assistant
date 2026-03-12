# AI-Assistant 项目级配置

> 项目级 Claude Code 配置

## 项目信息

- **项目类型**: Claude Code 插件
- **用途**: 个人开发助手
- **技术栈**: Vue 3 + Python FastAPI

## 架构说明

### 直达自治模式（v5.0 — 无 Coordinator）

**核心理念**：去掉中间调度层，每个命令直达对应 Agent 或加载对应 Skill。

#### 命令路由

**Fork 到 Agent**（独立子会话，适合明确的单一任务）：
- `/review` → reviewer（代码审查）
- `/debugging` → debugger（Bug 定位修复）
- `/security-review` → reviewer（安全审查）
- `/thinking` → analyst（思维教练）
- `/verification` → tester（功能验证）
- `/test-planner` → tester（测试设计）
- `/docs-sync` → scout（文档同步）
- `/learn-concept` → researcher（学习概念）
- `/implement` → executor（实现功能）
- `/refactor` → executor（重构代码）
- `/analyze` → researcher（代码/方案分析）
- `/docs` → researcher（编写文档）

**加载 Skill 到主线程**（需要多角色编排，主线程可用 Task() 调度）：
- `/plan` → writing-plans skill
- `/executing-plans` → executing-plans skill
- `/team-generator` → team-generator skill
- `/discuss` → brainstorming skill

#### 9 个角色
| 角色 | 模型 | 记忆 | 职责 |
|------|------|------|------|
| analyst | opus | project | 需求分析、策略制定、思维引导 |
| executor | inherit | project | 代码实现、功能开发、代码重构 |
| tester | inherit | project | 测试设计与执行 |
| reviewer | inherit | project | 代码审查、安全审查 |
| researcher | inherit | project | 代码分析、技术调研、文档编写 |
| debugger | inherit | project | Bug 定位和修复 |
| scout | haiku | — | 外部资源获取 |
| skeptics | inherit | — | 建设性质疑（可选） |
| ui-ux-reviewer | inherit | — | UI/UX 审查（可选） |

---

## 配置目录

- `skills/` - 技能配置
- `agents/` - Agent 定义
- `commands/` - 命令配置
- `hooks/` - 钩子配置
- `contexts/` - 上下文配置
- `rules/` - 代码规范

---

## 开发规范

### 工作原则

1. **命令直达** - 每个命令有明确对应的 Agent 或 Skill，无需中间调度
2. **上下文驱动** - 信息在会话中流转，只在复杂任务创建文档
3. **闭环执行** - 每轮执行后检查结果，迭代调整
4. **主线程编排** - 需要多角色协作时，主线程用 Task() 直接调度各 Agent

### 文档产出

| 任务档位 | 文档 |
|----------|------|
| S 档 | 无 |
| M 档 | TodoWrite 跟踪 |
| L 档 | `docs/plans/<task>-plan.md` |

---

## 角色列表

| 角色 | 职责 |
|------|------|
| analyst | 需求理解、问题分析、策略制定 |
| executor | 代码实现、功能开发 |
| tester | 测试设计、执行、功能验证 |
| reviewer | 代码审查、安全审查、质量评估 |
| researcher | 代码分析、项目调研、文档查阅 |
| debugger | Bug 定位和修复 |
| skeptics | 建设性质疑（可选） |
| ui-ux-reviewer | UI/UX 审查（可选） |

---

## 质量要求

- 测试覆盖率: 80%+
- 代码审查: 所有重要变更
- 验证通过才能合并

---

## 思考习惯

1. **查文档作为参考** - 遇到需求时，如果有相关文档可以参考，先查文档再分析，不要凭猜测
2. **记住用户的建议** - 用户给出的调整建议，需要应用到后续类似场景
3. **理解错误并调整** - 不是硬编码规则，而是理解后自然应用
4. **区分配置描述** - 注意区分"插件项目配置"和"开发时的配置"
5. **深层次分析后再优化** - 不要只基于用户描述的内容优化，用户说一个例子要分析这类问题的本质
6. **主动揣测用户意图** - 用户说一个问题要想还有什么相关问题，主动检查同类而不是等用户说
7. **遇到模块要扫描完整** - 遇到一个模块的问题，要主动扫描完整相关代码，而不是只修一个问题
8. **先确定范围再行动** - 每次做决定前，先想清楚是在哪个范围：插件项目（skills/）还是项目配置（.claude/）
9. **先问目的再回应** - 用户提需求时，先问核心目的是什么，不要只听表面需求就做
10. **完成前必检** - 完成任何任务后，必须主动检查：需求对照、历史遗留问题、接口错误
11. **执行必留痕** - 执行计划时记录每个阶段做了什么，保存到执行日志供后续分析
12. **思维引导** - 用户提需求或想法时，主动分析是否清晰完整，追问深化，提示盲点
13. **阶段门控** - 前一阶段未完成（需求未确认、计划未确认）不得进入下一阶段
14. **历史问题检查** - 执行前必须查阅 `docs/plans/history-checklist.md`，避免重复犯错
15. **实现前评估** - 写代码前先评估：边界条件、异常情况、依赖关系、测试策略
16. **测试覆盖检查** - 测试不只是跑通，必须检查边界条件、异常场景是否覆盖
17. **证据化验收** - 每项需求实现必须提供代码位置作为证据，前端功能必须提供截图
18. **需求状态检查** - 制定计划前必须读取 `docs/requirements/README.md`，只基于当前确认需求，忽略已作废需求
19. **需求作废标记** - 当讨论新需求时，如果老需求不再需要，必须标记为"已作废"，不能当作"功能缺失"
20. **蓝图更新** - 完成功能后更新 `docs/蓝图.md`，记录当前项目状态
21. **深度理解** - 每次接收任务时，先思考用户真正想要什么，不要只处理字面意思。有不确定的地方先理解清楚再行动

---

## 文件操作范围限制

> 所有文件操作默认仅限当前项目目录

### 核心原则

- **Read 工具**：无限制（可读取任意目录）
- **Write/Edit/Bash**：仅限当前项目目录
- **Glob/Grep**：默认仅搜索当前项目目录

### 具体规则

1. 所有文件操作（Glob、Grep、Read、Edit、Write、Bash）默认仅限当前项目目录
2. 当前项目目录通过 Claude Code 的 PWD（当前工作目录）获取
3. 操作外部目录前必须获得用户明确授权

### 示意

```
当前项目：/path/to/project

| 工具 | 项目目录内 | 项目目录外 |
|------|-----------|-----------|
| Read | ✅ 允许 | ✅ 允许 |
| Glob | ✅ 允许 | ❌ 默认禁止 |
| Grep | ✅ 允许 | ❌ 默认禁止 |
| Edit | ✅ 允许 | ❌ 禁止 |
| Write | ✅ 允许 | ❌ 禁止 |
| Bash | ✅ 允许 | ❌ 禁止 |

例外：用户明确授权后可操作外部目录
```

---

## 沟通约定

| 描述 | 指代 |
|------|------|
| 插件项目配置的问题 | 整个 AI-Assistant 项目（skills/, hooks/, agents/ 等所有插件配置） |
| 开发时的配置 | .claude/ 目录 |

> 约定原因：避免将插件配置和项目配置搞混

---

## 相关文档

- 完整规范: `docs/claude-code/reference.md`
- 项目蓝图: `docs/蓝图.md`
- 开发计划: `docs/plans/`
