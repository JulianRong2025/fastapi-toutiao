# 模块化路由就是把每个业务功能的接口拆分到独立文件里，再统一挂载到主应用中。

from fastapi import APIRouter
from crud import news
from config.db_config import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends


# 创建apirouter实例
# prefix: 路由前缀(根据 api 接口规范文档编写)，tags: 标签（分组）
router = APIRouter(prefix="/api/news", tags=["news"])

# 接口实现流程
# 1 模块化路由 → API 接口规范文档
# 2 定义模型类 → 数据库表（数据库设计文档）
# 3 在 crud 中创建文件，封装操作数据库的方法
# 4 在路由处理函数中调用 crud 中的方法，编写接口实现逻辑

@router.get("/categories")
async def get_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    # 获取数据库中的新闻分类列表（定义模型类、封装查询数据的方法）
    categories = await news.get_categories(db, skip, limit)
    return {
        "code": 200,
        "message": "获取新闻分类成功",
        "data": categories
    }