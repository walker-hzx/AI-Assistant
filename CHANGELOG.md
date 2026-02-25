# Changelog

All notable changes to this project will be documented in this file.

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
