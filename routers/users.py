from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_config import get_db
from schemas.users import UserRequest

# 创建apirouter实例
# prefix: 路由前缀(根据 api 接口规范文档编写)，tags: 标签（分组）
router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("/register")
async def register(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    return {
        "code": 200,
        "message": "注册成功",
        "data": {
            "token": "用户访问令牌",
            "userInfo": {
                "id": 1,
                "username": user_data.username,
                "bio": "这个人很懒，什么都没留下",
                "avatar": "https://example.com/avatar.jpg"
            }
        }
    }