# 模块化路由就是把每个业务功能的接口拆分到独立文件里，再统一挂载到主应用中。

from fastapi import APIRouter, HTTPException, Query
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

@router.get("/list")
async def get_news_list(
        category_id: int = Query(..., alias="categoryId"),  # alias设置别名，前端传categoryId，后端接收category_id
        page: int = 1,
        page_size: int = Query(10, alias="pageSize", le=100),
        db: AsyncSession = Depends(get_db)
    ):
    # 思路：处理分页规则 → 查询新闻列表 → 计算总量 → 计算是否还有更多
    skip = (page - 1) * page_size
    news_list = await news.get_news_list(db, category_id, skip, page_size)
    total = await news.get_news_count(db, category_id)
    # 跳过的条数 + 当前页的条数 < 总条数 → 还有更多
    has_more = (skip + len(news_list) < total)
    return {
        "code": 200,
        "message": "获取新闻列表成功",
        "data": {
            "list": news_list,
            "total": total,
            "hasMore": has_more
        }
    }

@router.get("/detail")
async def get_news_detail(db: AsyncSession = Depends(get_db), news_id: int = Query(..., alias="id")):
    # 查询新闻详情 + 浏览量+1 +相关新闻
    news_detail = await news.get_news_detail(db, news_id)
    if not news_detail:
        raise HTTPException(status_code=404, detail="新闻不存在")
    
    views_res = await news.increase_news_views(db, news_detail.id)  # 浏览量+1
    if not views_res:
        raise HTTPException(status_code=404, detail="更新浏览量失败")
    
    releated_news = await news.get_related_news(db, news_detail.category_id, news_detail.id)

    return {
        "code": 200,
        "message": "获取新闻详情成功",
        "data": {
            "id": news_detail.id,
            "title": news_detail.title,
            "content": news_detail.content,
            "image": news_detail.image,
            "author": news_detail.author,
            "publishTime": news_detail.publish_time,
            "category_id": news_detail.category_id,
            "views": news_detail.views,
            "relatedNews": releated_news
        }
    }