from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UserRequest(BaseModel):
    username: str
    password: str

# user_info 对应的类:基础类 + Info 类（id、用户名）
class UserInfoBase(BaseModel):
# 用户信息基础数据模型
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    bio: Optional[str] = Field(None, max_length=500, description="个人简介")

class UserInfoResponse(UserInfoBase):
    id: int
    username: str
    # 模型类配置
    model_config = ConfigDict(
        from_attributes=True,  # 允许从 ORM 模型对象创建 Pydantic 模型实例
    )

# data 数据类型
class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse = Field(..., alias="userInfo")  # 使用别名 userInfo 来匹配前端接口规范

    # 模型类配置
    model_config = ConfigDict(
        from_attributes=True,  # 允许从 ORM 模型对象创建 Pydantic 模型实例
        populate_by_name=True  # 允许使用字段别名来创建模型实例
    )

# 更新用户信息的模型类
class UserUpdateRequest(BaseModel):
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    bio: Optional[str] = Field(None, max_length=500, description="个人简介")
    phone: Optional[str] = Field(None, max_length=20, description="电话号码")

# 修改密码的模型类
class UserChangePwdRequest(BaseModel):
    old_password: str = Field(..., description="旧密码", alias="oldPassword")
    new_password: str = Field(..., min_length=6,description="新密码", alias="newPassword")