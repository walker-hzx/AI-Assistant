# AI-Assistant 配置规范草稿

> 正在不断完善中...
> 创建时间：2026-02-19

---

## 一、技术栈

### 1.1 前端技术栈

| 类别 | 技术 |
|------|------|
| 框架 | Vue 3.4 + Composition API |
| 语言 | TypeScript + TSX |
| 构建 | Vite 5 |
| 状态 | Pinia 3 |
| 路由 | Vue Router 4 |
| 样式 | Tailwind CSS 3 + Less |
| 工具 | ESLint + Prettier |
| HTTP | Fetch |
| i18n | vue-i18n 9 |
| 测试 | Vitest |
| E2E | Agent Browser (Vercel) |

### 1.2 后端技术栈

| 类别 | 技术 |
|------|------|
| 语言 | Python |
| 框架 | FastAPI |
| 数据库 | PostgreSQL |
| AI 框架 | LangGraph |

---

## 二、目录结构

### 2.1 前端目录结构

```
src/
├── api/              # API 接口
├── components/       # 组件
│   ├── common/       # 公共组件（跨项目可用）
│   │   └── Button/
│   │       ├── index.tsx
│   │       └── Button.tsx
│   └── business/     # 业务组件（当前项目通用）
│       └── UserCard/
│           └── index.tsx
├── constants/        # 常量定义
├── hooks/            # 组合式函数（use开头）
│   └── useUser.ts
├── i18n/             # 国际化
├── pages/            # 页面
│   └── Home/
│       ├── index.tsx
│       └── components/  # 页面级组件（仅当前页面使用）
│           └── HomeHeader/
│               └── index.tsx
├── router/           # 路由配置
├── stores/           # Pinia 状态管理
├── styles/           # 全局样式
├── types/            # TypeScript 类型定义
└── utils/            # 工具函数
```

### 2.2 后端目录结构（Python/FastAPI）

```
src/
├── api/                    # API 路由
│   ├── __init__.py
│   ├── deps.py             # 依赖注入
│   ├── middleware/         # 中间件
│   │   └── __init__.py
│   └── v1/                 # API v1 版本
│       ├── __init__.py
│       ├── endpoints/       # 端点
│       │   ├── __init__.py
│       │   ├── users.py
│       │   └── items.py
│       └── router.py       # 路由汇总
├── core/                   # 核心配置
│   ├── __init__.py
│   ├── config.py           # 配置管理
│   ├── security.py         # 安全相关
│   └── database.py         # 数据库连接
├── models/                 # 数据模型（SQLAlchemy）
│   ├── __init__.py
│   ├── user.py
│   └── item.py
├── schemas/                # Pydantic schemas
│   ├── __init__.py
│   ├── user.py
│   └── item.py
├── services/               # 业务逻辑
│   ├── __init__.py
│   ├── user_service.py
│   └── item_service.py
├── utils/                 # 工具函数
│   ├── __init__.py
│   └── helpers.py
├── constants/              # 常量定义
│   └── __init__.py
├── tests/                  # 测试
│   ├── __init__.py
│   ├── conftest.py
│   ├── api/
│   ├── services/
│   └── utils/
├── main.py                 # 应用入口
├── requirements.txt        # 依赖
├── alembic.ini             # 数据库迁移
└── .env                   # 环境变量
```

---

## 三、代码规范

### 3.1 前端命名规范（TypeScript/Vue）

| 类型 | 规范 | 示例 |
|------|------|------|
| 变量/函数 | 小驼峰 (camelCase) | `getUserInfo`, `userName` |
| 组件文件夹 | 大驼峰 (PascalCase) | `UserCard/` |
| 组件文件 | 大驼峰 (PascalCase) | `UserCard.tsx` |
| CSS 类名 |  kebab-case | `user-card` |
| 常量 | 全大写 + 下划线 | `MAX_RETRY_COUNT` |

### 3.2 后端命名规范（Python）

| 类型 | 规范 | 示例 |
|------|------|------|
| 变量/函数 | 小写下划线 (snake_case) | `get_user_info`, `user_name` |
| 类名 | 大驼峰 (PascalCase) | `UserService`, `ItemModel` |
| 数据库表名 | 小写下划线 + 复数 | `users`, `user_items` |
| API 路径 | 小写下划线 + 复数 | `/users`, `/user-items` |
| 常量 | 全大写 + 下划线 | `MAX_RETRY_COUNT` |
| 私有变量/函数 | 单下划线前缀 | `_private_function` |

### 3.2 组件分级与存放位置

| 级别 | 描述 | 存放位置 |
|------|------|----------|
| 页面级 | 仅当前页面使用 | `pages/页面名/components/组件名/` |
| 项目级 | 当前项目通用 | `components/business/组件名/` |
| 公共级 | 跨项目可用 | `components/common/组件名/` |

### 3.3 组件设计原则

#### 3.3.1 组件提取时机

当出现以下情况时，考虑提取组件：

1. **重复代码**：相同或类似的代码出现 2 次以上
2. **单一职责**：组件只做一件事
3. **可复用性**：可能在其他地方重复使用
4. **复杂度**：组件代码超过 200 行
5. **可测试性**：业务逻辑可以独立测试

#### 3.3.2 组件接口规范

```typescript
// 组件 props 接口
interface UserCardProps {
  userId: string
  name: string
  avatar?: string
  showActions?: boolean  // 可选 props 放后面
}

// 组件事件
interface UserCardEvents {
  onEdit: (userId: string) => void
  onDelete: (userId: string) => void
}

// 组合式函数类型
interface UseUserListReturn {
  users: Ref<User[]>
  loading: Ref<boolean>
  fetchUsers: () => Promise<void>
}
```

#### 3.3.3 组件文档

```vue
<!-- UserCard 用户卡片组件 -->
<!-- 用于展示用户基本信息，包含头像、名称、操作按钮 -->
<!-- -->
<!-- @see /docs/components.md 组件设计规范 -->

<script setup lang="ts">
// props
interface Props {
  user: User
  showActions?: boolean
}
const props = withDefaults(defineProps<Props>(), {
  showActions: true
})

// emits
const emit = defineEmits<{
  edit: [id: string]
  delete: [id: string]
}>()
</script>
```

### 3.4 设计模式使用

#### 3.4.1 常用设计模式

| 场景 | 推荐模式 | 说明 |
|------|----------|------|
| 状态管理 | Pinia Store | 全局状态 |
| 表单处理 | Form + Field 模式 | 表单验证 |
| 列表管理 | Repository 模式 | 数据获取/缓存 |
| API 调用 | Repository 模式 | 数据抽象 |
| 依赖注入 | Provide/Inject | 跨组件通信 |
| 权限控制 | HOC (高阶组件) | 权限封装 |
| 列表筛选 | Strategy 模式 | 不同筛选策略 |
| 排序/分页 | Strategy 模式 | 排序算法切换 |

#### 3.4.2 组合式函数（Composables）

```
提取逻辑时优先使用组合式函数：

useUser.ts        # 用户相关逻辑
usePagination.ts   # 分页逻辑
useDebounce.ts    # 防抖
useLocalStorage.ts # 本地存储
```

#### 3.4.3 耦合度控制

- **props/emits**：父子组件通过 props 向下传递，emits 向上传递
- **依赖注入**：跨级组件通信使用 provide/inject
- **状态管理**：全局状态使用 Pinia，避免直接修改
- **API 抽象**：通过 repository 模式隔离 API 逻辑

```typescript
// ✅ 好的实践：通过 props 传递
const props = defineProps<{ user: User }>()

// ✅ 好的实践：通过 emits 通知
const emit = defineEmits<{ update: [user: User] }>()

// ❌ 避免：直接修改 props
props.user.name = 'new name'  // 错误！

// ❌ 避免：组件直接调用 API
await api.getUsers()  // 错误！应该通过 props 或 store
```

### 3.5 注释规范

**通用/全局函数（JSDoc 格式）**：
```typescript
/**
 * @description: 获取用户信息
 * @param {string} userId 用户ID
 * @return {Promise<UserInfo>} 用户信息
 */
function getUserInfo(userId: string): Promise<UserInfo>
```

**组件内函数**：
```typescript
// 处理用户点击事件
function handleClick() { ... }
```

### 3.4 代码质量标准

- **函数长度**：不超过 50 行
- **文件大小**：不超过 400 行
- **嵌套层级**：不超过 4 层
- **测试覆盖率**：80%

### 3.5 后端设计模式（Python/FastAPI）

#### 3.5.1 分层架构

```
API 层 (endpoints/)     → 处理请求/响应，调用 Service
    ↓
Service 层 (services/)  → 业务逻辑，事务管理
    ↓
Repository 层 (repositories/) → 数据访问抽象
    ↓
Model 层 (models/)     → 数据库模型
```

#### 3.5.2 Repository 模式

```python
# repositories/user_repository.py
class UserRepository:
    """用户数据访问层"""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
```

#### 3.5.3 Service 层规范

```python
# services/user_service.py
class UserService:
    """用户服务层 - 业务逻辑"""

    def __init__(self, user_repository: UserRepository):
        self.user_repo = user_repository

    def get_user(self, user_id: int) -> User:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User {user_id} not found")
        return user

    def create_user(self, user_data: CreateUserSchema) -> User:
        # 业务逻辑：验证邮箱是否存在
        existing = self.user_repo.get_by_email(user_data.email)
        if existing:
            raise UserAlreadyExistsError("Email already registered")

        # 创建用户
        user = User(email=user_data.email, name=user_data.name)
        return self.user_repo.create(user)
```

#### 3.5.4 依赖注入

```python
# api/deps.py
def get_user_repository() -> UserRepository:
    """依赖注入：用户仓库"""
    db = Depends(get_db)
    return UserRepository(db)

def get_user_service(
    user_repo: UserRepository = Depends(get_user_repository)
) -> UserService:
    """依赖注入：用户服务"""
    return UserService(user_repo)

# 使用
@router.post("/users", response_model=UserSchema)
def create_user(
    user_data: CreateUserSchema,
    user_service: UserService = Depends(get_user_service)
):
    return user_service.create_user(user_data)
```

#### 3.5.5 常用设计模式

| 场景 | 模式 | 说明 |
|------|------|------|
| 数据访问 | Repository | 抽象数据库操作 |
| 业务逻辑 | Service | 业务规则、事务 |
| 依赖注入 | DI (Depends) | 解耦依赖 |
| 配置管理 | Settings | 集中配置 |
| 错误处理 | Exception Handler | 统一异常处理 |
| 认证/授权 | Dependency | Token 验证、权限检查 |
| 缓存 | Cache | 缓存抽象 |

#### 3.5.6 提取时机

当出现以下情况时，考虑提取：

1. **重复数据库操作**：相同的查询出现 2 次以上 → 提取到 Repository
2. **业务逻辑复杂**：超过 50 行 → 拆分到多个 Service 方法
3. **可复用**：某个功能可能在多个地方使用 → 提取为独立 Service
4. **可测试**：业务逻辑需要单独测试 → 从 API 层分离

#### 3.5.7 耦合度控制

```python
# ✅ 好的实践：依赖抽象接口
class UserService:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

# ❌ 避免：直接依赖具体实现
class UserService:
    def __init__(self, db: Session):
        self.db = db  # 直接操作数据库
```

#### 3.5.8 API Endpoint 规范

```python
# api/v1/endpoints/users.py
router = APIRouter(prefix="/users", tags=["用户管理"])

@router.get("", response_model=List[UserSchema])
def list_users(
    skip: int = 0,
    limit: int = 100,
    user_service: UserService = Depends(get_user_service)
):
    """获取用户列表"""
    return user_service.list_users(skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserSchema)
def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    """获取单个用户"""
    return user_service.get_user(user_id)

@router.post("", response_model=UserSchema, status_code=201)
def create_user(
    user_data: CreateUserSchema,
    user_service: UserService = Depends(get_user_service)
):
    """创建用户"""
    return user_service.create_user(user_data)
```

### 3.6 Python 注释规范

**模块/函数文档字符串**：
```python
def get_user_by_id(user_id: int) -> User | None:
    """
    根据用户ID获取用户信息

    Args:
        user_id: 用户ID

    Returns:
        User: 用户信息，如果不存在返回 None

    Raises:
        ValueError: user_id 无效时
    """
```

**类文档字符串**：
```python
class UserService:
    """
    用户服务类

    负责处理用户的增删改查等业务逻辑

    Attributes:
        db: 数据库会话实例
    """

    def __init__(self, db: Session):
        self.db = db
```

### 3.6 FastAPI 路由规范

- 路由文件放 `api/v1/endpoints/`
- 使用 `APIRouter` 分组
- 路径使用小写下划线：`/user-items`
- HTTP 方法：GET（查询）、POST（创建）、PUT（更新）、DELETE（删除）
- 依赖注入使用 `Depends`

### 3.7 日志规范

使用 Python `logging` 模块，结构化日志：

```python
import logging
from logging import Logger

# 配置日志格式
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# 日志级别：DEBUG, INFO, WARNING, ERROR, CRITICAL
LEVEL = "INFO"
```

**日志输出**：
- 开发环境：控制台输出（彩色）
- 生产环境：文件 + 控制台

**使用方式**：
```python
logger = logging.getLogger(__name__)
logger.info("用户登录成功")
logger.error("数据库连接失败", extra={"user_id": 123})
```

### 3.8 环境变量管理

使用 `pydantic-settings` + `python-dotenv`：

```python
# .env 文件示例
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
API_KEY=your-api-key-here
DEBUG=true
LOG_LEVEL=INFO
```

**配置类**：
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    api_key: str
    debug: bool = False
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
```

### 3.9 安全规范

- **敏感信息**：禁止硬编码，使用环境变量
- **密码加密**：使用 bcrypt
- **API 认证**：JWT Token
- **CORS**：配置允许的域名
- **限流**：使用 SlowAPI
- **输入验证**：Pydantic models

### 3.10 错误处理

统一错误响应格式：

```python
from pydantic import BaseModel

class ErrorResponse(BaseModel):
    error: str
    detail: str | None = None
    code: int = 400
```

---

## 四、AI Agent 沟通规范

### 4.0.1 为什么要规范沟通

- AI 不是肚子里的蛔虫，需要明确表达
- 好的描述 = 好的结果
- 不同阶段需要不同详细程度的描述

### 4.0.2 沟通原则

| 原则 | 说明 | 示例 |
|------|------|------|
| **具体** | 不要说"做个登录"，要说"邮箱+密码登录，错误提示要明确" | ❌ "做个登录" → ✅ "邮箱+密码登录，密码错误提示'密码错误'，登录成功后跳转 /dashboard" |
| **分阶段** | 需求阶段说需求，交互阶段说交互 | 需求："做一个用户管理" → 交互："点击新建弹出Modal" |
| **带参考** | 给 AI 参考例子，比文字描述更有效 | "参考 Ant Design Pro 的用户列表页" |
| **有反馈** | AI 做完后，明确告诉哪里不对 | "按钮颜色错了，应该是 #1890ff" |

### 4.0.3 需求描述模板

**模板**：
```markdown
## 功能：功能名称

### 核心需求
1. ...（最重要的 1-2 句）
2. ...

### 详细需求
- 场景 1：...
- 场景 2：...

### 参考
- 参考项目/页面：...
- 类似的现有功能：...

### 不需要
- （可选）明确告诉 AI 不需要做什么，避免过度实现
```

**示例**：
```markdown
## 功能：用户登录

### 核心需求
1. 用户输入邮箱和密码登录
2. 登录成功跳转首页，失败显示错误

### 详细需求
- 输入验证：邮箱格式、密码非空
- 错误提示："邮箱或密码错误"
- 登录成功后保存 token 到 localStorage

### 参考
- 参考：https://ant.design/components/form-cn/

### 不需要
- 不需要"记住我"功能
- 不需要社交登录
```

### 4.0.4 交互描述模板

**模板**：
```markdown
## 交互：页面名称/组件名称

### 加载状态
- 初始加载：显示骨架屏
- 加载时间 > 1s：顶部显示加载条

### 用户操作
- 点击 X：显示 Y
- 成功后：Toast 提示"成功"，1 秒后消失
- 失败后：Modal 显示错误信息

### 空状态
- 无数据时：显示"暂无数据" + 新建按钮

### 动画
- Modal 打开：从上滑入，300ms
- 按钮 hover：背景色加深
```

**示例**：
```markdown
## 交互：用户列表页

### 加载状态
- 表格显示骨架屏

### 用户操作
- 点击"新建"按钮：弹出 Modal 表单
- 点击表格行编辑按钮：弹出 Modal 表单（填充数据）
- 点击删除按钮：弹出确认框，确认后删除并刷新

### 反馈
- 成功：Toast 绿色提示
- 失败：Modal 红色错误提示

### 空状态
- 无数据：显示"暂无用户" + "新建用户"按钮
```

### 4.0.5 反馈修改模板

**AI 生成后，这样反馈**：

```markdown
问题 1：布局不对
- 描述：侧边栏应该在左边，内容在右边
- 正确布局：[示意图或参考]

问题 2：颜色不对
- 描述：主色应该是 #1890ff（蓝色），不是灰色

问题 3：交互缺失
- 描述：点击按钮没有反应，需要弹出确认框

问题 4：代码问题
- 描述：TypeScript 类型错误，User 缺少 id 字段
```

### 4.0.6 沟通检查清单

**需求沟通时检查**：
- [ ] 我说清楚"做什么"了吗？
- [ ] 有具体的场景吗？
- [ ] 有参考示例吗？

**交互沟通时检查**：
- [ ] 加载状态描述了吗？
- [ ] 操作反馈描述了吗？
- [ ] 成功/失败状态都说了吗？

**反馈修改时检查**：
- [ ] 问题描述具体吗？
- [ ] 有正确 vs 错误的对比吗？

---

## 四、工作流规范

### 4.1 完整开发流程（AI Agent 场景）

```
┌─────────────────────────────────────────────────────────────────┐
│                        完整开发流程                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 需求沟通与细化                                                │
│     └── 头脑风暴 → 不断提问澄清 → 需求文档（不讨论交互）         │
│                         ↓                                       │
│  2. 基础交互描述                                                  │
│     └── 需求明确后再做                                           │
│     └── 核心交互描述（加载、反馈、空状态、确认）                  │
│     └── 这相当于"文字版原型"                                     │
│                         ↓                                       │
│  3. 技术方案设计                                                  │
│     └── 架构设计 → 技术选型 → 接口设计 → 方案评审                │
│                         ↓                                       │
│  4. 详细计划制定                                                  │
│     └── 任务分解 → 时间估算 → 依赖分析 → 计划确认               │
│                         ↓                                       │
│  5. 编码实现（TDD）                                               │
│     └── 写测试 → 写实现 → 重构                                   │
│                         ↓                                       │
│  6. 交互优化（可选）                                              │
│     └── MVP 完成后完善动效细节                                    │
│                         ↓                                       │
│  7. 代码审查                                                      │
│     └── 自审 → 交叉审查 → 修改确认                               │
│                         ↓                                       │
│  8. 测试验证                                                      │
│     └── 单元测试 → 集成测试 → E2E 测试                           │
│                         ↓                                       │
│  9. 部署上线                                                      │
│     └── 构建 → 部署 → 验证                                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**关键原则**：
- **阶段 1（需求沟通）**：只讨论"做什么"，不讨论"怎么做交互"
- **阶段 2（交互描述）**：需求明确后再做，相当于文字版原型
- **阶段 3（计划）**：需求 + 交互都明确后再做计划
- **持续更新蓝图**：每个关键节点都更新 docs/蓝图.md

### 4.2 需求沟通与细化
### 4.2 需求沟通与细化

#### 4.2.1 需求思考框架（8 维度）

每个需求都从以下 8 个维度思考，确保需求闭环但不过度设计：

```
┌─────────────────────────────────────────────────────────────────┐
│                      需求思考 8 维度                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 【目标】解决什么问题？为谁解决？价值是什么？                   │
│  2. 【功能】核心功能是什么？必须有哪些功能？可以没有哪些？         │
│  3. 【流程】用户如何完成这个任务？每一步是什么？                   │
│  4. 【数据】需要什么数据？输入什么？输出什么？如何存储？           │
│  5. 【异常】出错时怎么办？网络断了？数据不存在？权限不足？         │
│  6. 【边界】极端情况？空数据？大数据量？超长文本？                 │
│  7. 【安全】谁可以用？需要登录吗？敏感数据怎么处理？               │
│  8. 【性能】响应时间要求？并发用户多少？数据量多大？               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**重要原则**：
- **MVP 优先**：第一版只实现核心功能（维度 1-3）
- **渐进增强**：后续迭代再补充其他维度
- **避免过度设计**：不确定的功能留到后期，不要一次性做完美

#### 4.2.2 需求拆分策略

| 版本 | 目标 | 包含内容 |
|------|------|----------|
| **V0.1 (MVP)** | 能用 | 核心流程 + 正常场景 |
| **V0.2** | 好用 | 异常处理 + 边界情况 |
| **V0.3** | 健壮 | 性能优化 + 安全加固 |
| **V1.0** | 完善 | 完整功能 + 文档 |

**示例**：用户注册功能
- V0.1：邮箱 + 密码注册，正常流程
- V0.2：邮箱验证、密码强度检查、错误提示
- V0.3：防刷机制、验证码、性能优化
- V1.0：手机号注册、第三方登录、完整文档

#### 4.2.3 需求沟通原则

**核心原则**：不确定就问，直到完全理解

| 原则 | 说明 | 示例 |
|------|------|------|
| **明确性** | 需求必须具体、可衡量 | ❌ "做个用户管理" → ✅ "实现用户的增删改查，支持分页和搜索" |
| **完整性** | 覆盖所有场景和边界 | 正常流程 + 异常流程 + 边界条件 |
| **可行性** | 技术可实现，时间可控 | 评估技术难点和风险 |
| **一致性** | 与现有系统兼容 | 检查与现有功能的冲突 |

#### 4.2.4 需求细化流程

```
初次沟通 → 提出假设 → 提问澄清 → 记录需求 → 确认理解 → 编写文档
    ↑                                                              ↓
    └──────────────── 如有疑问，再次沟通 ← 评审确认 ← 方案设计 ←─┘
```

#### 4.2.3 提问模板

**功能性问题**：
- 这个功能要解决什么问题？
- 目标用户是谁？
- 核心操作流程是什么？
- 有哪些输入和输出？
- 成功和失败的状态分别是什么？

**非功能性问题**：
- 性能要求（响应时间、并发量）？
- 安全要求（权限控制、数据加密）？
- 兼容性要求（浏览器、设备）？
- 扩展性要求（未来可能的变化）？

**边界情况**：
- 没有数据时怎么处理？
- 数据量很大时怎么处理？
- 网络失败时怎么处理？
- 用户操作中断时怎么处理？

#### 4.2.4 需求文档模板

```markdown
# 需求文档：功能名称

## 1. 背景与目标
- 问题描述：
- 期望结果：
- 成功标准：

## 2. 功能需求
### 2.1 核心功能
- 功能点 1：
- 功能点 2：

### 2.2 用户场景
场景 1：正常流程
1. 用户...
2. 系统...
3. 结果...

场景 2：异常流程
...

## 3. 非功能需求
- 性能：
- 安全：
- 兼容性：

## 4. 边界条件
- 无数据：
- 大数据量：
- 网络异常：

## 5. 交互说明（重点）

### 5.1 核心交互流程
场景 1：正常流程
1. 用户进入页面 → 显示骨架屏（300ms）→ 显示数据
2. 用户 hover 表格行 → 行背景变化 + 显示操作按钮
3. 用户点击"新建" → 弹出 Modal（从上滑入，300ms）
4. 用户填写表单 → 实时验证 → 点击提交
5. 提交成功 → Toast 提示（绿色，顶部）→ 表格刷新 → Modal 关闭

场景 2：异常流程
1. 网络错误 → Toast 提示（红色，"网络异常，请重试"）
2. 表单验证失败 → 错误字段高亮 + 错误提示文字

### 5.2 关键交互细节
- **按钮 hover**：背景色加深 + 轻微上浮 + 阴影增强
- **表格行 hover**：背景变灰 + 显示操作按钮（编辑/删除）
- **Modal 动画**：打开时从上滑入 + 淡入，关闭时向下滑出
- **加载状态**：骨架屏 → 数据（渐变过渡）
- **空状态**：显示插图 + "暂无数据" + "新建"按钮

### 5.3 参考示例
- 表格交互参考：Ant Design Pro 列表页
- 按钮动效参考：Material Design 按钮

## 6. 依赖与风险
- 依赖项：
- 风险点：

## 7. 验收标准
- [ ] 标准 1
- [ ] 标准 2

## 8. 功能优先级（MoSCoW）

| 优先级 | 功能 | 说明 |
|--------|------|------|
| **Must** | 用户登录 | MVP 必须，没有无法使用 |
| **Must** | 用户注册 | MVP 必须 |
| **Should** | 邮箱验证 | 重要但可延后 |
| **Could** | 第三方登录 | 有更好，没有也行 |
| **Won't** | 手机号登录 | 本次不做，未来考虑 |
```

#### 4.2.5 需求验证机制

**验证目标**：确保双方理解一致，避免"我以为"

**验证方法**：

1. **复述验证**：用自己的话复述需求，让对方确认
   - "我理解这个功能是...对吗？"
   - "用户的操作流程是...这样理解正确吗？"

2. **原型验证**：画出草图或线框图，确认界面布局
   - "页面布局是这样的...符合预期吗？"
   - "按钮放在这里...操作便捷吗？"

3. **场景验证**：用具体场景走一遍流程
   - "用户 A 要...他会先...然后...最后..."
   - "如果用户没有...系统会...这样对吗？"

4. **边界验证**：讨论极端情况
   - "如果用户输入了...怎么处理？"
   - "当数据量达到...会有问题吗？"

**验证检查清单**：

- [ ] 我能用自己的话清楚描述这个需求
- [ ] 我能画出这个功能的页面草图
- [ ] 我能列出用户操作的所有步骤
- [ ] 我能说出至少 3 个异常场景
- [ ] 对方确认我的理解是正确的

**如验证失败**：
- 记录理解偏差
- 重新沟通澄清
- 更新需求文档
- 再次验证直到一致

### 4.3 UI/UX 设计（AI Agent 场景简化版）

**位置**：需求明确之后，技术方案之前

**核心理念**：在 AI Agent 开发场景下，**不需要高保真原型**，通过**自然语言描述** + **设计规范** + **参考示例**来指导 AI 生成代码。

#### 4.3.1 为什么不需要传统原型

| 传统方式 | AI Agent 方式 | 原因 |
|----------|---------------|------|
| 画高保真原型（1-3 天） | 直接描述需求（10 分钟） | AI 可直接根据描述生成代码 |
| 标注设计稿 | 说明设计规范 | AI 理解规范后直接应用 |
| 切图给开发 | AI 自动生成 | 不需要人工切图 |

#### 4.3.2 UI/UX 设计流程（简化）

```
需求文档
    ↓
信息架构（页面结构）
    ↓
设计规范定义（色彩/字体/组件）
    ↓
参考示例收集（截图/链接）
    ↓
自然语言描述（布局/交互）
    ↓
AI 生成初版 → 视觉评审 → 迭代调整
```

#### 4.3.3 交付物（极简）

| 交付物 | 形式 | 内容 |
|--------|------|------|
| **信息架构** | 文字或简单脑图 | 页面列表、层级关系 |
| **设计规范** | 文字描述 | 主色、字体、间距 |
| **参考示例** | 截图或链接 | "参考 Ant Design Pro 的表格页" |
| **页面描述** | 自然语言 | "左侧边栏，右侧内容区，顶部筛选..." |

#### 4.3.4 页面描述模板

```markdown
## 页面：用户管理

### 布局
- 整体：左侧边栏（200px）+ 右侧内容区
- 内容区：顶部筛选栏（60px）+ 表格区域 + 分页器

### 色彩
- 主色：#1890ff（蓝色）
- 背景：#f0f2f5（浅灰）
- 文字：#262626（主文字）、#8c8c8c（次文字）

### 组件
- 表格：参考 Ant Design Pro，支持排序、筛选、分页
- 按钮：主按钮蓝色，次按钮白色边框
- 表单：输入框圆角 4px，有聚焦态

### 交互
- 点击"新建"按钮，弹出 Modal 表单
- 表格行 hover 显示操作按钮（编辑/删除）
- 删除前确认弹窗

### 参考
- 类似页面：https://pro.ant.design/list/basic-list
```

#### 4.3.5 AI 生成后的视觉评审

**评审时机**：AI 生成初版代码后立即评审

**评审维度**：
- [ ] 布局是否符合描述
- [ ] 色彩是否正确应用
- [ ] 字体大小层次是否清晰
- [ ] 组件样式是否符合规范
- [ ] 交互反馈是否明确
- [ ] 响应式是否正常

**反馈方式**：
```
问题 1：侧边栏宽度应该是 200px，现在是 250px
问题 2：表格缺少 hover 效果
调整：按钮颜色从 #1890ff 改为 #722ed1
```

#### 4.3.6 交互规范（重点）

**为什么重要**：交互效果直接影响用户体验，必须在需求阶段就明确描述。

**交互描述的时机**：
- **需求阶段**：描述核心交互流程
- **UI 设计阶段**：细化每个组件的交互细节
- **实现阶段**：AI 根据描述生成代码，生成后验收交互效果

**交互描述模板**：

```markdown
## 交互规范：用户管理页面

### 1. 页面加载
- **加载状态**：显示骨架屏（Skeleton），文字区域用灰色块占位
- **加载时间**：
  - < 300ms：直接显示
  - 300ms-1s：显示骨架屏
  - > 1s：显示骨架屏 + 加载进度提示

### 2. 表格交互
- **行 hover**：
  - 背景色变为 #fafafa
  - 右侧显示操作按钮（编辑/删除）
  - 过渡动画：200ms ease-out

- **行点击**：
  - 选中态：左侧显示蓝色竖条（3px）
  - 背景色变为 #e6f7ff

- **排序**：
  - 点击表头：图标旋转 180°，动画 200ms
  - 排序中：表头显示 loading 图标

### 3. 按钮交互
- **主按钮 hover**：
  - 背景色加深（#40a9ff → #1890ff）
  - 轻微上浮（transform: translateY(-1px)）
  - 阴影增强（box-shadow: 0 2px 8px rgba(24,144,255,0.3)）

- **按钮点击**：
  - scale(0.98)，100ms
  - 涟漪效果（Ripple）

### 4. Modal 弹窗
- **打开**：
  - 背景遮罩：淡入 200ms
  - 弹窗：从上方滑入 + 淡入，300ms ease-out

- **关闭**：
  - 弹窗：向下滑出 + 淡出，200ms ease-in
  - 遮罩：淡出 200ms

- **拖拽**：
  - 可拖拽标题栏移动
  - 拖拽时有阴影增强

### 5. 表单验证
- **实时验证**：
  - 输入停止 500ms 后验证
  - 错误：输入框边框变红 + 下方显示错误提示（淡入 200ms）
  - 正确：输入框边框变绿 + 显示对勾图标

- **提交验证**：
  - 点击提交：验证所有字段
  - 有错误：第一个错误字段获得焦点 + 平滑滚动到该字段
  - 提交中：按钮显示 loading，禁用表单

### 6. 空状态
- **无数据**：
  - 显示空状态插图（居中）
  - 文字："暂无数据"
  - 按钮："新建用户"（引导操作）

### 7. 错误处理
- **网络错误**：
  - Toast 提示：红色，顶部居中
  - 自动消失：3 秒
  - 可手动关闭

- **操作失败**：
  - Modal 提示：详细错误信息
  - 提供重试按钮

### 参考示例
- 表格交互参考：https://ant.design/components/table-cn/
- 按钮动效参考：https://material.io/components/buttons
- Modal 动画参考：https://ant.design/components/modal-cn/
```

**交互验收标准**：

AI 生成代码后，必须检查以下交互细节：

- [ ] **状态反馈**：每个操作都有明确的反馈（hover、click、loading、success、error）
- [ ] **过渡动画**：状态变化有平滑过渡，不突兀
- [ ] **响应时间**：操作后 100ms 内必须有反馈，避免用户觉得"卡住了"
- [ ] **错误处理**：错误状态有清晰的提示，不让用户困惑
- [ ] **空状态**：无数据时有引导，不让页面空白
- [ ] **焦点管理**：键盘操作时焦点移动合理

**交互验收流程**：

```
AI 生成代码
    ↓
开发者本地运行
    ↓
逐项检查交互验收标准
    ↓
如有问题 → 记录问题 → 反馈给 AI 修改 → 重新生成
    ↓
验收通过 → 进入功能测试
```

#### 4.3.7 设计规范库（可复用）

建立常用设计规范，方便快速引用：

```
design/
├── color-palette.md       # 色彩规范
├── typography.md          # 字体规范
├── spacing.md             # 间距规范
├── animation.md           # 动画规范（新增）
├── interaction/           # 交互规范（新增）
│   ├── button.md          # 按钮交互
│   ├── form.md            # 表单交互
│   ├── table.md           # 表格交互
│   └── modal.md           # 弹窗交互
├── components/            # 组件示例
│   ├── button.md
│   ├── table.md
│   └── form.md
└── examples/              # 完整页面示例
    ├── list-page.md
    ├── detail-page.md
    └── form-page.md
```

**使用方式**：
```markdown
本页面遵循 [design/color-palette.md] 的色彩规范
表格组件参考 [design/components/table.md]
表格交互参考 [design/interaction/table.md]
布局类似 [design/examples/list-page.md]
```

### 4.4 技术方案设计

#### 4.4.1 方案设计流程（迭代式）

**核心理念**：不用一开始就把所有设计定死，采用**迭代式设计**

**阶段 1：核心架构（必须先做）**

| 内容 | 说明 |
|------|------|
| 技术栈 | Vue3 + TypeScript + FastAPI + PostgreSQL |
| 核心表 | 最核心的 1-2 张表 |
| 核心 API | 最核心的接口 |

**阶段 2：执行中补充（边做边完善）**

| 场景 | 做法 |
|------|------|
| 需要新表 | 补充表设计，补充到文档 |
| 需要新接口 | 补充接口定义，补充到文档 |
| 类型不够用 | 补充 TypeScript 类型定义 |
| 发现设计问题 | 记录问题，后面优化 |

**阶段 3：完成后回顾**

- 补充完整的技术文档
- 整理代码结构
- 为下一个功能模块做准备

**设计原则**：

```
✅ 先跑通再优化
✅ 架构服务于需求，不为架构而架构
✅ 文档跟代码走，做完再补充
✅ 不确定时用最简单方式，后面可以改
```

**方案设计流程**：

1. **现状分析**：了解现有架构和代码
2. **UI 分析**：基于交互描述分析组件和数据需求
3. **技术选型**：选择合适的技术方案
4. **核心架构设计**：设计核心模块关系（先做必须的）
5. **核心接口定义**：定义核心 API（先做必须的）
6. **执行中补充**：边做边补充非核心设计
7. **完成后回顾**：整理完善技术文档

#### 4.3.2 方案文档模板

```markdown
# 技术方案：功能名称

## 1. 方案概述
- 目标：
- 范围：

## 2. 架构设计
```
[架构图]
```

## 3. 技术选型
| 组件 | 选型 | 理由 |
|------|------|------|
| 前端状态管理 | Pinia | 团队熟悉，Vue3 官方推荐 |

## 4. 接口设计
### API 列表
- `GET /api/v1/users` - 获取用户列表
- `POST /api/v1/users` - 创建用户

### 数据结构
```typescript
interface User {
  id: string
  name: string
  email: string
}
```

## 5. 风险评估
| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 性能瓶颈 | 高 | 添加缓存，优化查询 |

## 6. 备选方案
方案 B：...（优缺点对比）
```

### 4.4 详细计划制定

#### 4.4.1 计划制定原则

**SMART 原则**：
- **S**pecific：任务具体明确
- **M**easurable：结果可衡量
- **A**chievable：可实现
- **R**elevant：与目标相关
- **T**ime-bound：有时间限制

#### 4.4.2 计划粒度策略（推荐：混合粒度）

**核心原则**：
- **大阶段定方向**：先划分 3-5 个主要阶段，明确里程碑
- **小任务保执行**：每个阶段再细分为 10-30 分钟的具体任务

**为什么不完全细粒度？**
- 前期无法预知所有细节，过度计划浪费时间
- 需求可能在执行中调整，太细的计划需要频繁修改
- 10-20 分钟的任务粒度太细，管理成本高

**推荐粒度**：

| 层级 | 粒度 | 时长 | 内容 |
|------|------|------|------|
| **阶段** | 粗粒度 | 1-3 天 | 大方向，如"数据库设计" |
| **任务** | 中粒度 | 2-4 小时 | 可交付单元，如"用户表设计" |
| **子任务** | 细粒度 | 10-30 分钟 | 执行步骤，如"定义用户模型字段" |

**执行策略**：
1. **初期**：只规划阶段 + 第一阶段的具体任务
2. **执行中**：每完成一个阶段，再细化下一个阶段的任务
3. **调整**：根据实际进度，动态调整后续计划

**示例**：用户管理功能

```
阶段 1：数据库设计（1 天）
├── 任务 1.1：用户表设计（2h）
│   ├── 子任务：确定用户字段（15min）
│   ├── 子任务：定义模型类（15min）
│   └── 子任务：编写迁移脚本（30min）
├── 任务 1.2：权限表设计（2h）
│   └── ...
└── 任务 1.3：数据库迁移（2h）
    └── ...

阶段 2：API 开发（2 天）
├── 任务 2.1：用户 CRUD API（4h）
└── 任务 2.2：权限控制 API（4h）
[先不细分子任务，执行到再拆分]

阶段 3：前端页面（2 天）
├── 任务 3.1：用户列表页面
└── 任务 3.2：用户编辑页面
[先不细分子任务]
```

**总结**：
- **前期**：阶段（粗）+ 第一阶段任务（中）+ 部分子任务（细）
- **执行**：滚动规划，完成一个阶段再细化下一个
- **粒度**：子任务控制在 10-30 分钟，方便估算和追踪

#### 4.4.3 计划文档模板

```markdown
# 开发计划：功能名称

## 1. 项目信息
- 开始日期：
- 预计结束：
- 负责人：

## 2. 任务清单

### 阶段 1：需求与技术方案（1 天）
- [ ] 1.1 需求沟通与细化（2h）
- [ ] 1.2 技术方案设计（4h）
- [ ] 1.3 方案评审确认（2h）

### 阶段 2：核心功能开发（3 天）
- [ ] 2.1 数据库设计（4h）
  - 依赖：1.3
- [ ] 2.2 API 接口开发（8h）
  - 依赖：2.1
- [ ] 2.3 前端页面开发（12h）
  - 依赖：2.2

### 阶段 3：测试与优化（2 天）
- [ ] 3.1 单元测试（4h）
- [ ] 3.2 集成测试（4h）
- [ ] 3.3 性能优化（4h）

### 阶段 4：部署上线（1 天）
- [ ] 4.1 部署配置（2h）
- [ ] 4.2 上线验证（2h）

## 3. 依赖关系
```
1.3 → 2.1 → 2.2 → 2.3
            ↓
           3.1 → 3.2 → 3.3
                    ↓
                   4.1 → 4.2
```

## 4. 风险与应对
| 风险 | 概率 | 应对策略 |
|------|------|----------|
| 第三方 API 延迟 | 中 | 提前对接，准备 mock |

## 5. 检查点
- [ ] Day 1 结束：方案确认
- [ ] Day 4 结束：核心功能完成
- [ ] Day 6 结束：测试通过
```

#### 4.4.4 计划确认检查清单

在正式开始开发前，必须确认：

- [ ] 需求已完全理解，无模糊点
- [ ] 技术方案已评审通过
- [ ] 所有任务已分解到可执行粒度
- [ ] 任务依赖关系已明确
- [ ] 时间估算合理（预留 20% 缓冲）
- [ ] 风险已识别并有应对策略
- [ ] 验收标准清晰明确

#### 4.4.5 里程碑与进度管理

**里程碑设定原则**：
- 每个里程碑必须有可演示的交付物
- 里程碑间隔 2-3 天，不超过 1 周
- 每个里程碑结束进行评审

**推荐里程碑**：

| 里程碑 | 交付物 | 评审标准 |
|--------|--------|----------|
| M1 - 方案完成 | 技术方案文档 | 方案通过评审 |
| M2 - 基础完成 | 数据库 + API | Postman 可调用 |
| M3 - 功能完成 | 前端 + 后端联调 | 功能可演示 |
| M4 - 测试完成 | 测试报告 | 覆盖率 80%+ |
| M5 - 上线完成 | 生产环境 | 可正常使用 |

**进度追踪方法**：

1. **每日站会（5-10 分钟）**：
   - 昨天做了什么？
   - 今天计划做什么？
   - 有什么阻塞？

2. **里程碑评审（30 分钟）**：
   - 演示交付物
   - 检查验收标准
   - 确认下一步计划

3. **进度可视化**：
   ```
   阶段 1：需求与方案 [████████░░] 80%
   ├── 1.1 需求细化 [██████████] 100% ✓
   ├── 1.2 技术方案 [████████░░] 80% → 进行中
   └── 1.3 方案评审 [░░░░░░░░░░] 0%
   ```

**进度偏差处理**：

| 偏差程度 | 处理措施 |
|----------|----------|
| < 20% | 正常波动，继续执行 |
| 20-50% | 分析原因，调整后续计划 |
| > 50% | 重新评估，可能需要调整范围或延期 |

**风险管理更新**：
- 每周回顾风险清单
- 新风险及时记录和评估
- 已发生风险更新应对状态

### 4.5 需求变更管理

#### 4.5.1 变更流程

```
变更请求 → 影响评估 → 方案调整 → 重新确认 → 更新计划 → 执行
```

#### 4.5.2 变更评估维度

- **范围影响**：是否超出原定范围？
- **时间影响**：延期多久？
- **成本影响**：需要额外资源吗？
- **质量影响**：是否引入技术债务？
- **依赖影响**：是否影响其他任务？

### 4.6 提交规范

```
feat: 添加用户登录功能

- 添加 JWT 认证
- 添加登录接口 /api/v1/auth/login

Co-Authored-By: Claude <noreply@anthropic.com>
```

类型：feat, fix, refactor, docs, test, chore, perf, ci

---

## 五、项目蓝图文档

### 5.1 蓝图定位

**项目蓝图** = 项目的"状态快照"

- 记录项目的完整面貌
- 随着需求/计划调整不断更新
- 供 AI 快速理解项目现状

### 5.2 蓝图文件

**位置**：`docs/蓝图.md`

### 5.3 蓝图内容

```markdown
# 项目蓝图：项目名称

## 1. 项目概述
- 项目名称：
- 核心功能：
- 目标用户：

## 2. 技术栈
- 前端：Vue3 + TypeScript + Vite + Pinia
- 后端：FastAPI + PostgreSQL

## 3. 数据库设计（已完成）
### 用户表 (users)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| name | VARCHAR | 用户名 |

## 4. API 接口
### 用户管理
| 方法 | 路径 | 说明 | 状态 |
|------|------|------|------|
| GET | /api/v1/users | 获取用户列表 | ✅已完成 |
| POST | /api/v1/users | 创建用户 | 🔄开发中 |

## 5. 前端类型
```typescript
interface User {
  id: string
  name: string
}
```

## 6. 功能清单
| 功能 | 描述 | 状态 | 备注 |
|------|------|------|------|
| 用户登录 | 邮箱密码登录 | ✅已完成 | |
| 用户管理 | CRUD 操作 | 🔄开发中 | |

## 7. 核心业务规则
- 用户名不能重复
```

### 5.4 更新时机

| 时机 | 更新内容 |
|------|----------|
| 需求明确后 | 添加功能描述、技术选型 |
| 技术方案后 | 添加数据库设计、API 接口 |
| 计划细化后 | 添加功能清单 |
| 完成一个功能 | 更新 API 状态 + 具体内容 |
| 计划调整后 | 更新功能清单状态 |

### 5.5 核心原则

- **准确**：每个关键节点都更新
- **具体**：不只是状态，还有具体内容
- **最小化**：只记录最核心的

---

## 六、Skills 与 Agents 配置

### 6.1 整合思路

**来源**：
- superpowers：工作流核心技能（头脑风暴、计划、调试、TDD）
- everything-claude-code：语言 patterns 和专业 agents

**整合原则**：
- 取两者所长
- 根据你的工作流调整
- 避免重复

### 6.2 推荐的 Skills

| Skill | 来源 | 用途 | 何时使用 |
|-------|------|------|----------|
| **brainstorming** | superpowers | 需求沟通 | 开始新功能时 |
| **writing-plans** | superpowers | 制定计划 | 需求明确后 |
| **test-driven-development** | superpowers | TDD 开发 | 编码时 |
| **systematic-debugging** | superpowers | 调试 | 遇到 bug 时 |
| **verification-before-completion** | superpowers | 完成前验证 | 功能完成时 |
| **requesting-code-review** | superpowers | 代码审查 | 提交前 |
| **frontend-patterns** | ecc | 前端规范 | 前端开发时 |
| **python-patterns** | ecc | 后端规范 | 后端开发时 |
| **api-design** | ecc | API 设计 | 设计接口时 |
| **security-review** | ecc | 安全审查 | 需要安全检查时 |

### 6.3 推荐的 Agents

| Agent | 来源 | 用途 | 何时使用 |
|-------|------|------|----------|
| **planner** | ecc | 规划功能 | 需求明确后制定计划 |
| **architect** | ecc | 架构设计 | 需要技术方案时 |
| **tdd-guide** | ecc | TDD 指导 | 编码时 |
| **code-reviewer** | ecc | 代码审查 | 提交前 |
| **security-reviewer** | ecc | 安全审查 | 需要安全检查时 |
| **build-error-resolver** | ecc | 构建错误 | 构建失败时 |
| **e2e-runner** | ecc | E2E 测试 | 需要端到端测试时 |
| **refactor-cleaner** | ecc | 重构清理 | 清理死代码时 |

### 6.4 Skills 使用场景对照

| 场景 | 使用 Skill |
|------|------------|
| 需求不明确，需要沟通 | `/brainstorming` |
| 需求明确，要做计划 | `/writing-plans` |
| 开始编码，要 TDD | `/test-driven-development` |
| 遇到 bug，要调试 | `/systematic-debugging` |
| 功能完成，要验证 | `/verification-before-completion` |
| 代码写完，要审查 | `/requesting-code-review` |
| 写前端代码 | `/frontend-patterns` |
| 写后端代码 | `/python-patterns` |
| 设计 API | `/api-design` |

### 6.5 Agents 使用场景对照

| 场景 | 使用 Agent |
|------|------------|
| 制定详细计划 | Task: planner |
| 设计系统架构 | Task: architect |
| TDD 编码指导 | Task: tdd-guide |
| 代码审查 | Task: code-reviewer |
| 安全审查 | Task: security-reviewer |
| 修复构建错误 | Task: build-error-resolver |
| 运行 E2E 测试 | Task: e2e-runner |
| 重构清理 | Task: refactor-cleaner |

### 6.6 禁用/调整的 Skills/Agents

| 原因 | 处理 |
|------|------|
| 与你的工作流重复 | 禁用 `finishing-a-development-branch` |
| 语言不匹配 | 禁用 Go/Java/C++ 相关 |
| 暂时不需要 | 禁用 continuous-learning |

### 6.7 配置建议

**settings.json**：
```json
{
  // 可以保留两个插件，根据场景切换
}
```

**推荐做法**：
- 核心工作流：使用 superpowers 的 Skills
- 语言规范：使用 everything-claude-code 的 Skills
- Agents：使用 everything-claude-code 的 Agents

---

## 七、测试规范

### 5.1 前端测试

- **框架**：Vitest
- **覆盖率**：80%
- **Mock**：MSW (Mock Service Worker) 或手动 mock

### 5.2 后端测试

- **框架**：pytest
- **覆盖率**：80%
- **Mock**：pytest-mock
- **Fixtures**：conftest.py
- **HTTP 测试**：pytest-httpx

### 5.3 E2E 测试（Agent Browser）

使用 Vercel 的 Agent Browser 进行端到端测试。

#### 5.3.1 测试范围

- **核心用户流程**：登录、注册、支付等
- **关键业务功能**：主要功能路径
- **跨页面交互**：页面间数据传递

#### 5.3.2 测试文件结构

```
e2e/
├── specs/                    # 测试用例
│   ├── auth.spec.ts         # 认证流程
│   ├── user.spec.ts         # 用户管理
│   └── order.spec.ts        # 订单流程
├── fixtures/                 # 测试数据
│   └── users.json
├── support/                  # 支持文件
│   └── commands.ts          # 自定义命令
└── agent.config.ts          # 配置文件
```

#### 5.3.3 测试用例规范

```typescript
// e2e/specs/auth.spec.ts
describe("认证流程", () => {
  it("用户登录成功", async ({ page }) => {
    await page.goto("/login")
    await page.fill("[data-testid="email"]", "test@example.com")
    await page.fill("[data-testid="password"]", "password123")
    await page.click("[data-testid="login-btn"]")

    // 验证登录成功
    await page.waitForURL("/dashboard")
    await expect(page.locator("[data-testid="user-name"]")).toBeVisible()
  })

  it("登录失败显示错误", async ({ page }) => {
    await page.goto("/login")
    await page.fill("[data-testid="email"]", "wrong@example.com")
    await page.fill("[data-testid="password"]", "wrong")
    await page.click("[data-testid="login-btn"]")

    // 验证错误提示
    await expect(page.locator("[data-testid="error-msg"]")).toContainText("登录失败")
  })
})
```

#### 5.3.4 选择器规范

使用 `data-testid` 属性标记测试元素：

```vue
<!-- 好的实践 -->
<button data-testid="submit-btn" @click="handleSubmit">提交</button>
<input data-testid="email-input" v-model="email" />

<!-- 避免使用 CSS 类或文本 -->
<button class="btn-primary">提交</button>  <!-- 不推荐 -->
```

#### 5.3.5 测试数据管理

```typescript
// e2e/fixtures/users.ts
export const testUsers = {
  admin: {
    email: "admin@test.com",
    password: "admin123"
  },
  user: {
    email: "user@test.com",
    password: "user123"
  }
}
```

#### 5.3.6 运行命令

```bash
# 运行所有 E2E 测试
npm run test:e2e

# 运行特定测试文件
npm run test:e2e -- specs/auth.spec.ts

# 调试模式
npm run test:e2e -- --debug
```
---

## 六、CI/CD 规范（可选）

### 6.1 GitHub Actions

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run linter
        run: npm run lint
      - name: Run tests
        run: npm run test
      - name: Build
        run: npm run build
```

---

## 七、待确认问题

### 已确认

- [x] 前端目录结构
- [x] 前端命名规范
- [x] 后端目录结构（Python/FastAPI）
- [x] 后端命名规范
- [x] 代码质量标准
- [x] 日志规范
- [x] 环境变量管理
- [x] 安全规范
- [x] 测试规范

### 待确认

- [ ] CI/CD 配置（上面是示例，需要根据项目调整）

---

## 七、参考项目

- 前端参考：`/Users/huangzhixin/Desktop/Code/AI/Agent-Monorepo/Agent-Monorepo-UI/`
- 后端参考：`/Users/huangzhixin/Desktop/Code/AI/` (当前 AI 相关项目)

---

*持续更新中...*
