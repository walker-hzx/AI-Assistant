# Changelog

All notable changes to this project will be documented in this file.

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
