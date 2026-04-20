from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

# 数据库连接URL
URL = "mysql+aiomysql://root:..167872130Wang@localhost:3306/news_app?charset=utf8mb4"

# 创建异步数据库引擎
async_engine = create_async_engine(URL,
                                   echo=True,  # 可选：输出 SQL 日志
                                   pool_size=10,  # 设置连接池中保持的持久连接数
                                   max_overflow=20  # 设置连接池允许创建的额外连接数
                                   )

# 异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,  # 绑定数据库引擎
    class_=AsyncSession,  # 使用异步会话类
    expire_on_commit=False # 提交后不失效，保持对象状态，不会重新查询数据库
    )

# 依赖项：获取数据库会话
async def get_db():
    async with AsyncSessionLocal() as session:  # 获取异步会话
        try:
            yield session  # 返回数据库会话给路由处理函数使用
            await session.commit()  # 提交事务
        except Exception as e:
            await session.rollback()  # 回滚事务
            raise e  # 抛出异常
        finally:
            await session.close()  # 关闭会话