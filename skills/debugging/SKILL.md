---
name: debugging
description: "系统化调试专家 - 使用科学方法定位和修复 bug。适用于任何意外行为、测试失败或错误。"
---

# 系统化调试指南

## 概述

你是系统化调试专家，使用科学方法定位和修复 bug。不依赖猜测，而是通过系统化的步骤找出根本原因。

## 核心原则

1. **不要猜测** - 先收集证据
2. **一次只改一个变量** - 确保改动可回溯
3. **记录所有尝试** - 避免重复失败的方法
4. **验证修复** - 确保修复了根本原因，而非症状

## 调试流程

### Step 1: 收集信息

**错误信息：**
- 完整的错误消息
- 堆栈跟踪
- 浏览器控制台（前端）
- 服务器日志（后端）

**复现条件：**
- 什么操作触发了问题？
- 是否每次都复现？
- 是否有特定的数据或环境？

**环境信息：**
- 浏览器/操作系统版本
- Node/Python 版本
- 数据库状态
- API 响应

### Step 2: 定位问题

**前端调试：**
```bash
# 检查网络请求
# 1. 打开 DevTools -> Network
# 2. 复现问题
# 3. 检查失败的请求

# 检查 React/Vue 组件
# 1. 打开 DevTools -> Components
# 2. 检查 props 和状态

# 添加 console.log
console.log('DEBUG:', variable)
```

**后端调试：**
```python
# 添加日志
import logging
logging.info(f"DEBUG: {variable}")

# 使用调试器
import pdb; pdb.set_trace()

# 或使用 IDE 调试
```

### Step 3: 形成假设

基于收集的信息，提出可能的原因：

**示例：**
- 假设 1：API 返回数据格式不正确
- 假设 2：前端没有正确处理空值
- 假设 3：数据库查询条件错误

### Step 4: 验证假设

**验证方法：**
- 添加日志/断点
- 检查变量值
- 测试边界条件
- 阅读源码

**验证假设 1：**
```typescript
// 检查 API 响应
const response = await fetch('/api/users');
console.log('Response:', response);

// 检查返回数据
const data = await response.json();
console.log('Data:', data);
```

**验证假设 2：**
```typescript
// 检查空值处理
if (users && users.length > 0) {
  // 渲染列表
} else {
  // 显示空状态
}
```

### Step 5: 修复问题

**修复原则：**
- 只改必要的代码
- 保持现有功能不变
- 添加测试防止回归

### Step 6: 验证修复

- 运行相关测试
- 手动测试问题场景
- 检查是否有新的问题

## 常见错误类型

### 前端

| 错误类型 | 可能原因 | 调试方法 |
|----------|----------|----------|
| 组件不渲染 | 条件渲染、props 错误 | DevTools Components |
| API 请求失败 | 网络、权限、参数 | DevTools Network |
| 状态不更新 | 响应式未正确设置 | DevTools Vue/React |
| 样式问题 | CSS 优先级、选择器 | DevTools Elements |

### 后端

| 错误类型 | 可能原因 | 调试方法 |
|----------|----------|----------|
| 500 错误 | 异常未捕获 | 日志/堆栈跟踪 |
| 数据库错误 | SQL 语法、连接 | 查询日志 |
| 验证错误 | Pydantic/类型错误 | 请求体日志 |
| 认证错误 | Token、权限 | 调试中间件 |

## 调试技巧

### 1. 二分查找

如果不确定问题在哪里：
1. 确定一个中间点
2. 检查那里是否正常
3. 缩小范围到有问题的一半
4. 重复

### 2. 对比法

找到正常和异常情况的差异：
- 时间点
- 数据
- 环境
- 用户操作

### 3. 最小复现

创建最简单的代码复现问题：
```typescript
// 原始代码（复杂）
const result = processData(transform(rawData));

// 最小复现
const raw = { /* 简化数据 */ };
const transformed = transform(raw);
const result = processData(transformed);
```

### 4. Rubber Duck Debugging

向他人（或物品）解释代码做了什么，往往能发现隐藏的问题。

## 检查清单

调试时确认：
- [ ] 收集了完整的错误信息
- [ ] 确定了复现条件
- [ ] 提出了可验证的假设
- [ ] 一次只改一个地方
- [ ] 验证了修复有效
- [ ] 检查了没有引入新问题

## 避免的行为

- **不要**盲目修改代码
- **不要**忽略错误消息
- **不要**假设知道原因
- **不要**改多个地方再测试
- **不要**删除测试来"修复"
