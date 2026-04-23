from datetime import datetime, timedelta
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User, UserToken
from schemas.users import UserRequest
from utils.security import get_password_hash, verify_password

# 根据用户名查询数据库
async def get_user_by_username(username: str, db: AsyncSession):
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    return result.scalar_one_or_none()  # 返回单个结果，如果没有结果返回 None

# 创建用户
async def create_user(user_data: UserRequest, db: AsyncSession):
    # 先密码加密，再添加用户到数据库
    new_user = User(username=user_data.username, password=get_password_hash(user_data.password))
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)  # 把数据库自动生成的字段，同步回 Python 对象，否则返回的新用户没有 ID、创建时间
    return new_user

# 生成 token
async def create_access_token(user_id: int, db: AsyncSession):
    # 生成 token + 设置过期时间 → 查询数据库当前用户是否有 token
    # 如果有 token，更新 token 和过期时间；如果没有 token，创建新 token
    token = str(uuid.uuid4())  # 生成随机 token
    # timedelta(days=7, hours=0, minutes=0, seconds=0) 全量写法
    expires_at = datetime.now() + timedelta(days=7)  # 设置过期时间为 7 天后
    query = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()  # 返回单个结果，如果没有结果返回 None
    
    if user_token:
        # 更新 token 和过期时间
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        # 创建新 token
        user_token = UserToken(user_id=user_id, token=token, expires_at=expires_at)
        db.add(user_token)
    
    await db.commit()
    await db.refresh(user_token)  # 同步数据库自动生成的字段
    return user_token

# 验证用户
async def authenticate_user(username: str, password: str, db: AsyncSession):
    user = await get_user_by_username(username, db)
    if not user:
        return None
    # 验证密码
    if not verify_password(password, user.password):
        return None
    return user

# 根据 token 查询用户：验证 token→查询用户
async def get_user_by_token(token: str, db: AsyncSession):
    query = select(UserToken).where(UserToken.token == token)
    result = await db.execute(query)
    db_user_token = result.scalar_one_or_none()
    if not db_user_token or db_user_token.expires_at < datetime.now():
        return None
    # 根据 token 查询到 user_id，再根据 user_id 查询用户信息
    query = select(User).where(User.id == db_user_token.user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()  