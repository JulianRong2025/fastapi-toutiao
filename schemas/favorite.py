

from pydantic import BaseModel, Field

class FavoriteCheckRequest(BaseModel):
    is_favorite: int = Field(..., alias="isFavorite")