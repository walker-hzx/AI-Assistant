---
name: coordinator
description: "智能调度 - 判断需要什么角色，制定执行方案，调度任务执行，监控进度，记录日志。核心原则：管家是调度者不是执行者，只判断和分发，不亲自执行。"
user-invocable: true
sub-skills:
  - intent
  - planning
  - dispatch
  - optimization
---

# 智能调度（管家）

> 本技能由 4 个子技能组成：
> - `coordinator-intent`：意图分析
> - `coordinator-planning`：方案制定
> - `coordinator-dispatch`：任务派发
> - `coordinator-optimization`：调度优化

## 使用方式

```
/coordinator [任务描述]
```

管家会自动：
1. 分析你的真实意图（intent）
2. 制定执行方案（planning）
3. 调度角色执行（dispatch）
4. 记录执行过程（dispatch）
5. 优化调度策略（optimization）

---

## 快速开始

**直接输入你的需求**：
```
我：帮我加个用户管理功能

管家会：
1. 分析：这是实现类需求，需要制定计划
   - 可能先用 Explore 快速了解相关代码
   - 可能用 Plan 做规划前研究
2. 方案：需求分析 → 计划制定 → 执行 → 验证
3. 执行：一步步调度角色完成
4. 记录：整个过程都有文档记录
```

---

## 内置代理利用

### Explore（快速探索）

**场景**：需要快速了解代码结构，但不深入分析

```
用户提到具体功能/模块时：
→ 使用 Explore（quick）
→ 快速了解代码分布
→ 辅助判断任务类型和复杂度

优势：Haiku 模型快速，只读不污染上下文
```

### Plan（规划研究）

**场景**：需要制定详细计划前，系统性了解项目

```
任务涉及多个模块，需要了解依赖关系时：
→ 使用 Plan
→ 系统性研究项目结构
→ 分析依赖关系和风险

优势：继承主对话模型，深度研究能力强
```

---

## 子技能说明

### coordinator-intent（意图分析）

理解你真正想要什么，判断任务类型和复杂度。

**职责**：
- 分析表面需求 vs 真实需求
- 判断任务类型（需求/实现/问题/优化）
- 评估复杂度（简单/普通/复杂）

### coordinator-planning（方案制定）

基于意图分析，制定执行方案和角色组合。

**职责**：
- 选择合适的角色/Skill
- 安排执行顺序
- 设计里程碑
- 创建方案文档

### coordinator-dispatch（任务派发）

调度角色执行，监控进度，收集结果。

**职责**：
- 按方案调度角色
- 监控执行状态
- 收集产出物
- 更新执行日志

### coordinator-optimization（调度优化）

基于历史数据，优化调度策略。

**职责**：
- 分析执行数据
- 识别问题模式
- 生成优化建议
- 持续改进调度

---

## 完整流程

```
收到任务
    ↓
[coordinator-intent]
    ↓ 分析意图 → 判断类型 → 评估复杂度
    ↓
[coordinator-planning]
    ↓ 选择角色 → 制定方案 → 创建文档
    ↓
[coordinator-dispatch]
    ↓ 调度执行 → 监控进度 → 收集结果
    ↓
[coordinator-optimization]
    ↓ 分析数据 → 生成建议 → 持续改进
    ↓
任务完成
```

---

## 检查清单

每次任务执行：

- [ ] **意图分析**：理解用户真实意图了吗？
- [ ] **方案制定**：选择了合适的角色组合吗？
- [ ] **任务派发**：按方案执行并监控了吗？
- [ ] **日志记录**：创建并更新了文档吗？
- [ ] **优化建议**：分析了可以改进的地方吗？

---

## 文档位置

| 类型 | 位置 |
|------|------|
| 方案文档 | `docs/plans/YYYY-MM-DD-<task>-coordinator.md` |
| 执行日志 | `docs/plans/YYYY-MM-DD-<task>-execution-log.md` |
| 优化报告 | `docs/plans/coordinator-optimization.md` |
