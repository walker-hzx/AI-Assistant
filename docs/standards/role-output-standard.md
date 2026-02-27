# 角色输出标准

> 所有角色完成任务后，必须返回标准化文档

## 核心原则

1. **每个角色必须有明确输出** - 不能只返回消息，必须创建文档
2. **文档位置统一** - 按类型保存在 `docs/` 目录下
3. **格式标准化** - 统一命名规范和内容结构

---

## 文档类型与保存位置

| 角色 | 文档类型 | 保存位置 | 命名规范 |
|------|---------|---------|---------|
| coordinator | 任务记录 | `docs/plans/` | `YYYY-MM-DD-<task>-coordinator.md` |
| requirements-analyst | 需求分析报告 | `docs/requirements/` | `YYYY-MM-DD-<feature>-requirements.md` |
| planner | 实施计划 | `docs/plans/` | `YYYY-MM-DD-<feature>-plan.md` |
| executor | 执行日志 | `docs/plans/` | `YYYY-MM-DD-<feature>-execution-log.md` |
| qa | 验证报告 | `docs/verification/` | `YYYY-MM-DD-<feature>-verification.md` |
| code-reviewer | 审查报告 | `docs/reviews/` | `YYYY-MM-DD-<feature>-review.md` |
| strategist | 分析报告 | `docs/analysis/` | `YYYY-MM-DD-<topic>-analysis.md` |
| debugger | 调试报告 | `docs/debug/` | `YYYY-MM-DD-<issue>-debug.md` |
| code-analysis | 分析报告 | `docs/analysis/` | `YYYY-MM-DD-<topic>-code-analysis.md` |
| architect | 架构文档 | `docs/architecture/` | `YYYY-MM-DD-<topic>-architecture.md` |
| database-expert | 数据库文档 | `docs/database/` | `YYYY-MM-DD-<topic>-database.md` |
| performance-expert | 性能报告 | `docs/performance/` | `YYYY-MM-DD-<topic>-performance.md` |
| refactoring-expert | 重构报告 | `docs/refactoring/` | `YYYY-MM-DD-<topic>-refactoring.md` |
| security-reviewer | 安全报告 | `docs/security/` | `YYYY-MM-DD-<feature>-security.md` |
| project-researcher | 调研报告 | `docs/research/` | `YYYY-MM-DD-<project>-research.md` |
| web-researcher | 研究报告 | `docs/research/` | `YYYY-MM-DD-<topic>-web-research.md` |
| e2e-tester | 测试报告 | `docs/testing/` | `YYYY-MM-DD-<feature>-e2e.md` |
| browser-debugger | 调试报告 | `docs/debug/` | `YYYY-MM-DD-<issue>-browser-debug.md` |

---

## 统一文档结构

### 最小输出内容

每个角色必须包含：

```markdown
# [文档标题]

**角色**：[角色名]
**时间**：YYYY-MM-DD HH:MM
**任务**：[任务描述]

## 执行结果

- 状态：[完成/部分完成/阻塞]
- 交付物：[产出文件/功能/修复]

## 详细说明

[具体执行内容]

## 发现的问题（如有）

| 问题 | 严重程度 | 建议 |
|------|----------|------|
|      |          |      |

## 后续建议（如有）

[如果任务未完成或需要后续处理]
```

---

## 输出检查清单

**任务完成前必须确认**：

- [ ] 已创建文档
- [ ] 文档保存在正确位置
- [ ] 文档包含最小输出内容
- [ ] 文档命名符合规范

**未满足任一条件，任务视为未完成。**

---

## Coordinator 文档汇总

Coordinator 负责收集所有角色的输出文档：

```markdown
## 任务执行汇总

**任务**：[任务描述]
**开始时间**：YYYY-MM-DD HH:MM
**结束时间**：YYYY-MM-DD HH:MM
**状态**：完成/部分完成

### 角色输出汇总

| 角色 | 文档位置 | 状态 |
|------|---------|------|
| requirements-analyst | docs/requirements/xxx.md | ✅ |
| planner | docs/plans/xxx.md | ✅ |
| executor | docs/plans/xxx-execution-log.md | ✅ |
| qa | docs/verification/xxx-report.md | ✅ |
```

---

## 文档目录自动创建

首次创建文档时，如果目录不存在，Coordinator 应自动创建：

```
docs/
├── requirements/   # 需求分析
├── plans/          # 计划和执行
├── verification/   # 验证报告
├── reviews/        # 代码审查
├── analysis/       # 分析报告
├── architecture/   # 架构文档
├── database/       # 数据库文档
├── performance/    # 性能报告
├── refactoring/    # 重构报告
├── security/       # 安全报告
├── research/       # 研究报告
├── testing/        # 测试报告
└── debug/         # 调试报告
```
