# 输出规范

> 本文档定义各阶段输出文档的格式规范

---

## 文档类型

| 文档类型 | 路径 | 创建者 | 是否必需 |
|----------|------|--------|----------|
| 调度记录 | `docs/coordinator/<task>-coordinator.md` | coordinator | 必需 |
| 需求分析 | `docs/intent/<task>-intent.md` | 需求类角色 | 可选 |
| 计划文档 | `docs/plans/<task>-plan.md` | 计划类角色 | 可选 |
| 执行日志 | `docs/execution/<task>-execution-N.md` | coordinator | 必需 |
| 验证报告 | `docs/verification/<task>-verification.md` | 验证类角色 | 可选 |
| 审查报告 | `docs/reviews/<task>-review.md` | 审查类角色 | 可选 |
| 质量评估 | `docs/quality/<task>-summary.md` | evaluator | 仅复杂任务 |
| 质疑报告 | `docs/skeptics/<task>-<type>-skeptics.md` | skeptics | 质疑环节必做 |

---

## 调度记录模板

```markdown
# 任务调度记录

- **任务名称**：{任务名}
- **任务类型**：{功能开发/Bug修复/调研/其他}
- **创建时间**：{YYYY-MM-DD}
- **状态**：{进行中/已完成/失败}

## 阶段状态

| 阶段 | 状态 | 说明 |
|------|------|------|
| 任务状态检测 | ✅ | 已完成 |
| 接收任务 | ✅ | 已完成 |
| 需求分析 | ✅/待执行 | - |
| 制定计划 | ✅/待执行 | - |
| 执行任务 | 进行中 | - |
| 功能验证 | 待执行 | - |
| 代码审查 | 待执行 | - |
| 完成 | 待执行 | - |
```

---

## 需求分析模板

```markdown
# 需求分析：{任务名称}

**时间**：{YYYY-MM-DD HH:MM}

## 需求理解
- 用户真实意图：{一句话说清楚}
- 任务类型：{功能开发/Bug修复/调研/其他}
- 复杂度：{简单/中等/复杂}

## 详细分析
{多角度分析内容}

## 角色建议
- 推荐角色：{角色组合}
- 执行顺序：{顺序}
```

---

## 计划文档模板

```markdown
# 实施计划：{任务名称}

**时间**：{YYYY-MM-DD HH:MM}

## 角色组合
{角色列表和用途}

## 里程碑
### 里程碑 1：{名称}
- [ ] 任务 1
- [ ] 任务 2

### 里程碑 2：{名称}
- [ ] 任务 3

## 执行轮次
### 轮次 1
- 角色：{角色名}
- 任务：{任务描述}
- 预期输出：{输出文档}
```

---

## 执行日志模板

```markdown
# 执行日志：{任务名称}

**轮次**：{N}
**时间**：{YYYY-MM-DD HH:MM}

## 当前状态
- 状态：{进行中/已完成/需调整/失败}
- 当前角色：{角色名}

## 执行记录
### 调用角色
- 角色：{角色名}
- 调用：Task(ai-assistant:xxx)

### 执行过程
{执行详细过程}

### 输出结果
- 输出文档：{路径}
- 执行结果：{成功/失败/需调整}

## 下一步
- [ ] {下一步任务}
```

---

## 验证报告模板

```markdown
# 验证报告：{任务名称}

**时间**：{YYYY-MM-DD HH:MM}
**验证者**：qa

## 验证结果
- 状态：{通过/未通过/有条件通过}
- 通过项：{列表}
- 未通过项：{列表}

## 详细结果
### 功能验证
{功能验证详情}

### 测试结果
{测试执行结果}

## 结论
{验证结论}
```

---

## 审查报告模板

```markdown
# 审查报告：{任务名称}

**时间**：{YYYY-MM-DD HH:MM}
**审查者**：code-reviewer

## 审查结果
- 状态：{通过/未通过/有条件通过}
- 严重问题：{数量}
- 建议：{数量}

## 代码质量
- 可读性：{评分}
- 可维护性：{评分}
- 安全性：{评分}

## 问题列表
| 问题 | 严重程度 | 位置 | 建议 |
|------|----------|------|------|
| 问题1 | 高 | 文件:行号 | 修复建议 |

## 结论
{审查结论}
```

---

## 质疑报告模板

```markdown
# 质疑报告：{质疑类型}

**时间**：{YYYY-MM-DD HH:MM}
**质疑者**：skeptics
**质疑类型**：{requirement/completeness/plan/output/verification/review}

## 整体评价
[简要说明整体评价]

## 质疑点

### 🔴 阻断级（必须处理）

| 序号 | 质疑点 | 说明 | 建议 |
|------|-------|------|------|
| 1 | ... | ... | ... |

### 🟠 重要级（建议处理）

| 序号 | 质疑点 | 说明 | 建议 |
|------|-------|------|------|
| 1 | ... | ... | ... |

### 🟡 建议级（可选处理）

| 序号 | 质疑点 | 说明 | 建议 |
|------|-------|------|------|
| 1 | ... | ... | ... |

## 结论

- 阻断级问题：X个
- 重要级问题：X个
- 建议级问题：X个

**建议**：[总结建议]
```

---

## 文档命名规范

```
格式：<task>-<type>.md

示例：
- user-login-coordinator.md
- user-login-intent.md
- user-login-plan.md
- user-login-execution-1.md
- user-login-verification.md
- user-login-review.md
- user-login-summary.md
- user-login-requirement-skeptics.md
- user-login-completeness-skeptics.md
- user-login-plan-skeptics.md
- user-login-output-skeptics.md
- user-login-verification-skeptics.md
- user-login-review-skeptics.md
```
