# AI-Assistant 配置问题清单

> 生成日期：2026-02-21

---

## 一、硬编码问题（需要修改）

### 1.1 writing-plans/SKILL.md

| 行号 | 当前内容 | 建议修改 |
|------|----------|----------|
| 261 | `- **前端**: Vue 3 + TypeScript + Vite + Vitest` | 根据项目实际情况确定 |
| 262 | `- **后端**: Python + FastAPI + pytest` | 根据项目实际情况确定 |

### 1.2 executing-plans/SKILL.md

| 行号 | 当前内容 | 建议修改 |
|------|----------|----------|
| 216 | `- **前端**: Vue 3 + TypeScript + Vitest` | 根据项目实际情况确定 |
| 217 | `- **后端**: Python + FastAPI + pytest` | 根据项目实际情况确定 |

### 1.3 update-blueprint/SKILL.md

| 行号 | 当前内容 | 建议修改 |
|------|----------|----------|
| 65 | `技术栈：Vue3 + TypeScript + FastAPI + PostgreSQL` | 根据项目实际情况确定 |

### 1.4 tdd-guide/SKILL.md (在 skills 目录下)

| 行号 | 当前内容 | 建议修改 |
|------|----------|----------|
| 62 | `### 前端 (Vue3 + TypeScript)` | `### 前端` |
| 68 | `### 后端 (Python + FastAPI)` | `### 后端` |

---

## 二、特定技能（不需要修改）

以下文件是特定技术栈的开发指南，硬编码是合理的：

| 文件 | 说明 |
|------|------|
| skills/python-fastapi-guide/SKILL.md | FastAPI 开发指南，本身就是针对特定技术栈 |
| skills/vue3-vite-guide/SKILL.md | Vue3 开发指南，本身就是针对特定技术栈 |

---

## 三、可优化点

### 3.1 commands 目录

- 当前有 6 个 command 文件
- 检查是否有缺失的常用命令

### 3.2 skills 完整性

检查以下流程是否都有对应 skill：
- [ ] 需求讨论 ✅ (discuss-requirements)
- [ ] 交互描述 ✅ (describe-interaction)
- [ ] 头脑风暴 ✅ (brainstorming)
- [ ] 制定计划 ✅ (writing-plans)
- [ ] 执行计划 ✅ (executing-plans)
- [ ] 验证代码 ✅ (verification-before-completion)
- [ ] 验证需求 ✅ (execution-validation)
- [ ] 更新蓝图 ✅ (update-blueprint)

### 3.3 agents 完整性

检查以下角色是否都有：
- [ ] 规划师 ✅ (planner)
- [ ] 架构师 ✅ (architect)
- [ ] 代码审查 ✅ (code-reviewer)
- [ ] TDD 专家 ✅ (tdd-guide)
- [ ] E2E 专家 ✅ (e2e-runner)
- [ ] 安全专家 ✅ (security-reviewer)

---

## 四、hooks 配置

| 事件 | 状态 | 说明 |
|------|------|------|
| SessionStart | ✅ | 会话开始 hook |
| PostToolUse | ✅ | 工具使用日志 |
| PreToolUse | ✅ | Bash 命令权限 guard |
| Stop | ✅ | 会话结束 |

hooks 配置看起来合理。

---

## 五、待讨论项

1. **是否需要更多特定技术栈的 guide？**
   - 如：React + Next.js guide
   - 如：Go + Gin guide
   - 如：NestJS guide

2. **是否需要添加新的 skill？**
   - 如：refactoring skill（重构专用）
   - 如：performance-optimization skill（性能优化）

3. **是否需要添加新的 agent？**
   - 如：devops agent（部署、运维）
   - 如：database agent（数据库设计、优化）

---

## 六、优先级排序

### P0（必须修改）

- [ ] writing-plans 技术栈硬编码
- [ ] executing-plans 技术栈硬编码
- [ ] update-blueprint 技术栈硬编码
- [ ] tdd-guide (skills) 硬编码

### P1（建议优化）

- [ ] 检查 commands 完整性
- [ ] 检查 skills 完整性
- [ ] 检查 agents 完整性

### P2（长期考虑）

- [ ] 添加更多技术栈 guide
- [ ] 添加更多 agent
