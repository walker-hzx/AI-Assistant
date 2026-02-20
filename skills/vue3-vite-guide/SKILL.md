---
name: vue3-vite-guide
description: Vue3 Vite 开发指南 - 提供 Vue3 + TypeScript + Vite 代码规范
---

# Vue3 Vite 开发指南

## 技术栈

- Vue 3.4 + Composition API
- TypeScript + TSX
- Vite 5
- Pinia 3
- Vue Router 4
- Tailwind CSS 3 + Less

## 目录结构

```
src/
├── api/                    # API 接口
├── components/            # 组件
│   ├── common/           # 公共组件（跨项目可用）
│   │   └── Button/
│   │       ├── index.tsx
│   │       └── Button.tsx
│   └── business/         # 业务组件（当前项目通用）
│       └── UserCard/
│           └── index.tsx
├── constants/            # 常量定义
├── hooks/                # 组合式函数（use 开头）
│   └── useUser.ts
├── i18n/                 # 国际化
├── pages/                # 页面
│   └── Home/
│       ├── index.tsx
│       └── components/   # 页面级组件（仅当前页面使用）
│           └── HomeHeader/
│               └── index.tsx
├── router/               # 路由配置
├── stores/               # Pinia 状态管理
├── styles/               # 全局样式
├── types/                # TypeScript 类型定义
└── utils/                # 工具函数
```

## 组件分级与存放

| 级别 | 存放位置 |
|------|----------|
| 页面级 | `pages/页面名/components/组件名/` |
| 项目级 | `components/business/组件名/` |
| 公共级 | `components/common/组件名/` |

## 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 变量/函数 | 小驼峰 | `getUserInfo` |
| 组件文件夹 | 大驼峰 | `UserCard/` |
| 组件文件 | 大驼峰 | `UserCard.tsx` |
| CSS 类名 | kebab-case | `user-card` |
| 常量 | 全大写下划线 | `MAX_RETRY_COUNT` |

## 代码质量标准

- **函数长度**：不超过 50 行
- **文件大小**：不超过 400 行
- **嵌套层级**：不超过 4 层
- **测试覆盖率**：80%

## 注释规范

**通用函数（JSDoc）**：
```typescript
/**
 * @description: 获取用户信息
 * @param {string} userId 用户ID
 * @return {Promise<UserInfo>}
 */
function getUserInfo(userId: string): Promise<UserInfo>
```

**组件内函数**：
```typescript
// 处理用户点击
function handleClick() { ... }
```

## 设计模式

| 场景 | 模式 |
|------|------|
| 状态管理 | Pinia Store |
| 表单处理 | Form + Field |
| 数据获取 | Repository 模式 |
| 依赖注入 | Provide/Inject |

## 组件接口规范

```typescript
interface Props {
  user: User
  showActions?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  showActions: true
})

const emit = defineEmits<{
  edit: [id: string]
  delete: [id: string]
}>()
```

## 交互要求

必须包含的交互：

1. **加载状态**：骨架屏或 loading
2. **操作反馈**：成功/失败提示
3. **空状态**：无数据时的引导
4. **确认对话框**：删除等危险操作

## 测试

- 框架：Vitest
- 覆盖率：80%
- Mock：MSW 或手动 mock
