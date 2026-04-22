from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User
from schemas.users import UserRequest
from utils.security import get_password_hash

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