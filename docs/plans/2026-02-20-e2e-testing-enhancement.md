# E2E 测试强化方案

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 加强前端 E2E 测试，确保代码完成后必须通过界面实际运行验证才能验收

**Architecture:** 在验证环节强制要求 E2E 测试覆盖关键流程，并在 execution-validation 中增加 UI 实际运行验证

**Tech Stack:** 修改 SKILL.md 文件

---

## 背景分析

### 当前问题

| 环节 | 当前状态 | 问题 |
|------|----------|------|
| verification-before-completion | E2E 测试是"（如有）" | 非强制，可跳过 |
| execution-validation | 只对照需求文档 | 没有 UI 实际运行验证 |
| e2e-runner | 有完整的 E2E 测试规范 | 未强制使用 |

### 用户核心需求

**代码写完了，不能只看测试通过，必须通过界面实际运行来验证效果。**

---

## 方案对比

### 方案 A：仅修改 verification-before-completion

| 方案 | 优点 | 缺点 |
|------|------|------|
| 将 E2E 测试从"（如有）"改为"必须" | 改动最小 | 执行时可能忽略 |

### 方案 B：仅修改 execution-validation

| 方案 | 优点 | 缺点 |
|------|------|------|
| 增加 UI 实际运行验证环节 | 直接解决需求 | 依赖于 E2E 测试存在 |

### 方案 C：综合方案（推荐）

| 改进点 | 方式 | 说明 |
|--------|------|------|
| verification-before-completion | E2E 测试改为必须 | 强制要求 |
| execution-validation | 增加 UI 实际运行验证 | 补充验证 |
| writing-plans | E2E 测试计划必须包含 | 规划阶段就考虑 |

---

## 推荐方案：方案 C

### 改进 1：verification-before-completion 强制 E2E 测试

**修改文件：** `skills/verification-before-completion/SKILL.md`

- 将"E2E 测试通过（如有）"改为"必须 E2E 测试通过"
- 增加 E2E 测试的检查清单

### 改进 2：execution-validation 增加 UI 实际运行验证

**修改文件：** `skills/execution-validation/SKILL.md`

- 增加"UI 实际运行验证"环节
- 明确验证方式：浏览器中实际运行 + 截图确认
- 检查关键 UI 元素是否正确渲染

### 改进 3：writing-plans E2E 测试计划必须包含

**修改文件：** `skills/writing-plans/SKILL.md`

- 在任务结构中增加 E2E 测试要求
- 关键功能必须包含 E2E 测试计划

---

## 任务总览

| 任务 | 描述 | 优先级 |
|------|------|--------|
| 1 | 修改 verification-before-completion 强制 E2E 测试 | P0 |
| 2 | 修改 execution-validation 增加 UI 验证 | P0 |
| 3 | 修改 writing-plans 增加 E2E 测试要求 | P1 |

---

## Task 1: 修改 verification-before-completion 强制 E2E 测试

**Files:**
- Modify: `skills/verification-before-completion/SKILL.md`

**修改内容：**

1. **修改前端额外检查**

当前：
```markdown
- [ ] E2E 测试通过（如有）
```

修改为：
```markdown
- [ ] E2E 测试通过（必须）
```

2. **增加 E2E 测试检查清单**

```markdown
### E2E 测试检查清单

- [ ] 关键用户流程已覆盖 E2E 测试
- [ ] 测试在无头模式（headless）下通过
- [ ] 测试使用稳定的选择器（data-testid）
- [ ] 失败时自动截图
- [ ] 关键断言已添加
```

3. **增加 E2E 测试重要性说明**

```markdown
## 为什么 E2E 测试必须

- 单元测试和组件测试无法发现运行时问题
- 代码看起来对，但实际跑起来可能有 bug
- 必须在真实浏览器环境中验证
- 这是确保代码可用的最后一道防线
```

---

## Task 2: 修改 execution-validation 增加 UI 验证

**Files:**
- Modify: `skills/execution-validation/SKILL.md`

**增加内容：**

1. **增加 UI 实际运行验证章节**

```markdown
## UI 实际运行验证

### 什么是 UI 实际运行验证

在真实浏览器环境中运行应用，检查：
- 页面是否正确渲染
- 交互是否正常工作
- 数据是否正确显示
- 错误是否正确处理

### 验证方式

1. **启动开发服务器**
```bash
npm run dev
```

2. **手动验证或 E2E 测试验证**
- 运行关键流程的 E2E 测试
- 检查测试截图
- 验证 UI 元素正确渲染

3. **截图对比**（可选）
- 预期效果截图
- 实际效果截图
- 对比差异

### 检查要点

| 检查项 | 说明 |
|--------|------|
| 页面加载 | 无白屏、无控制台错误 |
| 组件渲染 | 正确显示、无样式问题 |
| 交互响应 | 点击/输入有正确响应 |
| 数据展示 | 数据显示正确、无截断 |
| 错误处理 | 错误提示正确显示 |

### 输出格式

```markdown
## UI 实际运行验证结果

### 验证环境
- 浏览器：Chrome
- 分辨率：1920x1080
- URL：http://localhost:5173

### 验证结果
| 功能 | 状态 | 说明 |
|------|------|------|
| 登录页面 | ✅ | 正确渲染，输入框可交互 |
| 登录成功 | ✅ | 提交后正确跳转 |
| 登录失败 | ✅ | 错误提示正确显示 |
| 用户头像 | ✅ | 正确显示用户名称 |

### 结论
[是否通过验收]
```
```

2. **在验收标准中增加 UI 验证**

```markdown
## 验收标准

- [ ] 每个原始需求都有明确状态
- [ ] UI 实际运行验证通过
- [ ] E2E 测试通过（关键流程）
- [ ] 未完成项有合理解释
- [ ] 用户确认后才能标记为完成
```

---

## Task 3: 修改 writing-plans 增加 E2E 测试要求

**Files:**
- Modify: `skills/writing-plans/SKILL.md`

**修改内容：**

1. **在计划文档头部增加 E2E 要求**

```markdown
## 计划文档头部

**每个计划必须包含 E2E 测试计划：**

```markdown
## E2E 测试计划

### 关键流程（必须覆盖）
- [ ] 用户登录/登出
- [ ] 核心业务功能

### 测试方式
- [ ] 使用 Playwright
- [ ] 使用 data-testid 选择器
- [ ] 失败时自动截图
```

2. **在任务结构中增加 E2E 步骤**

```markdown
### 任务 N：[组件名称]

**文件：**
- 创建：`exact/path/to/file.ts`
- 修改：`exact/path/to/existing.ts:123-145`
- 测试：`tests/exact/path/to/test.ts`
- **E2E 测试**：`tests/e2e/specs/xxx.spec.ts`

**步骤 1：编写失败的测试**
...

**步骤 N：E2E 测试（关键功能必须）**

如果此功能涉及用户界面，需要添加 E2E 测试：
```typescript
test('功能名称', async ({ page }) => {
  await page.goto('/feature');
  // 验证关键交互
  await expect(page.locator('[data-testid="xxx"]')).toBeVisible();
});
```
```

---

## 实施顺序

1. Task 1: 修改 verification-before-completion（强制 E2E）
2. Task 2: 修改 execution-validation（增加 UI 验证）
3. Task 3: 修改 writing-plans（规划阶段考虑 E2E）

---

## 优化后的验证流程

```
代码完成
    ↓
verification-before-completion
    ↓ [强制 E2E 测试通过]
execution-validation
    ↓ [UI 实际运行验证]
update-blueprint
```

---

## Plan complete and saved to `docs/plans/2026-02-20-e2e-testing-enhancement.md`

Two execution options:

1. **Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

2. **Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

Which approach?
