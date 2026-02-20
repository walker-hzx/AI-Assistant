---
name: requesting-code-review
description: 在完成任务、实现主要功能或合并前使用，以验证工作是否符合要求
---

# 请求代码审查

## 概述

派遣 code-reviewer 子代理进行代码审查，在问题蔓延之前捕获它们。

**核心原则：** 尽早审查，频繁审查。

## 何时请求审查

**必须审查：**
- 完成主要功能后
- 合并到 main 分支前
- 提交 PR 前

**可选但有价值：**
- 遇到困难时（获得新视角）
- 重构前（基线检查）
- 修复复杂 bug 后

## 如何请求

**1. 获取 git 信息：**
```bash
BASE_SHA=$(git rev-parse HEAD~1)
HEAD_SHA=$(git rev-parse HEAD)
```

**2. 调用 code-reviewer agent：**

```bash
Task: code-reviewer
描述: 审查刚完成的用户登录功能
```

## 审查内容

### 必须检查
- [ ] 功能正确性
- [ ] 代码安全性
- [ ] 错误处理
- [ ] 测试覆盖

### 建议检查
- [ ] 代码可读性
- [ ] 命名规范
- [ ] 性能考虑
- [ ] 文档更新
