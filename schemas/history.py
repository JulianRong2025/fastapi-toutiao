from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from schemas.base import NewsItenBase

# 添加浏览历史请求体
class HistoryAddRequest(BaseModel):
    news_id: int = Field(..., alias="newsId")

class HistoryNewsItemResponse(NewsItenBase):
    history_id: int = Field(alias="historyId")
    view_time: datetime = Field(alias="viewTime")

    model_config = ConfigDict(
        from_attributes=True,  # 支持从ORM模型转换
        populate_by_name=True  # 支持别名字段
    )

class HistoryListResponse(BaseModel):
    list: list[HistoryNewsItemResponse]
    total: int
    has_more: bool = Field(alias="hasMore")

    model_config = ConfigDict(
        from_attributes=True,  # 支持从ORM模型转换
        populate_by_name=True  # 支持别名字段
    )
