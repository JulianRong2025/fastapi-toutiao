# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在此代码库中工作时提供指导。

## 项目概述

这是一个 FastAPI 新闻应用后端，前端位于 `xwzx-news/` 目录下（Vue/React）。后端实现了完整的新闻平台功能，包括用户认证、新闻浏览、收藏和阅读历史。

## 运行应用

```bash
# 安装依赖
pip install -r requirements.txt

# 启动 FastAPI 开发服务器
uvicorn main:app --reload

# 启动前端（进入 xwzx-news/ 目录）
cd xwzx-news
npm install
npm run dev
```

## 架构设计

### 分层架构

项目遵循清晰的分层架构：

- **`main.py`**: 应用入口，注册路由、CORS 中间件和全局异常处理器
- **`routers/`**: 按功能组织的 API 端点（users, news, favorite, history）。每个路由器处理 HTTP 请求并返回响应。
- **`crud/`**: 数据库操作和业务逻辑。函数由路由器调用，执行查询和变更。
- **`models/`**: SQLAlchemy ORM 模型，表示数据库表。所有模型使用 SQLAlchemy 2.0 语法和 `Mapped` 类型提示。
- **`schemas/`**: Pydantic 模型，用于请求验证和响应序列化。
- **`cache/`**: Redis 缓存辅助函数，用于读写缓存数据。
- **`config/`**: 数据库配置（带连接池的 MySQL）和 Redis 客户端设置。
- **`utils/`**: 认证、密码加密、异常处理和响应格式化工具。

### 数据库与缓存策略

应用使用 **MySQL** 作为主数据库，**Redis** 用于缓存，采用 cache-aside 模式：

1. 优先尝试从 Redis 缓存读取
2. 缓存未命中时，查询 MySQL 数据库
3. 将结果缓存回 Redis，设置适当的 TTL

缓存过期时间：
- 分类：7200s（2 小时）- 稳定的参考数据
- 新闻列表：600s（10 分钟）- 中等变化频率
- 新闻详情：1800s（30 分钟）- 内容稳定
- 相关新闻：600s（10 分钟）

### 认证系统

应用使用自定义的基于 Token 的认证系统（非 JWT）：
- Token 存储在 `user_token` 表中，7 天过期
- `Authorization` 请求头必须包含 `Bearer <token>`
- 使用 `utils/auth.py` 中的 `get_current_user` 依赖进行端点认证
- 密码通过 `utils/security.py` 使用 bcrypt 加密

### 数据库配置

数据库 URL 硬编码在 `config/db_config.py` 中：
- 使用 `mysql+aiomysql://` 连接 MySQL
- 连接池：10 个持久连接，20 个最大溢出连接
- 始终使用 `AsyncSession = Depends(get_db)` 依赖进行数据库访问

### 错误处理

全局异常处理器注册在 `utils/exception_handlers.py` 中：
- `HTTPException`: 业务逻辑错误（404, 401 等）
- `IntegrityError`: 数据库约束违反（唯一键、外键）
- `SQLAlchemyError`: 通用数据库错误
- `Exception`: 捕获所有未处理的异常

所有错误返回 JSON 响应，结构为：`{"code": int, "message": str, "data": Any}`

### 响应格式

使用 `utils/response.success_response()` 返回一致的成功响应：
```python
return success_response(message="操作成功", data=response_data)
```

## 开发模式

### 添加新功能

1. **定义模型**：在 `models/<feature>.py` 中使用 SQLAlchemy 2.0 `Mapped` 语法定义模型
2. **创建 Pydantic 模型**：在 `schemas/<feature>.py` 中创建请求/响应验证模型
3. **实现 CRUD 操作**：在 `crud/<feature>.py` 中实现数据库操作（如需缓存层也在此添加）
4. **创建路由**：在 `routers/<feature>.py` 中使用 APIRouter 创建端点
5. **注册路由**：在 `main.py` 中使用 `app.include_router()` 注册路由

### Async/Await

所有数据库操作和缓存操作使用 async/await：
- 查询使用 `await db.execute(stmt)`
- Redis 使用 `await redis_client.get(key)` 和 `await redis_client.setex()`
- 数据库会话始终使用 `AsyncSession`

### 模型到 Schema 转换

使用 Pydantic 的 `model_validate()` 将 ORM 模型转换为 schema：
```python
response_data = UserInfoResponse.model_validate(user)
```

对于缓存存储，使用 `jsonable_encoder()` 将 ORM 对象转换为 JSON 可序列化格式。

### 索引

为频繁查询的列创建索引以提高性能：
```python
__table_args__ = (
    Index('idx_column', 'column_name'),
)
```

## 常用命令

```bash
# 检查 MySQL 是否运行
mysql -u root -p -e "SHOW DATABASES;"

# 检查 Redis 连接
redis-cli PING

# 启动 MySQL 服务器（如果未运行）
brew services start mysql
brew services start redis
```
