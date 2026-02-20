---
name: python-fastapi-guide
description: Python FastAPI 开发指南 - 提供 Python + FastAPI 代码规范
---

# Python FastAPI 开发指南

## 技术栈

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- LangGraph（AI 场景）

## 目录结构

```
src/
├── api/                    # API 路由
│   ├── __init__.py
│   ├── deps.py            # 依赖注入
│   ├── middleware/       # 中间件
│   └── v1/
│       ├── endpoints/    # 端点
│       │   ├── users.py
│       │   └── items.py
│       └── router.py
├── core/                   # 核心配置
│   ├── config.py         # 配置管理
│   ├── security.py       # 安全相关
│   └── database.py       # 数据库连接
├── models/                # 数据模型
│   ├── user.py
│   └── item.py
├── schemas/               # Pydantic schemas
│   ├── user.py
│   └── item.py
├── services/              # 业务逻辑
│   ├── user_service.py
│   └── item_service.py
├── utils/                 # 工具函数
├── constants/             # 常量
├── tests/                 # 测试
└── main.py               # 应用入口
```

## 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 变量/函数 | snake_case | `get_user_info` |
| 类名 | PascalCase | `UserService` |
| 数据库表 | snake_case + 复数 | `users` |
| API 路径 | snake_case + 复数 | `/users` |
| 常量 | 全大写下划线 | `MAX_RETRY_COUNT` |

## 分层架构

```
API 层 (endpoints/)     → 处理请求/响应，调用 Service
    ↓
Service 层 (services/)  → 业务逻辑，事务管理
    ↓
Repository 层          → 数据访问抽象
    ↓
Model 层 (models/)     → 数据库模型
```

## 代码质量标准

- **函数长度**：不超过 50 行
- **文件大小**：不超过 400 行
- **嵌套层级**：不超过 4 层
- **测试覆盖率**：80%

## 注释规范

**函数文档字符串**：
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

## Repository 模式

```python
class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
```

## Service 层

```python
class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repo = user_repository

    def get_user(self, user_id: int) -> User:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User {user_id} not found")
        return user
```

## API Endpoint 规范

```python
router = APIRouter(prefix="/users", tags=["用户管理"])

@router.get("", response_model=List[UserSchema])
def list_users(
    skip: int = 0,
    limit: int = 100,
    user_service: UserService = Depends(get_user_service)
):
    """获取用户列表"""
    return user_service.list_users(skip=skip, limit=limit)
```

## 依赖注入

```python
def get_user_service(
    user_repo: UserRepository = Depends(get_user_repository)
) -> UserService:
    return UserService(user_repo)
```

## 安全规范

- 敏感信息：使用环境变量
- 密码加密：bcrypt
- API 认证：JWT Token
- 输入验证：Pydantic models
- CORS：配置允许的域名

## 测试

- 框架：pytest
- 覆盖率：80%
- Mock：pytest-mock
- HTTP 测试：pytest-httpx
