# 管家调度优化方案（草稿）

> 基于 2026-02-27 讨论 + 测试记录分析

---

## 问题总结（来自测试记录分析）

### 问题 1：计划中未明确指定执行者
- **现象**：计划文档中的任务没有明确指定由哪个 Subagent 执行
- **影响**：执行时无法确定调用哪个角色，容易用错名字
- **解决**：每个任务必须显式声明 `执行者：<Subagent名称>`

### 问题 2：使用了错误的 Subagent 名称
- **现象**：使用了不存在的名称如 `code-implementation`、`executing-plans`
- **影响**：Task 工具调用失败
- **解决**：严格使用 ROLES.md 中定义的 15 个 Subagent 名称

### 问题 3：验证描述过于模糊
- **现象**：验证步骤只写"验证功能"，没有具体标准
- **影响**：无法判断是否真正通过
- **解决**：每个任务必须包含明确的验收标准

### 问题 4：缺少信息约定
- **现象**：Subagent 不知道从哪里读取信息、结果写到哪里
- **影响**：上下文隔离导致信息丢失
- **解决**：制定完整的信息约定文档

---

## 需求总结

### 1. 管家定位
- 管家 = 中控大脑
- 职责 = 任务统筹安排 + 分发
- 不是执行者，是调度者

### 2. Claude Code Subagent 特性
- 上下文隔离：Subagent 执行时没有主会话上下文
- 独立执行：像独立任务处理
- 信息传递：通过文档约定

### 3. 调用方式
- 当前：Task(ai-assistant:executor, prompt="...")
- 期望：使用 executor subagent（自然语言）

---

## 优化方案

### 1. 定义流程包（绑定步骤）

| 流程包 | 包含角色 | 适用场景 |
|--------|---------|---------|
| 开发流程 | requirement-analysis → executor → qa → code-reviewer | 新功能开发 |
| 调试流程 | debugger → qa → code-reviewer | Bug 修复 |
| 分析流程 | code-analysis | 代码问题分析 |
| 调研流程 | project-researcher / web-researcher | 项目调研、资料查找 |
| 测试流程 | test-designer → e2e-tester | 测试设计、E2E 测试 |
| 安全流程 | security-reviewer | 安全审查 |

### 2. 计划文档强制格式

每个任务必须包含以下字段：

```markdown
### 任务 N：[任务名称]

**执行者：** executor （必填，从 ROLES.md 中选择）

**输入：** docs/plans/xxx-plan.md （从哪里读取信息）

**输出：** docs/execution/xxx-execution-N.md （结果写到哪里）

**验收标准：**
- [ ] 标准1：功能正常运行
- [ ] 标准2：单元测试通过

**回滚步骤（可选）：**
1. `git checkout src/xxx.ts`
```

### 3. 信息约定（优化版 - 基于 Claude Code 特性）

> **背景**：Subagent 能收到系统提示（角色定义）+ 基本环境信息，但收不到主会话完整上下文和前置任务结果。

**信息传递方式**：
1. **Task prompt** - 直接传递任务要求（主要方式）
2. **文档** - 传递上下文、执行结果（补充方式）

| Subagent | Task prompt 传递 | 文档传递 | 说明 |
|----------|-----------------|---------|------|
| requirement-analysis | 需求内容 | docs/intent/ | 分析结果写入文档 |
| executor | 任务描述 + 验收标准 | docs/plans/ | 从计划读取详细步骤 |
| debugger | 问题描述 + 错误信息 | docs/execution/ | 读取执行日志定位问题 |
| qa | 验证要求 | docs/plans/, docs/execution/ | 读取计划和执行结果 |
| code-reviewer | 审查要求 | docs/verification/ | 从验证报告开始审查 |
| security-reviewer | 审查范围 | docs/execution/ | 读取代码进行审查 |
| test-designer | 需求内容 | docs/intent/, docs/plans/ | 分析需求输出测试用例 |
| e2e-tester | 测试场景 | docs/plans/, docs/verification/ | 读取测试计划执行 |
| thinking-coach | 问题描述 | docs/intent/ | 写入思考引导结果 |
| strategist | 决策问题 | docs/plans/ | 写入策略分析 |
| code-analysis | 分析目标 | docs/plans/ | 写入分析报告 |
| project-researcher | 调研目标 | - | 可直接读取项目 |
| web-researcher | 研究目标 | docs/plans/ | 写入研究成果 |
| browser-debugger | 问题描述 | docs/execution/ | 读取错误日志 |
| team-generator | 团队需求 | docs/plans/ | 写入团队配置 |

### 4. Subagent 名称白名单（必须严格使用）

```
thinking-coach, strategist, code-analysis, project-researcher, web-researcher,
requirement-analysis, executor, qa, e2e-tester, test-designer,
security-reviewer, code-reviewer, debugger, browser-debugger, team-generator
```

**禁止使用的名称**：
- code-implementation ❌
- executing-plans ❌
- implementation ❌
- 执行 ❌

---

## 管家制定计划流程

```
1. 接收任务
2. 分析任务类型
3. 选择对应的"流程包"
4. 拆分任务（每个任务 2-5 分钟）
5. 【关键】为每个任务指定执行者
6. 【关键】明确输入/输出目录
7. 【关键】制定验收标准
8. 写入计划文档
```

---

## 实施步骤

1. 更新 coordinator SKILL.md 中的计划模板
2. 在检查点中添加"执行者声明检查"
3. 添加 Subagent 名称验证
4. 测试验证

---

## 待确认
- [x] 流程包定义是否合理
- [x] 信息约定是否完整
- [x] 计划模板格式是否完善
- [ ] 如何测试
