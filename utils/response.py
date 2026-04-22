from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def success_response(message: str = "Success", data = None):
    content = {
        "code": 200,
        "message": message,
        "data": data
    }
    # 任何的 FastAPI、Pydantic、ORM 对象都要正常响应
    return JSONResponse(content=jsonable_encoder(content))