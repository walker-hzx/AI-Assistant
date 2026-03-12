---
name: docs-sync
description: "文档同步 - 抓取框架官方文档，生成结构化使用指南"
context: fork
agent: ai-assistant:scout
---

爬取框架/组件库文档，生成结构化使用指南。

## 目标

$ARGUMENTS

## 流程

1. 访问目标网站，分析文档结构
2. 生成 Python + Playwright 爬虫脚本
3. 执行爬取，获取组件列表、API、代码示例
4. 整理成结构化 Markdown 文档
