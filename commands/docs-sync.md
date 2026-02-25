---
name: docs-sync
description: 文档同步工具 - 爬取框架/组件库文档
---

# 文档同步

自动从官网爬取框架/组件库文档，生成结构化的 Markdown 使用指南。

## 使用方式

```
/docs-sync
```

## 功能

1. **分析官网结构** - 访问网站，识别组件/API 文档位置
2. **生成爬虫脚本** - 针对网站结构生成 Python + Playwright 爬虫
3. **执行数据爬取** - 获取组件列表、API、示例代码
4. **生成标准文档** - 整理成结构化 Markdown

## 使用方式

用户需要提供：
1. 框架名称（如：Element Plus）
2. 官网地址（如：https://element-plus.org）
3. 包名（如：element-plus）
4. 技术栈（Vue 3 / React / 其他）

## 输出位置

- 爬虫脚本：`scripts/fetch-docs/fetch-{name}.py`
- 生成文档：`docs/frameworks/{name}/`
  - `index.md` - 总览
  - `components/*.md` - 详细组件文档
