# Changelog

All notable changes to this project will be documented in this file.

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
