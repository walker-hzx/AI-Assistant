# 前端项目映射

> 将前端项目的技术栈、API、组件、样式规范梳理清楚，生成结构化文档。帮助 Claude Code 理解项目并生成符合预期的代码。

---

## 使用时机

- **接手前端项目**：需要快速了解项目规范和组件库
- **开始新功能开发**：确保生成的代码符合项目样式和组件用法
- **组件复用**：想使用项目中已有的组件而非重新造轮子
- **样式对齐**：想让 AI 生成的 UI 样式与现有风格一致

---

## 工作流程

### Step 1：解析任务

分析用户输入中的 focus 参数：

| Focus | 文档 | 解决的问题 |
|--------|------|-----------|
| `full` | 全部文档 | 全面了解项目 |
| `tech` | TECH.md | 了解技术栈和依赖 |
| `api` | API.md | 了解前后端接口约定 |
| `components` | COMPONENTS.md | 了解组件库和使用方式 |
| `styling` | STYLING.md | 了解样式规范和设计令牌 |
| `patterns` | UI-PATTERNS.md | 了解常用 UI 模式 |

**默认**：`full`（全部扫描）

---

### Step 2：探索项目

根据 focus 进行探索：

#### `tech` - 技术栈分析

```bash
# 读取 package.json（提取依赖、脚本、框架）
cat package.json

# 查看构建配置
ls vite.config.* tsconfig.json tailwind.config.* postcss.config.* .eslintrc* .prettierrc* 2>/dev/null

# 查看样式配置
cat tailwind.config.js 2>/dev/null || cat tailwind.config.ts 2>/dev/null
```

**识别**：Vue/React、状态管理、路由、UI 库、CSS 方案

#### `api` - API 分析

```bash
# 查找 API 定义文件
ls src/api/ src/services/ src/http/ 2>/dev/null

# 查找 API 调用示例
grep -r "axios\|fetch\|request" src/ --include="*.ts" --include="*.tsx" -l | head -5

# 查找类型定义（API 响应类型）
ls src/types/ src/models/ 2>/dev/null
```

**提取**：API 基础路径、请求封装方式、类型定义

#### `components` - 组件分析

```bash
# 列出所有组件
ls src/components/ src/components/common/ src/components/business/ 2>/dev/null

# 分析组件目录结构
find src/components -name "*.vue" -o -name "*.tsx" | head -20

# 查看组合式函数（hooks）
ls src/hooks/ src/composables/ 2>/dev/null
```

**提取**：每个组件的用途、Props 定义、使用示例

#### `styling` - 样式分析

```bash
# 查看全局样式
ls src/styles/ src/assets/styles/ 2>/dev/null

# 查找 CSS 变量 / 设计令牌
grep -r "CSS\|:root\|--tw-" src/ --include="*.css" --include="*.scss" --include="*.vue" | head -30

# 查看 Tailwind 扩展配置
cat tailwind.config.* 2>/dev/null | grep -A 20 "theme\|extend"

# 查找常用样式工具类
grep -r "class=\|className=" src/ --include="*.vue" --include="*.tsx" | head -20
```

**提取**：设计令牌、CSS 变量、Tailwind 扩展、常用类名

#### `patterns` - UI 模式分析

```bash
# 查找页面组件
ls src/pages/ src/views/ 2>/dev/null

# 分析复杂组件（寻找可复用的子组件）
grep -r "const.*=.*define" src/components/ --include="*.vue" --include="*.tsx" | head -20

# 查看组合式函数模式
cat src/hooks/use*.ts src/composables/*.ts 2>/dev/null | head -100
```

**提取**：布局模式、表单处理、数据展示模式

---

### Step 3：写入文档

将文档写入 `docs/frontend/` 目录：

```
docs/frontend/
├── TECH.md         # 技术栈
├── API.md          # API 接口
├── COMPONENTS.md   # 组件库
├── STYLING.md      # 样式规范
└── UI-PATTERNS.md  # UI 模式
```

**使用 Write 工具直接写入，不要用 heredoc。**

---

### Step 4：确认完成

```
✅ 前端项目映射完成！

生成文档：
- docs/frontend/TECH.md（技术栈）
- docs/frontend/API.md（API 接口）
- docs/frontend/COMPONENTS.md（组件库）
- docs/frontend/STYLING.md（样式规范）
- docs/frontend/UI-PATTERNS.md（UI 模式）

后续使用：
- /implement - 开发功能时，Claude Code 会参考这些文档
- /review - 代码审查时检查是否符合规范
```

---

## 文档模板

### TECH.md - 技术栈

```markdown
# 前端技术栈

**分析日期：** YYYY-MM-DD

## 框架与核心库

**框架：** [Vue 3 / React 18 / ...]
**版本：** [版本号]
**UI 库：** [Element Plus / Ant Design / Headless UI / ...]

## 状态管理

**方案：** [Pinia / Vuex / Zustand / Redux / ...]
**位置：** `src/stores/` / `src/store/`

## 路由

**方案：** [Vue Router / React Router]
**配置：** `src/router/` / `src/routes/`

## HTTP 请求

**方案：** [axios / ky / fetch]
**封装位置：** `src/api/` / `src/services/`

## CSS 方案

**方案：** [Tailwind CSS / SCSS / CSS Modules / UnoCSS / ...]
**配置文件：** `tailwind.config.*` / `vite.config.ts`

## 构建工具

**工具：** Vite / Webpack / ...
**版本：** [版本号]

## 关键依赖

| 包名 | 版本 | 用途 |
|------|------|------|
| | | |

## 开发命令

```bash
npm run dev      # 开发服务器
npm run build   # 生产构建
npm run lint    # 代码检查
```

## 环境变量

| 变量 | 说明 |
|------|------|
| VITE_API_BASE | API 基础路径 |
```

### API.md - API 接口

```markdown
# API 接口规范

**分析日期：** YYYY-MM-DD

## 基础配置

**Base URL：** `/api/v1`（从环境变量 `VITE_API_BASE` 读取）
**请求封装：** `src/api/request.ts`（基于 axios）

## 请求封装

**通用配置：**
```typescript
// 请求拦截器：添加 token
// 响应拦截器：统一错误处理
```

## 接口模块

### 用户模块

**列表接口：** `GET /users`
```typescript
// 请求参数
interface UserListParams {
  page: number
  pageSize: number
}

// 响应类型
interface UserListResponse {
  data: User[]
  total: number
}
```

**详情接口：** `GET /users/:id`

### [其他模块...]

## 数据模型

```typescript
// 用户
interface User {
  id: string
  name: string
  email: string
  avatar?: string
  createdAt: string
}
```

## 错误处理

**状态码约定：**
- `200` - 成功
- `401` - 未登录
- `403` - 无权限
- `404` - 资源不存在
- `500` - 服务器错误

**统一错误响应：**
```typescript
interface ApiError {
  code: string
  message: string
}
```
```

### COMPONENTS.md - 组件库

```markdown
# 组件库

**分析日期：** YYYY-MM-DD

## 目录结构

```
src/components/
├── common/       # 通用组件（Button, Input, Modal...）
├── business/      # 业务组件（UserCard, OrderList...）
└── layout/       # 布局组件（Header, Sidebar...）
```

## 通用组件

### Button

**文件：** `src/components/common/Button.vue`
**用途：** 按钮，支持多种类型和尺寸

**Props：**
```typescript
interface ButtonProps {
  type?: 'primary' | 'secondary' | 'danger' | 'text'
  size?: 'small' | 'medium' | 'large'
  disabled?: boolean
  loading?: boolean
}
```

**使用示例：**
```vue
<Button type="primary" size="medium">确认</Button>
<Button type="text" loading>加载中</Button>
```

### Input

**文件：** `src/components/common/Input.vue`
**用途：** 输入框

**Props：**
```typescript
interface InputProps {
  modelValue: string
  placeholder?: string
  type?: 'text' | 'password' | 'email'
  error?: string
}
```

**使用示例：**
```vue
<Input v-model="form.name" placeholder="请输入名称" error="名称不能为空" />
```

### Modal

**文件：** `src/components/common/Modal.vue`
**用途：** 模态框

**Props：**
```typescript
interface ModalProps {
  modelValue: boolean
  title?: string
  width?: string
}
```

**使用示例：**
```vue
<Modal v-model="showModal" title="编辑用户">
  <!-- 弹窗内容 -->
</Modal>
```

## 业务组件

### [组件名]

**文件：** `src/components/business/[ComponentName].vue`
**用途：** [描述]

**使用示例：**
```vue
<[ComponentName] [props] />
```
```

### STYLING.md - 样式规范

```markdown
# 样式规范

**分析日期：** YYYY-MM-DD

## CSS 方案

**方案：** Tailwind CSS
**配置：** `tailwind.config.js`

## 设计令牌

### 颜色

```css
:root {
  --color-primary: #3b82f6;
  --color-secondary: #64748b;
  --color-success: #22c55e;
  --color-warning: #f59e0b;
  --color-danger: #ef4444;
  --color-bg: #ffffff;
  --color-bg-secondary: #f8fafc;
  --color-text: #1e293b;
  --color-text-secondary: #64748b;
}
```

### 间距

```css
--space-xs: 4px;
--space-sm: 8px;
--space-md: 16px;
--space-lg: 24px;
--space-xl: 32px;
```

### 圆角

```css
--radius-sm: 4px;
--radius-md: 8px;
--radius-lg: 12px;
--radius-full: 9999px;
```

### 阴影

```css
--shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
--shadow-md: 0 4px 6px rgba(0,0,0,0.1);
--shadow-lg: 0 10px 15px rgba(0,0,0,0.1);
```

## Tailwind 扩展

### 自定义颜色

```js
// tailwind.config.js
colors: {
  brand: {
    50: '#eff6ff',
    500: '#3b82f6',
    900: '#1e3a8a',
  }
}
```

### 自定义间距

```js
spacing: {
  '18': '4.5rem',
  '88': '22rem',
}
```

## 常用类名模式

### 按钮样式
```html
<!-- 主按钮 -->
<button class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600">

<!-- 次要按钮 -->
<button class="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50">

<!-- 危险按钮 -->
<button class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600">
```

### 卡片样式
```html
<div class="bg-white rounded-lg shadow-md p-6">
  <!-- 卡片内容 -->
</div>
```

### 表单样式
```html
<input class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
```

## 响应式断点

| 断点 | 类名前缀 | 尺寸 |
|------|----------|------|
| 移动端 | 默认 | < 640px |
| 平板 | sm: | ≥ 640px |
| 桌面 | md: | ≥ 768px |
| 大屏 | lg: | ≥ 1024px |
| 超大屏 | xl: | ≥ 1280px |

## 注意事项

- 使用 `flex` 布局时优先用 `gap-*` 而非手动 `margin`
- 颜色使用 Tailwind 预设色板中的命名
- 阴影优先使用预设 shadow
```
```

### UI-PATTERNS.md - UI 模式

```markdown
# UI 模式

**分析日期：** YYYY-MM-DD

## 页面布局

### 基础布局

```
+----------------------------------+
|           Header (固定)           |
+--------+-------------------------+
|        |                         |
| Sidebar|        Main Content     |
| (固定) |                         |
|        |                         |
+--------+-------------------------+
```

**实现：** `src/components/layout/BasicLayout.vue`

### 列表页布局

```
+----------------------------------+
|  搜索区域                         |
+----------------------------------+
|  操作栏（新增、批量操作）          |
+----------------------------------+
|  表格 / 列表                      |
+----------------------------------+
|  分页                            |
+----------------------------------+
```

## 数据展示

### 表格

**组件：** `src/components/common/Table.vue`

**使用模式：**
```vue
<Table :data="tableData" :columns="columns" :loading="loading">
  <template #action="{ row }">
    <Button size="small" @click="handleEdit(row)">编辑</Button>
    <Button size="small" type="danger" @click="handleDelete(row)">删除</Button>
  </template>
</Table>
```

### 空状态

**模式：**
```vue
<div v-if="data.length === 0" class="text-center py-12">
  <EmptyState icon="inbox" message="暂无数据" />
</div>
```

## 表单处理

### 基础表单

**模式：**
```vue
<Form :model="form" :rules="rules" @submit="handleSubmit">
  <FormItem label="名称" prop="name">
    <Input v-model="form.name" />
  </FormItem>
</Form>
```

### 表单验证

**规则定义：**
```typescript
const rules = {
  name: [
    { required: true, message: '请输入名称' },
    { min: 2, max: 20, message: '长度在 2-20 个字符' }
  ],
  email: [
    { required: true, message: '请输入邮箱' },
    { type: 'email', message: '请输入正确的邮箱格式' }
  ]
}
```

## 状态处理

### 加载状态

```vue
<!-- 骨架屏 -->
<Skeleton :rows="5" v-if="loading" />

<!-- 或加载指示器 -->
<div v-if="loading" class="flex justify-center py-8">
  <LoadingSpinner />
</div>
```

### 错误状态

```vue
<ErrorState message="加载失败" @retry="fetchData" />
```

### 成功反馈

```typescript
// 使用消息提示
message.success('操作成功')
message.error('操作失败')
```

## 交互模式

### 确认对话框

```typescript
const handleDelete = (row) => {
  ElMessageBox.confirm('确定要删除吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    // 执行删除
  })
}
```

### 表格行操作

**原则：**
- 主要操作放行内（编辑、删除）
- 批量操作放操作栏
- 危险操作需要确认

---

## 检查清单

- [ ] TECH.md 生成（技术栈）
- [ ] API.md 生成（API 接口）
- [ ] COMPONENTS.md 生成（组件库）
- [ ] STYLING.md 生成（样式规范）
- [ ] UI-PATTERNS.md 生成（UI 模式）

---

## 关键原则

1. **使用现有组件**：开发前先查看 COMPONENTS.md，优先使用已有的组件
2. **遵循样式规范**：按照 STYLING.md 中的设计令牌和类名模式
3. **复用 UI 模式**：参考 UI-PATTERNS.md 中的模式，而非重新发明
4. **保持组件拆分**：单文件超过 200 行考虑拆分
