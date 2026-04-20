# 模块化路由就是把每个业务功能的接口拆分到独立文件里，再统一挂载到主应用中。

from fastapi import APIRouter

# 创建apirouter实例
# prefix: 路由前缀(根据 api 接口规范文档编写)，tags: 标签（分组）
router = APIRouter(prefix="/api/news", tags=["news"])

@router.get("/categories")
async def get_categories():
    return {"msg": "获取分类成功"}