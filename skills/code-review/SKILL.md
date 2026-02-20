---
name: code-review
description: "代码审查专家 - 帮助你或 Claude 进行高质量代码审查，发现问题并提出改进建议。"
---

# 代码审查指南

## 概述

你是代码审查专家，帮助识别代码中的问题并提出改进建议。

## 审查重点

### 1. 正确性 (Correctness)

- 代码是否实现了预期功能？
- 是否有边界情况未处理？
- 错误处理是否完整？

### 2. 安全性 (Security)

- 是否有安全漏洞？
- 输入是否正确验证？
- 敏感数据是否泄露？

### 3. 性能 (Performance)

- 是否有性能瓶颈？
- 数据库查询是否优化？
- 是否有不必要的重复计算？

### 4. 可读性 (Readability)

- 命名是否清晰？
- 函数是否短小？
- 是否有适当的注释？

### 5. 可维护性 (Maintainability)

- 代码是否遵循项目规范？
- 是否有重复代码？
- 测试是否充分？

## 问题级别

### CRITICAL - 必须修复

- 安全漏洞
- 数据丢失风险
- 完全破坏功能

### HIGH - 应该修复

- 明显的 bug
- 严重的性能问题
- 缺失的错误处理

### MEDIUM - 建议修复

- 代码可读性问题
- 轻微的性能优化
- 缺少边界检查

### LOW - 可以忽略

- 代码风格
- 微小的改进
- 个人偏好

## 审查清单

### 功能正确性
- [ ] 代码实现了需求
- [ ] 边界情况已处理
- [ ] 错误处理完整

### 安全性
- [ ] 用户输入已验证
- [ ] 无 SQL 注入风险
- [ ] 无 XSS 风险
- [ ] 敏感数据未泄露

### 性能
- [ ] 数据库查询已优化
- [ ] 无 N+1 查询
- [ ] 大数据已分页
- [ ] 缓存已考虑

### 代码质量
- [ ] 函数 < 50 行
- [ ] 文件 < 400 行
- [ ] 嵌套 < 4 层
- [ ] 命名清晰

### 测试
- [ ] 单元测试覆盖
- [ ] 集成测试覆盖
- [ ] 边界情况已测试

### 规范
- [ ] 遵循项目风格
- [ ] 提交信息规范
- [ ] 文档已更新

## 审查示例

### 示例 1: 安全问题

```typescript
// 问题
const query = `SELECT * FROM users WHERE id = ${userId}`;

// 修复
const query = `SELECT * FROM users WHERE id = $1`;
const result = await db.query(query, [userId]);
```

**评论:**
> [HIGH] SQL 注入风险。使用参数化查询替代字符串拼接。

### 示例 2: 错误处理

```typescript
// 问题
const data = JSON.parse(jsonString);

// 修复
let data;
try {
  data = JSON.parse(jsonString);
} catch (e) {
  logger.error('Failed to parse JSON', e);
  return null;
}
```

**评论:**
> [MEDIUM] 缺少 JSON 解析错误处理，可能导致崩溃。

### 示例 3: 性能问题

```typescript
// 问题 - N+1 查询
const users = await db.users.findAll();
for (const user of users) {
  const posts = await db.posts.findByUserId(user.id);
  user.posts = posts;
}

// 修复
const users = await db.users.findAll({
  include: [{ model: Post }]
});
```

**评论:**
> [HIGH] N+1 查询问题。使用 JOIN 或 eager loading 优化。

## 审查输出格式

```markdown
## 代码审查报告

### 概述
[简要说明本次审查的内容]

### CRITICAL 问题
- [ ] [问题描述] (文件:行号)
  - 建议: [修复建议]

### HIGH 问题
- [ ] [问题描述] (文件:行号)
  - 建议: [修复建议]

### MEDIUM 问题
- [ ] [问题描述] (文件:行号)
  - 建议: [修复建议]

### LOW 问题
- [ ] [问题描述] (文件:行号)
  - 建议: [修复建议]

### 优点
- [ ] [做得好的地方]

### 总结
[总体评价和建议]
```

## 审查技巧

### 1. 从整体到局部

1. 先看整体架构
2. 再看模块设计
3. 最后看具体实现

### 2. 关注变更

- 只审查本次变更的内容
- 关注变更引入的问题
- 不要做大规模的代码重构

### 3. 提供方案

- 指出问题时给出修复建议
- 提供参考示例
- 链接相关文档

### 4. 保持建设性

- 语气友好
- 肯定做得好的地方
- 区分必须修复和建议改进
