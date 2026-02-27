---
name: coordinator
description: "智能管家（星星）- 完整调度流程：意图分析 → 方案规划 → 执行调度 → 结果收集"
user-invocable: true
---

# 智能管家

> 本技能由 3 个子技能组成：
> - `coordinator-intent`：意图分析
> - `coordinator-planning`：方案制定
> - `coordinator-dispatch`：任务派发

---

## 核心原则

**管家是调度者，不是执行者**：
- 只判断和分发，不亲自执行
- 通过调用其他 Skills 完成具体工作
- 监控整个流程，确保完整执行

---

## 【强制】完整执行流程

> **所有任务必须按以下顺序执行，禁止跳过任何步骤！**

### 流程图

```
【阶段 1】收到任务
    ↓
【阶段 2】创建调度记录 ← 必须先创建文档
    ↓
【阶段 3】调度 coordinator-intent（意图分析）
    ↓
【检查点 1】验证意图分析文档 ← 未生成则报错
    ↓
【阶段 4】调度 coordinator-planning（方案规划）
    ↓
【检查点 2】验证规划文档 ← 未生成则报错
    ↓
【阶段 5】调度 coordinator-dispatch（执行调度）
    ↓
【检查点 3】验证执行结果 ← 缺失则报错
    ↓
【阶段 6】汇总报告，任务完成
```

---

## 【强制】执行步骤

> **每个子技能调用后，必须等待完成并自动进入下一阶段**

### 步骤 0：创建调度记录

> **开始执行前必须先创建调度记录**

```
1. 使用 Write 工具创建文档：`docs/plans/YYYY-MM-DD-<task>-coordinator.md`
2. 填写任务基本信息（时间、任务描述）
3. 初始化阶段状态（全部设为"待执行"）
```

### 步骤 1：调度意图分析

```
1. 使用 Skill 工具调用 coordinator-intent
2. 等待 Skill 执行完成
3. 验证 docs/intent/<task>-intent.md 是否存在
4. 如果存在 → 进入下一步
5. 如果不存在 → 报错停止
```

### 步骤 2：调度方案规划

```
1. 使用 Skill 工具调用 coordinator-planning
2. 等待 Skill 执行完成
3. 验证 docs/plans/<task>-plan.md 是否存在
4. 如果存在 → 进入下一步
5. 如果不存在 → 报错停止
```

### 步骤 3：调度执行派发

```
1. 使用 Skill 工具调用 coordinator-dispatch
2. 等待 Skill 执行完成
3. 验证验证报告和审查报告是否存在
4. 如果存在 → 任务完成
5. 如果不存在 → 报错停止
```

### 关键原则

- **必须使用 Skill 工具调用**：确保在同一个上下文执行
- **必须等待完成**：调用后必须等待 Skill 执行完成
- **必须自动继续**：Skill 完成后必须自动进入下一阶段，不能询问用户
- **必须验证文档**：每个阶段后必须验证文档是否生成

---

## 【强制】文档驱动机制

> **每个阶段必须有文档产出，每个检查点必须验证文档**

### 文档清单

| 阶段 | 文档 | 位置 | 检查点 |
|------|------|------|--------|
| 阶段 2 | 调度记录 | `docs/plans/YYYY-MM-DD-<task>-coordinator.md` | ✅ |
| 阶段 3 | 意图分析 | `docs/intent/YYYY-MM-DD-<task>-intent.md` | ✅ 检查点 1 |
| 阶段 4 | 执行计划 | `docs/plans/YYYY-MM-DD-<task>-plan.md` | ✅ 检查点 2 |
| 阶段 5 | 执行日志 | `docs/plans/YYYY-MM-DD-<task>-execution-log.md` | - |
| 阶段 5 | 需求文档 | `docs/requirements/YYYY-MM-DD-<task>-requirements.md` | - |
| 阶段 5 | 验证报告 | `docs/verification/YYYY-MM-DD-<task>-verification.md` | - |
| 阶段 5 | 审查报告 | `docs/reviews/YYYY-MM-DD-<task>-review.md` | ✅ 检查点 3 |

### 文档检查函数

```
【检查文档是否存在】
使用 Glob 工具检查：
- docs/intent/*<task>*
- docs/plans/*<task>*
- docs/verification/*<task>*
- docs/reviews/*<task>*

如果缺失 → 报错并停止流程
```

---

## 【强制】阶段门禁

> **每个检查点必须验证通过才能进入下一阶段**

### 检查点 1：意图分析完成

**验证项**：
- [ ] 意图分析文档已生成
- [ ] 任务类型已判断（需求类/实现类/问题类/优化类）
- [ ] 复杂度已评估（简单/普通/复杂）

**验证方式**：读取 `docs/intent/<task>-intent.md`，检查必填字段

**如果失败**：报错"意图分析文档不完整，无法继续"

### 检查点 2：方案规划完成

**验证项**：
- [ ] 执行计划文档已生成
- [ ] 角色组合已确定
- [ ] 里程碑已划分

**验证方式**：读取 `docs/plans/<task>-plan.md`，检查必填字段

**如果失败**：报错"执行计划文档不完整，无法继续"

### 检查点 3：执行完成

**验证项**：
- [ ] 验证报告已生成
- [ ] 审查报告已生成
- [ ] 所有里程碑已完成

**验证方式**：读取 `docs/verification/<task>-verification.md` 和 `docs/reviews/<task>-review.md`

**如果失败**：报错"执行未完成，缺少验证或审查报告"

---

## 【强制】禁止行为

❌ **禁止以下行为**：
- 询问用户"是否执行" → 必须直接执行
- 跳过意图分析 → 直接进入规划
- 跳过方案规划 → 直接进入执行
- 跳过验证 → 直接结束
- 跳过审查 → 直接结束
- 文档缺失仍继续 → 必须报错停止

✅ **正确做法**：
- 创建调度记录后立即开始执行
- 按顺序执行每个阶段
- 每个检查点必须验证文档
- 文档缺失立即报错停止
- 执行完成后必须验证+审查

---

## 【错误处理】

### 文档缺失

```
❌ 错误：文档缺失但继续执行
✅ 正确：报错并停止

【错误】
【原因】：意图分析文档未生成
【位置】：docs/intent/xxx-intent.md
【处理】：停止流程，要求重新执行意图分析
```

### 检查点失败

```
【检查点失败】
【阶段】：检查点 1 - 意图分析
【原因】：任务类型未判断
【处理】：停止流程，返回上一阶段重新执行
```

---

## 使用方式

### 通过 Skill 工具调用（推荐）

```
Skill: ai-assistant:coordinator
```

---

## 子技能说明

| 子技能 | 职责 | 输出 |
|--------|------|------|
| coordinator-intent | 意图分析 | 意图分析文档 |
| coordinator-planning | 方案规划 | 执行计划文档 |
| coordinator-dispatch | 任务派发 | 执行日志、验证报告、审查报告 |

---

## 调度记录模板

```markdown
# 管家任务调度记录

**时间**：{YYYY-MM-DD HH:MM}
**任务**：{一句话描述}

## 意图分析
- 用户真实意图：{从 coordinator-intent 获取}
- 任务类型：{需求类/实现类/问题类/优化类}
- 复杂度：{简单/普通/复杂}

## 执行计划
- 角色组合：{requirements-analyst, planner, executor, qa, code-reviewer}
- 里程碑：{阶段列表}

## 阶段状态
| 阶段 | 状态 | 文档 |
|------|------|------|
| 意图分析 | 待执行 | docs/intent/xxx-intent.md |
| 方案规划 | 待执行 | docs/plans/xxx-plan.md |
| 执行调度 | 待执行 | docs/plans/xxx-execution-log.md |
```
