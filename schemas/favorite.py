from datetime import datetime

from schemas.base import NewsItenBase

from pydantic import BaseModel, ConfigDict, Field

# 是否收藏类型
class FavoriteCheckRequest(BaseModel):
    is_favorite: bool = Field(..., alias="isFavorite")

# 添加收藏请求体
class FavoriteAddRequest(BaseModel):
    news_id: int = Field(..., alias="newsId")




# 规划两个类：一个是新闻模型类 + 收藏的模型类（浏览历史也要使用到新闻模型类，为了增加复用性，分成两个类）
class FavoriteNewsItem(NewsItenBase):
    favorite_time: datetime = Field(alias="favoriteTime")
    favorite_id: int = Field(alias="favoriteId")

    model_config = ConfigDict(
        from_attributes=True,  # 支持从ORM模型转换
        populate_by_name=True  # 支持别名字段
    )

# 收藏列表项
class FavoriteListItem(BaseModel):
    list: list[FavoriteNewsItem]
    total: int
    has_more: bool = Field(alias="hasMore")

    model_config = ConfigDict(
        from_attributes=True,  # 支持从ORM模型转换
        populate_by_name=True  # 支持别名字段
    )