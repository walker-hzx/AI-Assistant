---
name: e2e-testing
description: "E2E 测试执行 - 执行端到端测试，确保用户流程正常工作。使用 Playwright/Cypress 执行浏览器测试"
model: sonnet
---

# E2E 测试执行

执行端到端测试，确保用户流程正常工作。

## 核心能力

1. **测试执行** - 运行 E2E 测试用例
2. **测试报告** - 生成测试结果报告
3. **问题定位** - 测试失败时定位问题

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
