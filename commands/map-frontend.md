---
name: map-frontend
description: "前端项目映射 - 扫描前端项目的技术栈、API、组件、样式规范，生成结构化文档，帮助 Claude Code 生成符合预期的代码"
context: fork
agent: ai-assistant:researcher
---

将前端项目的技术栈、API、组件、样式规范梳理清楚，生成 `docs/frontend/` 下的结构化文档。

## 任务

$ARGUMENTS

## 执行要求

1. 解析 focus 参数：`full`（默认）或 `tech` / `api` / `components` / `styling` / `patterns`
2. 根据 focus 探索项目，读取实际文件内容
3. 使用 Write 工具将文档写入 `docs/frontend/` 目录
4. 使用模板填充实际发现的内容，不要留 placeholder

## 文档输出位置

```
docs/frontend/
├── TECH.md         # 技术栈
├── API.md          # API 接口
├── COMPONENTS.md   # 组件库
├── STYLING.md      # 样式规范
└── UI-PATTERNS.md  # UI 模式
```

## 完成后

展示生成的文件列表和关键发现摘要。
