from fastapi import FastAPI
from routers import news, users
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 添加 CORS 中间件，解决跨域问题
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许访问的源,开发阶段可以设置为 ["*"]，生产环境需要指定具体域名
    allow_credentials=True,  # 允许携带 Cookie
    allow_methods=["*"],  # 允许所有请求方法
    allow_headers=["*"],  # 允许所有请求头
)


@app.get("/")
async def root():
    return {"message": "Hello World"}

# 挂载路由（注册路由）
app.include_router(news.router)
app.include_router(users.router)