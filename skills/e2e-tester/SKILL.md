---
name: e2e-testing
description: "E2E 测试执行 - 执行端到端测试，确保用户流程正常工作。使用 Playwright/Cypress，包含 UI 断言指南和前端验证技巧"
model: sonnet
---

# E2E 测试执行

执行端到端测试，确保用户流程正常工作。

## 核心能力

1. **测试执行** - 运行 E2E 测试用例
2. **测试报告** - 生成测试结果报告
3. **问题定位** - 测试失败时定位问题
4. **UI 验证** - 前端交互的断言技巧

## 使用场景

- 验证用户完整流程（注册→登录→操作→登出）
- 前端功能需要浏览器测试
- 验收测试
- 回归测试

## 工作流程

### 步骤 1：确认测试需求

询问用户：
```
需要测试什么流程？
- 是完整的用户流程还是特定功能？
- 需要在哪些浏览器测试？
- 有现有的测试用例吗？
```

### 步骤 2：准备测试环境

检查测试框架：
```bash
# 检查是否已安装 Playwright
npx playwright --version

# 检查 Cypress
npx cypress --version
```

### 步骤 3：执行测试

根据情况执行：
```bash
# Playwright
npx playwright test

# Cypress
npx cypress run

# 单个测试文件
npx playwright test tests/login.spec.ts
```

### 步骤 4：分析结果

生成测试报告：
```markdown
## E2E 测试报告

**测试时间**：[时间]
**测试结果**：[通过/失败]
**测试框架**：[Playwright/Cypress]

### 测试摘要
- 总数：N
- 通过：N
- 失败：N
- 跳过：N

### 通过的测试
| 测试用例 | 耗时 |
|---------|------|
| 用例1 | 1.2s |

### 失败的测试
| 测试用例 | 错误 | 截图 |
|---------|------|------|
| 用例2 | Error message | screenshot.png |

### 建议
- [ ]
```

## 测试用例设计原则

### 核心流程覆盖

| 优先级 | 场景 | 说明 |
|--------|------|------|
| P0 | 登录/登出 | 核心功能 |
| P0 | 核心业务流程 | 主要功能路径 |
| P1 | 表单提交 | 数据录入 |
| P1 | 列表操作 | 增删改查 |
| P2 | 边缘情况 | 错误处理 |

### 测试用例结构

```typescript
// Playwright 示例
import { test, expect } from '@playwright/test';

test.describe('用户登录流程', () => {
  test('成功登录', async ({ page }) => {
    await page.goto('/login');
    await page.fill('#username', 'testuser');
    await page.fill('#password', 'password');
    await page.click('#submit');
    await expect(page.locator('.dashboard')).toBeVisible();
  });

  test('登录失败', async ({ page }) => {
    await page.goto('/login');
    await page.fill('#username', 'wrong');
    await page.fill('#password', 'wrong');
    await page.click('#submit');
    await expect(page.locator('.error')).toBeVisible();
  });
});
```

## 常用命令

### Playwright

```bash
# 安装
npm init playwright@latest

# 运行所有测试
npx playwright test

# 运行指定文件
npx playwright test tests/login.spec.ts

# 生成报告
npx playwright show-report

# 截取失败截图
npx playwright test --retries=2
```

### Cypress

```bash
# 安装
npm install cypress

# 打开 GUI
npx cypress open

# 运行测试
npx cypress run

# 指定浏览器
npx cypress run --browser chrome
```

## 常见问题

### Q: 测试跑不过怎么办？
A:
1. 先看错误信息
2. 检查是否是环境问题（浏览器版本、网络）
3. 检查测试用例是否过期
4. 查看截图/日志定位问题

### Q: 需要登录怎么办？
A:
1. 使用 beforeEach 处理登录
2. 或使用 cookie/session 复用
3. 或使用 API 登录获取 token

### Q: 异步加载怎么处理？
A:
1. 使用 page.waitForSelector
2. 使用 page.waitForLoadState('networkidle')
3. 使用 expect(locator).toBeVisible()

## 输出要求

**测试报告位置**：`docs/verification/`

**报告内容**：
- 测试时间
- 测试结果（通过/失败）
- 失败用例及错误信息
- 截图（如有）
- 建议

## 检查清单

- [ ] 确认测试需求
- [ ] 检查测试环境
- [ ] 执行测试
- [ ] 分析结果
- [ ] 生成报告
- [ ] 记录问题

---

## UI 断言指南

### 常见 UI 断言

| 场景 | Playwright | Cypress |
|------|------------|---------|
| 元素可见 | toBeVisible() | should('be.visible') |
| 元素存在 | toBeAttached() | should('exist') |
| 元素隐藏 | toBeHidden() | should('not.be.visible') |
| 文本包含 | toContainText() | should('contain', 'text') |
| 文本精确 | toHaveText() | should('have.text', 'text') |
| 输入框值 | toHaveValue() | should('have.value', 'text') |
| 元素数量 | toHaveCount(n) | should('have.length', n) |
| 类名包含 | toHaveClass() | should('have.class', 'name') |
| URL 匹配 | toHaveURL() | should('have.url', 'url') |
| 页面标题 | toHaveTitle() | should('have.title', 'title') |

### 等待策略

```typescript
// Playwright
// 1. 等待元素可见
await expect(page.locator('.loading')).not.toBeVisible();

// 2. 等待网络空闲
await page.waitForLoadState('networkidle');

// 3. 等待 API 响应
await page.waitForResponse(response => response.status() === 200);

// 4. 等待特定时间（慎用）
await page.waitForTimeout(1000);
```

```javascript
// Cypress
// 1. 等待元素可见
cy.get('.loading').should('not.be.visible');

// 2. 等待网络请求
cy.wait('@apiRequest');

// 3. 等待 DOM 稳定
cy.get('button').should('be.enabled');
```

### 交互断言

```typescript
// 点击后验证
await page.click('#submit');
await expect(page.locator('.success')).toBeVisible();

// 表单提交验证
await page.fill('#name', 'test');
await expect(page.locator('#name')).toHaveValue('test');

// 弹窗验证
await page.click('#open-modal');
await expect(page.locator('.modal')).toBeVisible();

// 表格行验证
await expect(page.locator('table tr')).toHaveCount(5);
```

### 截图对比（视觉回归）

```typescript
// Playwright
await expect(page).toHaveScreenshot('expected.png');

// 带 mask 的截图（忽略动态内容）
await expect(page).toHaveScreenshot('expected.png', {
  mask: [page.locator('.timestamp')],
});
```

### 前端验证技巧

| 场景 | 验证方式 |
|------|---------|
| 页面加载完成 | `waitForLoadState('networkidle')` |
| 动画结束 | `waitForTimeout` + 元素可见 |
| 异步数据渲染 | `waitForSelector` + 文本存在 |
| 弹窗动画 | `waitFor` + 可见性 |
| 列表排序 | 获取文本数组比对 |
| 表单校验 | 触发 blur 后检查错误提示 |
| 状态变更 | 检查 class/属性变化 |

### 常见问题处理

| 问题 | 解决方案 |
|------|---------|
| 元素点击无效 | 等待动画结束 + 强制点击 |
| 断言超时 | 增加 waitFor 或调整 timeout |
| 随机失败 | 添加重试机制 + 等待稳定 |
| 动态 ID | 使用 text/CSS 选择器替代 |
| 跨域 iframe | 切换到 iframe 上下文 |
