---
name: learn-concept
description: "搜索学习工具 - 遇到不确定的概念时，搜索并学习"
model: sonnet
user-invocable: true
---

# 搜索学习工具

## 功能

遇到不确定的概念时，搜索并学习。

## 使用场景

- 对话中遇到不懂的概念
- 需要了解新概念/新技术
- 不确定某个术语的含义

## 使用方式

### 1. 搜索并学习

运行搜索脚本，会自动获取内容：

```bash
python3 ~/.claude/plugins/marketplaces/ai-assistant/skills/learn-concept/scripts/search.py "概念名称"
```

### 2. 优先搜索源

| 源 | 说明 | 适用场景 |
|----|------|----------|
| wikipedia | 维基百科 | 通用概念 |
| mdn | MDN Web Docs | Web 技术 |

### 3. 工作流程

1. 遇到不确定的概念时，先问用户："要不要我搜索学习一下？"
2. 用户同意后，运行搜索脚本
3. **用 Playwright 打开浏览器获取内容**（不是 WebFetch）
4. 提取关键信息
5. 汇总后告诉用户

## 重要：不用 WebFetch

- **不要用 WebFetch** - 会被网络限制
- **用 Playwright** - 本地浏览器，可以翻墙
- 脚本会自动用 Playwright 获取网页内容

## 搜索脚本

```python
# scripts/search.py
from playwright.sync_api import sync_playwright

# 用 Playwright 打开浏览器，获取网页内容
# 优先获取维基百科、MDN 内容
```

## 注意事项

- 优先使用维基百科和 MDN
- 搜索结果直接获取内容，不需要额外请求
- 获取内容后基于自己的理解汇总告诉用户
