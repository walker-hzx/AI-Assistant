# 执行规范

> 本文档定义管家执行任务的流程规范

---

## 执行流程

### 流程图

```
【步骤 0】任务状态检测
    ↓
【步骤 1】接收任务 + 创建调度记录
    ↓
【步骤 2】需求分析
    ↓
【步骤 3】制定计划（可选）
    ↓
【步骤 4】执行任务（循环）
    ↓
【步骤 5】功能验证（可选）
    ↓
【步骤 6】代码审查（可选）
    ↓
【步骤 7】质量评估（复杂任务）
    ↓
【步骤 8】完成
```

**注意**：根据任务类型选择需要的步骤，详见 SKILL.md

---

## 步骤详解

### 步骤 0：任务状态检测

**任务来源**：用户输入

**处理**：
1. 扫描 docs/coordinator/ 目录
2. 查找状态为"进行中"的调度记录
3. 判断用户输入性质（新任务/继续任务）

### 步骤 1：接收任务 + 创建调度记录

**必须创建文档**：`docs/coordinator/<task>-coordinator.md`

**内容**：
```markdown
# 任务调度记录

- **任务名称**：{任务名}
- **任务类型**：{功能开发/Bug修复/调研/其他}
- **创建时间**：{YYYY-MM-DD}
- **状态**：进行中

## 阶段状态

| 阶段 | 状态 | 说明 |
|------|------|------|
| 任务状态检测 | ✅ | 已完成 |
| 接收任务 | ✅ | 已完成 |
| 需求分析 | 待执行 | - |
| 制定计划 | 待执行 | - |
| 执行任务 | 待执行 | - |
| 功能验证 | 待执行 | - |
| 代码审查 | 待执行 | - |
| 质量评估 | 待执行 | - |
| 完成 | 待执行 | - |
```

### 步骤 2：需求分析（可选）

**调用角色**：thinking-coach, requirement-analysis, web-researcher

**触发条件**：
- 用户需求不明确
- 需要多角度分析

**输出文档**：`docs/intent/<task>-intent.md`

### 步骤 3：制定计划（可选）

**此步骤可选**：简单任务可跳过

**调用角色**：writing-plans / strategist

**必须生成文档**：`docs/plans/<task>-plan.md`

**内容**：
- 角色组合
- 执行顺序
- 里程碑列表
- 每轮执行的子任务

### 步骤 4：执行任务（循环）

**核心机制**：闭环执行循环

```
【执行轮次 N】
1. 从计划中获取当前轮次的任务
2. 调度相应 Subagent 执行
3. 等待 Subagent 完成
4. 读取输出文档
5. 检查执行结果
6. 判断是否需要调整
    → 需要调整 → 更新计划 → 继续
    → 完成 → 进入下一步
```

**执行日志**：`docs/execution/<task>-execution-N.md`

### 步骤 5：功能验证（可选）

**此步骤可选**：调研任务等不需要

**调用角色**：qa, e2e-tester

**输出文档**：`docs/verification/<task>-verification.md`

### 步骤 6：代码审查（可选）

**此步骤可选**：调研任务等不需要

**调用角色**：code-reviewer, security-reviewer, ui-ux-reviewer

**输出文档**：`docs/reviews/<task>-review.md`

### 步骤 7：质量评估（仅复杂任务）

**仅复杂任务需要**

**调用角色**：evaluator

**输出文档**：`docs/quality/<task>-summary.md`

### 步骤 8：完成

**更新调度记录**：标记任务为"已完成"

---

## 文档位置约定

```
docs/
├── coordinator/         # 管家调度记录
│   └── <task>-coordinator.md
├── intent/             # 需求分析
│   └── <task>-intent.md
├── plans/             # 计划文档
│   └── <task>-plan.md
├── execution/          # 执行日志（按轮次）
│   ├── <task>-execution-1.md
│   ├── <task>-execution-2.md
│   └── ...
├── verification/       # 验证报告
│   └── <task>-verification.md
├── reviews/           # 审查报告
│   └── <task>-review.md
└── quality/           # 质量评估报告
    ├── <task>-eval-1.md
    └── <task>-summary.md
```
