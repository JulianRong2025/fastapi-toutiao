from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_config import get_db
from models.users import User
from schemas.users import UserAuthResponse, UserInfoResponse, UserRequest
from crud.users import create_access_token, get_user_by_username, create_user, authenticate_user
from starlette import status
from utils.response import success_response
from utils.auth import get_current_user

# 创建apirouter实例
# prefix: 路由前缀(根据 api 接口规范文档编写)，tags: 标签（分组）
router = APIRouter(prefix="/api/user", tags=["users"])

# 注册接口
@router.post("/register")
async def register(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    # 注册逻辑：验证用户是否存在，创建用户，生成令牌
    existing_user = await get_user_by_username(user_data.username, db)  # 查询用户是否存在
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户已存在")
    new_user = await create_user(user_data, db)

    user_token = await create_access_token(new_user.id, db)

    response_data = UserAuthResponse(
        token=user_token.token, 
        user_info=UserInfoResponse.model_validate(new_user)  # model_validate()从 news_user 这个 orm 对象中取值
        )  

    return success_response(message="注册成功", data=response_data)
    # return {
    #     "code": 200,
    #     "message": "注册成功",
    #     "data": {
    #         "token": user_token.token,
    #         "userInfo": {
    #             "id": new_user.id,
    #             "username": new_user.username,
    #             "bio": new_user.bio,
    #             "avatar": new_user.avatar
    #         }
    #     }
    # }

# 登录接口
@router.post("/login")
async def login(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    # 登录逻辑：验证用户是否存在，验证密码，生成令牌
    user = await authenticate_user(user_data.username, user_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")

    user_token = await create_access_token(user.id, db)

    response_data = UserAuthResponse(
        token=user_token.token, 
        user_info=UserInfoResponse.model_validate(user)  # model_validate()从user 这个 orm 对象中取值
        )  
    
    return success_response(message="登录成功", data=response_data)

# 获取用户信息接口
@router.get("/info")
async def get_user_info(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    # 获取用户信息逻辑：查并验证令牌，查用户→封装 crud → 整合成一个工具函数→路由导入使用：依赖注入

    response_data = UserInfoResponse.model_validate(user)  # model_validate()从 user 这个 orm 对象中取值

    return success_response(message="获取用户信息成功", data=response_data)