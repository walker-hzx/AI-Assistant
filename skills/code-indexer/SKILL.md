---
name: code-indexer
description: "代码索引扫描 - 扫描项目代码，生成索引文件，方便复用现有代码"
---

# 代码索引扫描

## 功能

扫描项目代码，生成索引文件，方便在生成代码时知道有哪些可复用的工具函数、组件等。

## 使用场景

- **writing-plans** - 生成计划前扫描索引，确定可复用代码
- **生成代码前** - 知道现有代码，避免重复
- **代码审查时** - 了解项目结构

## 使用方式

### 1. 扫描项目

运行扫描脚本：

```bash
python skills/code-indexer/scripts/scan.py <项目路径>
```

### 2. 生成索引文件

扫描结果会生成两个输出：
- **JSON** - 程序使用
- **Markdown** - 文档形式，保存到 `docs/code-index.md`

### 3. 索引内容

```
docs/code-index.md

## 前端

### 工具函数
- `src/utils/formatDate.ts`
- `src/utils/validateEmail.ts`

### 组件
- `src/components/UserCard.vue`

## 后端

### 服务层
- `src/services/user_service.py`

### 仓储层
- `src/repositories/user_repo.py`
```

## 扫描范围

| 类别 | 路径 | 说明 |
|------|------|------|
| **前端工具函数** | utils/*.ts, helpers/*.ts | 工具函数 |
| **前端组件** | components/**/*.vue | Vue 组件 |
| **前端 API** | api/*.ts, services/*.ts | API 服务 |
| **前端 Hooks** | hooks/*.ts, composables/*.ts | 组合式函数 |
| **后端服务** | services/*.py | 服务层 |
| **后端仓储** | repositories/*.py | 仓储层 |
| **后端模型** | models/*.py | 数据模型 |
| **后端 Schema** | schemas/*.py | Pydantic 模型 |
| **后端 API** | api/**/*.py | API 路由 |

## 工作流程

### 在 writing-plans 中使用

1. 开始创建实施计划前
2. 先扫描项目索引
3. 在计划中标注可复用的代码
4. 生成代码时参考索引

### 增量更新

当项目有新增工具函数/组件时：
1. 重新扫描
2. 更新索引文件

## 注意事项

- 只扫描 src 目录
- 忽略 node_modules、__pycache__ 等
- 索引文件放在 `docs/code-index.md`

## 与其他技能的关系

| 技能 | 关系 |
|------|------|
| **writing-plans** | 生成计划前先扫描索引 |
| **vue3-vite-guide** | 生成前端代码时参考索引 |
| **python-fastapi-guide** | 生成后端代码时参考索引 |
