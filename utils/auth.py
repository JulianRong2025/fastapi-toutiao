from fastapi import Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_config import get_db
from crud.users import get_user_by_token
from starlette import status

# 整合 根据 token 查询用户信息，返回用户信息的函数
async def get_current_user(
        authorization: str = Header(..., alias="Authorization"), 
        db: AsyncSession = Depends(get_db)
        ):
    # bearer xxx
    # token = authorization.split(" ")[1]  # 从 "Bearer xxx" 中提取 token(第一种写法)
    token = authorization.replace("Bearer ", "")  # 替换掉 "Bearer " 前缀，得到纯 token（第二种写法）
    current_user = await get_user_by_token(token, db)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无效的token或已经过期的token")
    return current_user
