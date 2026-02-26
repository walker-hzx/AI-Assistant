---
name: tdd
description: "测试驱动开发 - 先写测试，再写实现，确保测试覆盖率。"
model: sonnet
user-invocable: true
---

# 测试驱动开发

## 概述

先写测试，再写实现，确保测试覆盖率。

**核心理念**：红色 → 绿色 → 重构。

---

## TDD 流程

### 1. 红色（Red）

写一个失败的测试：
- 描述期望的行为
- 运行测试确认失败
- 失败原因：功能未实现

### 2. 绿色（Green）

写最小实现通过测试：
- 只写让测试通过代码
- 不追求完美
- 运行测试确认通过

### 3. 重构（Refactor）

优化代码：
- 改善代码结构
- 保持测试通过
- 不添加新功能

---

## 测试原则

### 测试分层

| 层级 | 测试内容 |
|------|----------|
| 单元测试 | 函数、工具类 |
| 集成测试 | API、数据库 |
| E2E 测试 | 关键用户流程 |

### 测试覆盖

- 核心功能 100%
- 边界条件覆盖
- 异常情况覆盖

---

## 测试结构

```markdown
### 测试：[功能名称]

**步骤 1：编写失败测试**
```typescript
function test_behavior() {
  const result = function(input)
  expect(result).toBe(expected)
}
```

**步骤 2：运行验证失败**
- 预期：FAIL

**步骤 3：编写最小实现**
```typescript
function function(input) {
  return expected
}
```

**步骤 4：运行验证通过**
- 预期：PASS
```
---

## 注意事项

- 测试先行
- 最小实现
- 保持测试通过
- 持续重构
