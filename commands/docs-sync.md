---
name: docs-sync
description: "文档同步 - 抓取框架官方文档，生成结构化使用指南"
skill: coordinator
---

# 文档同步

**【重要】此命令通过 Skill 智能调度执行**

使用 `/docs-sync` 爬取框架/组件库文档，coordinator 会智能调度。

## 使用方式

```
/docs-sync
/docs-sync Element Plus, https://element-plus.org
```

## 功能

1. **分析官网结构** - 访问网站，识别组件/API 文档位置
2. **生成爬虫脚本** - 针对网站结构生成 Python + Playwright 爬虫
3. **执行数据爬取** - 获取组件列表、API、示例代码
4. **生成标准文档** - 整理成结构化 Markdown

## 说明

此命令会调用 coordinator，coordinator 会：
- 分析需求
- 决定是否需要 researcher
- 调度合适的角色执行
