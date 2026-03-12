---
name: init
description: "项目初始化 - 扫描项目，生成 CLAUDE.md、蓝图、需求追踪等全局配置"
context: fork
agent: ai-assistant:researcher
---

初始化当前项目的 AI-Assistant 开发配置。

## 任务

扫描项目结构，生成全局上下文文件，让 AI-Assistant 开箱即用。

$ARGUMENTS

## 执行要求

1. 扫描项目文件识别技术栈和目录结构
2. 生成配置草稿（CLAUDE.md、蓝图、需求追踪）
3. 展示草稿供用户确认后再写入
4. 不覆盖已存在的有效配置
