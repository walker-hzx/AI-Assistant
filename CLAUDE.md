# AI-Assistant 项目配置

> Claude Code 项目级配置，用于定义项目的整体上下文和开发规范

## 项目概述

AI-Assistant 是一个 Claude Code 插件项目，用于辅助全栈开发。

## 技术栈

- **前端**: Vue 3 + Composition API + TypeScript + TSX + Vite + Pinia + Tailwind CSS
- **后端**: Python + FastAPI + PostgreSQL + SQLAlchemy + Pydantic

## 开发流程

```
需求阶段: discuss → interaction → blueprint
    ↓
规划阶段: brainstorming → writing-plans → planner
    ↓
执行阶段: executing-plans → tdd-guide
    ↓
审查阶段: requesting-code-review → code-review → receiving-code-review
    ↓
验证阶段: verification-before-completion
    ↓
完成阶段: update-blueprint
```

## 核心规范

### 1. 代码组织

- 多个小文件 > 少数大文件
- 高内聚，低耦合
- 通常 200-400 行，最多 800 行
- 按功能/领域组织，而非按类型

### 2. 代码风格

- 变量/函数使用小驼峰 (camelCase)
- 组件使用大驼峰 (PascalCase)
- 常量使用全大写下划线 (UPPER_SNAKE_CASE)
- CSS 类名使用 kebab-case

### 3. 不可变性

始终创建新对象，永不修改现有对象：

```typescript
// 错误
user.name = 'new name'

// 正确
const updatedUser = { ...user, name: 'new name' }
```

### 4. 错误处理

- 在每一层显式处理错误
- 面向 UI 的代码提供用户友好的错误消息
- 服务器端记录详细的错误上下文
- 永不静默吞并错误

### 5. 输入验证

- 在处理前验证所有用户输入
- 使用基于模式的验证（Pydantic, Zod）
- 快速失败并提供清晰的错误消息

### 6. 测试

- TDD: 测试先行
- 80% 最低覆盖率
- 单元测试、集成测试、E2E 测试

### 7. 安全

- 无硬编码密钥
- 敏感数据使用环境变量
- 参数化查询
- 验证所有用户输入

## 目录结构

### 前端

```
src/
├── api/                    # API 接口
├── components/            # 组件
│   ├── common/          # 公共组件
│   └── business/        # 业务组件
├── constants/            # 常量
├── hooks/                # 组合式函数
├── pages/                # 页面
├── router/               # 路由
├── stores/               # Pinia 状态管理
├── styles/               # 样式
├── types/                # 类型定义
└── utils/               # 工具函数
```

### 后端

```
src/
├── api/                    # API 路由
│   ├── deps.py           # 依赖注入
│   └── v1/
│       └── endpoints/    # 端点
├── core/                   # 核心配置
├── models/                # 数据模型
├── schemas/               # Pydantic schemas
├── services/              # 业务逻辑
├── utils/                # 工具函数
└── tests/                # 测试
```

## 可用命令

- `/discuss` - 开始需求讨论
- `/interaction` - 描述交互细节
- `/blueprint` - 更新项目蓝图
- `/plan` - 制定实施计划
- `/review` - 代码审查

## 质量标准

- 函数长度: ≤ 50 行
- 文件大小: ≤ 400 行
- 嵌套层级: ≤ 4 层

## Git 工作流

- 提交信息格式: `<类型>: <描述>`
- 类型: feat, fix, refactor, docs, test, chore, perf, ci
- 合并前需要代码审查
- 所有测试必须通过
