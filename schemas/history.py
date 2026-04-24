from pydantic import BaseModel, Field


# 添加浏览历史请求体
class HistoryAddRequest(BaseModel):
    news_id: int = Field(..., alias="newsId")
