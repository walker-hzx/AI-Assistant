# Changelog

All notable changes to this project will be documented in this file.

## [5.1.0] - 2026-03-12

### Added

#### Agent 强化与能力补全 (v5.1)

**主要变更**：
- **新增直达命令**：
  - `/implement`：executor 专属实现入口，支持不经计划直接写代码。
  - `/refactor`：executor 专属重构入口，集成安全重构技能。
  - `/analyze`：researcher 专属分析入口，深入调研代码和方案。
  - `/docs`：researcher 专属文档编写入口，从代码生成 README/API 文档。
- **技能武器库升级**：
  - `executor`：新增 `refactoring` (重构), `vue3-vite-guide`, `python-fastapi-guide` (技术栈规范) 技能。
  - `researcher`：新增 `doc-writing` (文档编写), `web-researcher` (外部搜索) 技能。
  - `analyst`：新增 `brainstorming` (头脑风暴) 技能支撑需求分析。
- **命令链路优化**：`/discuss` 指令不再仅是空谈，现在深度加载 `brainstorming` 技能。

## [5.0.0] - 2026-03-12

### Changed

#### 架构大改造 — 直达自治模式 (v5.0 — 无 Coordinator)

**核心理念**：彻底移除中间调度层，通过命令直接触发目标 Agent 或 Skill，消除指令损耗和调度瓶颈。

**主要变更**：
- **移除 Coordinator**：`skills/coordinator/` 已归档，不再由中心调度，改为「分布自治」模式。
- **命令专场化**：
  - `/review` & `/security-review` 直达 `reviewer` Agent。
  - `/debugging` 直达 `debugger` Agent。
  - `/thinking` 直达 `analyst` Agent (Opus 驱动)。
  - `/verification` 直达 `tester` Agent。
  - `/docs-sync` 直达 `scout` Agent (Haiku 驱动)。
- **Agent 强化**：
  - 核心 Agent (analyst, executor, debugger, reviewer, researcher, tester) 开启 `memory: project`，具备跨会话记忆。
  - `analyst` 分配最高权限模型 `opus` 用于深度推理；`scout` 分配 `haiku` 用于快速外部资源采集。
- **主线程编排**：涉及多阶段协作的任务（如 `/plan`, `/executing-plans`）直接加载 Skill 到主线程，利用 `Task()` 进行细粒度编排。

## [4.0.0] - 2026-03-12

### Changed

#### 架构精简分层版 (v4.0)

**主要变更**：
- **Coordinator 瘦身**：SKILL.md 从 973 行精简至 239 行，移除冗余示例，压缩指令。
- **混合路由**：初步引入 `context: fork` 机制，部分核心命令（review, debugging）开始尝试直达 Agent。
- **跨会话记忆**：为 6 个核心 Agent 启用项目级持久化记忆。

## [3.0.5] - 2026-03-06

### Enhanced

#### MVT（最小可行性测试）调试策略

**背景**：修复 bug 反复失败时，缺少系统性的降级排查机制，导致循环修复。

**Coordinator 增强**（`skills/coordinator/SKILL.md`）：
- 新增「修复循环检测与 MVT 降级策略」
- 定义 4 个循环修复信号（同一问题修 2 次未解决、改 A 坏 B、A→B→A 循环、根因不明反复试）
- 命中任一信号强制触发 MVT 降级，禁止继续盲改
- 提供标准 Task 模板给 coordinator 调度 debugger 进入 MVT 模式

**Debugger Agent 增强**（`agents/debugger.md`）：
- 新增「最小可行性测试排查法（MVT 模式）」作为核心调试方法
- 完整五步法：剥离→确认→逐步增加→修复→应用
- 新增循环修复降级原则：同一问题修 2 次仍失败 → 立即切换 MVT

**Debugging Skill 增强**（`skills/debugging/SKILL.md`）：
- 新增完整 MVT 章节，含触发条件表、五步法详解（前后端代码示例）、探针测试写法、输出报告模板
- 原"最小复现"技巧升级为 MVT 章节引用，避免重复

**Executor Agent 增强**（`agents/executor.md`）：
- 意外信号表新增：同一修复第 2 次仍失败 → 建议 coordinator 切换 MVT 排查

**Coordinator ROLES 更新**（`skills/coordinator/ROLES.md`）：
- debugger 调度表新增 MVT 模式场景

## [1.8.0] - 2026-02-26

### Added

#### 角色体系架构（Subagents）

**新增 `.claude-plugin/agents/` 目录**，定义 11 个 Subagents：

**核心角色（线性流程）**：
- requirements-analyst → brainstorming
- planner → writing-plans
- executor → executing-plans
- qa → verification
- code-reviewer → code-review

**辅助角色（按需调用）**：
- coordinator → coordinator
- thinking-coach → thinking-coach
- debugger → debugging
- code-analyst → code-analysis
- security-reviewer → security-review
- test-designer → test-planner

**实现方式**：
- 每个角色是 Claude Code Subagent（Markdown + YAML frontmatter）
- 使用 `skills` 字段预加载对应 Skill 到 Subagent 上下文
- 管家（Coordinator）调度角色执行任务

**文件结构**：
- `.claude-plugin/agents/` - 11 个角色 Subagent 文件
- `.claude-plugin/plugin.json` - 新增 `agents` 字段

**技术实现**：
- Subagent 文件格式：YAML frontmatter + Markdown 系统 prompt
- 预加载 skills：`skills: [brainstorming]` 等
- 继承模型：`model: inherit`

## [1.7.6] - 2026-02-25

### Enhanced

#### thinking-coach 全面重构

**核心定位**：
- 像高手一样给你洞见和方向
- 直接给判断，而不是只给选项
- 每次1-3条建议，让你有机会调整

**使用场景**：
- 问题模糊、方向不明、需求有误
- 思维偏差、视角局限、想被点拨
- 口语整理（帮你整理语音输入）

**核心能力**：
1. 问题厘清 - 帮你把模糊的问题描述清楚
2. 思路纠正 - 指出思维偏在哪，给出正确方向
3. 洞察指出 - 指出你没想到的盲点
4. 主动分析 - 你不清楚的，主动深度分析给方案
5. 口语整理 - 语音输入时帮你整理成清晰文字

**优化内容**：
- 删除过多的框架和模板
- 强调"高手风格"：直接给方向，而不是问用户选哪个
- 限制建议数量：每次最多3条
- 精简行数：657行 → ~330行

### Enhanced

#### writing-plans 优化（精简+减少重复）

- 删除与 verification 重复的"里程碑验收标准"章节（验收是 verification 的职责）
- 删除重复的"详细检查需求文档流程"章节
- 精简"功能完整性检查"（从 ~25 行 → ~18 行）
- 总行数从 381 行精简到 331 行

### Enhanced

#### writing-plans 重构（分层设计）

**核心层**（AI 必须遵循）：
- 创建计划流程简化为 4 步核心流程
- 简洁明了，AI 容易执行

**参考层**（需要时查阅）：
- 详细需求检查流程
- 功能完整性检查
- 任务结构模板

**优化内容**：
- 删除重复的"计划确认"章节
- 保留"阶段门控确认提示"
- 简化"检查需求文档"（7步 → 3步核心）
- 调整章节顺序，逻辑更清晰
- 总行数从 697 行精简到 ~350 行

## [1.7.3] - 2026-02-25

### Enhanced

#### 阶段门控确认提示
- brainstorming：结束增加"需要您确认"提示
- writing-plans：结束增加"需要您确认"提示
- executing-plans：结束增加"需要您确认"提示
- verification：结束增加"需要您确认"提示
- code-review：结束增加"需要您确认"提示

**简化触发时机**：每个阶段结束时，明确告知用户"需要确认什么"和"下一步是什么"

## [1.7.2] - 2026-02-25

### Enhanced

#### thinking-coach 增强
- 新增「本质分析」功能：问根本问题，找到问题本质
- 新增「维度分解」功能：把复杂问题拆解成不同维度（层次/角色/时间/范围）
- 帮助用户在困惑时找到分析问题的框架

#### brainstorming 融入交互设计
- 增加「用户流程检查清单」
  - 用户操作路径
  - 核心操作
  - 状态反馈
  - 异常流程
  - 边界提示
- 只检查概念层，具体界面在计划阶段

#### writing-plans 融入界面设计
- 新增「界面/组件设计任务」模板
  - 页面布局结构
  - 交互流程
  - 状态展示
  - 组件划分
- 在计划阶段考虑实现层界面设计

## [1.7.1] - 2026-02-25

### Added
- 新增 `code-analysis` 技能 - 代码分析专家
  - 代码问题分析（逻辑、边界、异常、资源管理）
  - 结构设计分析（模块划分、数据流、接口设计）
  - 代码质量分析（可读性、可维护性、性能、安全）
  - 前后端接口分析（API完整性、字段匹配、授权校验）
  - 问题诊断框架（方向不明确时的排查思路）
  - 决策支持框架（方案对比、技术选型）

### Enhanced
- 明确 code-analysis 与 debugging 技能的边界
  - debugging：已知 bug 定位修复
  - code-analysis：未知问题系统分析

## [1.7.0] - 2026-02-25

### 重大更新

#### 架构重构
- 删除所有 Agents，统一通过 Skills 定义能力
- 新增 6 个 Teams 配置，支持复杂协作场景

#### Skills 优化
- 恢复 `update-blueprint` 完成阶段
- `brainstorming` 增加多角度思考清单和场景识别
- `thinking-coach` 增加思维陷阱清单、决策框架、口语整理场景
- `verification` 增加验证失败处理流程
- 新增 `security-review`、`code-review`、`team-generator`、`claude-code-docs` 等 Skills

#### Commands 补齐
- 从 4 个增加到 12 个，覆盖所有高频场景

#### 流程优化
- verification 从执行阶段独立为正式阶段
- 明确阶段门控：需求→计划→执行→验证→审查→完成

### Removed
- 重复的 Agents（planner, tdd-guide, code-reviewer, security-reviewer, e2e-runner, debugger, architect）

### Enhanced
- 阶段门控机制完善
- 验证失败处理流程

## [1.6.5] - 2026-02-22

### Added
- Global Teardown support in Playwright config (`teardown.ts`)
- Double cleanup strategy (test-level + global teardown)

### Enhanced
- E2E runner documentation with cleanup strategy

## [1.6.4] - 2026-02-22

### Added
- `debugger` Agent - Debugging specialist for errors and bugs
- Independent context for complex debugging tasks

## [1.6.3] - 2026-02-22

### Added
- `test-planner` Skill - Test design before implementation
- Project analyzer capability (`.claude/skills/project-analyzer/`)

### Removed
- Duplicate skills (code-review, tdd-guide)

### Enhanced
- Agent descriptions support proactively auto-trigger

## [1.6.2] - 2026-02-20

### Added
- E2E functional flow testing support
- Complete CRUD flow test templates

## [1.6.1] - 2026-02-20

### Added
- Script and gitignore updates

## [1.6.0] - 2026-02-20

### Added
- `test-harness` Skill - Testing framework for plugin validation

### Enhanced
- Framework documentation sync capability

## [1.5.0] - 2026-02-20

### Added
- `docs-sync` Skill - Crawl framework documentation

## [1.4.0] - 2026-02-20

### Enhanced
- E2E runner performance optimizations

## [1.3.0] - 2026-02-20

### Added
- Execution checkpoints for progress tracking

## [1.2.0] - 2026-02-20

### Added
- Phase-based planning for large requirements

## [1.1.0] - 2026-02-20

### Added
- Feature completeness checks in brainstorming and writing-plans

## [1.0.0] - 2026-02-19

### Added
- Initial version
- Core skills:
  - discuss-requirements
  - describe-interaction
  - update-blueprint
  - frontend-guide (Vue3 + TypeScript)
  - backend-guide (Python + FastAPI)
- Code standards and patterns
