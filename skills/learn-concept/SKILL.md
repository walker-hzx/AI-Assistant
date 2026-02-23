---
name: learn-concept
description: "搜索学习工具 - 遇到不确定的概念时，搜索并学习"
---

# 搜索学习工具

## 功能

遇到不确定的概念时，搜索并学习。

## 使用场景

- 对话中遇到不懂的概念
- 需要了解新概念/新技术
- 不确定某个术语的含义

## 使用方式

### 1. 搜索概念

运行搜索脚本：

```bash
python skills/learn-concept/scripts/search.py "概念名称"
```

### 2. 优先搜索源

| 源 | 说明 | 适用场景 |
|----|------|----------|
| wikipedia | 维基百科 | 通用概念 |
| mdn | MDN Web Docs | Web 技术 |
| google | Google 搜索 | 其他情况 |

### 3. 工作流程

1. 遇到不确定的概念时，先问用户："要不要我搜索学习一下？"
2. 用户同意后，运行搜索脚本
3. 获取搜索结果 URL
4. 根据 URL 访问学习
5. 汇总后告诉用户

## 搜索脚本

```python
# scripts/search.py
from playwright.sync_api import sync_playwright

# 支持优先搜索：wikipedia -> mdn -> google
```

## 注意事项

- 优先使用维基百科和 MDN
- Google 搜索作为备选
- 搜索结果只作为参考，要基于自己的理解汇总
