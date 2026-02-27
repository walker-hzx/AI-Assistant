---
name: unit-tester
description: "单元测试 - 编写和执行单元测试，确保代码质量。使用 Jest/Vitest/Pytest 等框架"
user-invocable: true
---

# 单元测试

编写和执行单元测试，确保代码质量。

## 使用场景

- 为函数/方法编写测试
- 为工具类编写测试
- 为组件的逻辑部分编写测试
- 验证边界条件和异常处理

## 测试框架

| 语言 | 推荐框架 |
|------|---------|
| JavaScript/TypeScript | Jest, Vitest |
| Python | pytest, unittest |
| Go | testing, testify |
| Java | JUnit, TestNG |

## 工作流程

### 1. 分析待测代码

```
读取待测代码，分析：
- 函数的输入/输出
- 边界条件
- 异常情况
- 依赖关系
```

### 2. 设计测试用例

```
基于分析结果，设计测试用例：

#### 正常输入
- 典型值测试
- 边界值测试

#### 异常输入
- 无效输入处理
- 边界条件
- 空值/undefined

#### 依赖处理
- Mock 外部依赖
- 模拟异常情况
```

### 3. 编写测试

```javascript
// 示例：Jest
describe('functionName', () => {
  test('正常输入 - 预期结果', () => {
    expect(functionName(input)).toBe(expected);
  });

  test('异常输入 - 应该抛出错误', () => {
    expect(() => functionName(invalidInput)).toThrow();
  });

  test('边界条件 - 空数组', () => {
    expect(functionName([])).toBe([]);
  });
});
```

### 4. 运行测试

```bash
# 运行单个测试文件
npm test -- filename.test.ts

# 运行并显示覆盖率
npm test -- --coverage

# 监听模式
npm test -- --watch
```

### 5. 检查覆盖率

```
目标覆盖率：
- 行覆盖率 ≥ 80%
- 分支覆盖率 ≥ 70%
- 函数覆盖率 ≥ 80%

如果覆盖率不足：
- 补充测试用例
- 标记无法测试的代码（istanbul ignore）
```

## 断言技巧

### 常见断言

| 场景 | 断言 |
|------|------|
| 相等 | toBe(), toEqual() |
| 布尔 | toBeTruthy(), toBeFalsy() |
| 空值 | toBeNull(), toBeUndefined() |
| 数组 | toContain(), toHaveLength() |
| 对象 | toMatchObject(), toHaveProperty() |
| 异常 | toThrow() |
| 异步 | resolves, rejects |

### 异步测试

```javascript
// Promise
test('异步操作', async () => {
  const result = await asyncFunction();
  expect(result).toBe(expected);
});

// Callback
test('回调函数', (done) => {
  callbackFunction((err, data) => {
    expect(err).toBeNull();
    done();
  });
});
```

## 测试组织

### 命名规范

```
# 文件命名
functionName.test.ts
functionName.spec.ts
functionName.test.js

# 测试描述
describe('模块名', () => {
  describe('方法名', () => {
    it('应该...', () => {});
  });
});
```

### 目录结构

```
src/
├── utils/
│   ├── format.ts
│   └── format.test.ts    # 测试文件放旁边
├── components/
│   ├── Button.tsx
│   └── Button.test.tsx   # 组件测试
```

## 输出

- 测试文件：与源文件同目录，后缀 .test.ts
- 覆盖率报告：coverage/ 目录

## 与其他工具的协作

- **tdd** → TDD 流程指导
- **code-implementation** → 实现代码后编写测试

---

## 快速开始

```
1. 分析待测代码
2. 设计测试用例
3. 编写测试
4. 运行测试
5. 检查覆盖率
```
