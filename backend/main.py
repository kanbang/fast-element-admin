'''
Descripttion: 
version: 0.x
Author: zhai
Date: 2023-05-26 08:49:32
LastEditors: zhai
LastEditTime: 2023-05-31 14:52:07
'''
'''
Descripttion: 
version: 0.x
Author: zhai
Date: 2023-05-26 08:49:32
LastEditors: zhai
LastEditTime: 2023-05-31 12:05:55
'''
'''
Descripttion: 
version: 0.x
Author: zhai
Date: 2023-05-26 08:49:32
LastEditors: zhai
LastEditTime: 2023-05-31 11:06:46
'''
# -*- coding: utf-8 -*-
# @author: xiaobai


import uvicorn
from fastapi import FastAPI, Depends, HTTPException

from config import config
from app.corelibs.logger import init_logger, logger
from app.db.redis import init_redis_pool
from app.init.cors import init_cors
from app.init.exception import init_exception
from app.init.middleware import init_middleware
from app.init.routers import init_router
from app.init.dependencies import set_global_request
# from app.models import init_db

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{config.API_PREFIX}/user/login")

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def token_auth(token: str=Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(401, "Invalid token")

# router = MemoryCRUDRouter(schema=MySchema, dependencies=[Depends(token_auth)])
# app.include_router(router)



app = FastAPI(title="Admin", description=config.PROJECT_DESC,
              version=config.PROJECT_VERSION,
              dependencies=[Depends(set_global_request)])


def init_app():
    """ 注册中心 """
    # register_mount(app)  # 挂载静态文件

    init_exception(app)  # 注册捕获全局异常

    init_router(app)  # 注册路由

    init_middleware(app)  # 注册请求响应拦截

    init_cors(app)  # 初始化跨域

    init_logger()

    logger.info("日志初始化成功！！!")  # 初始化日志


@app.on_event("startup")
async def startup():
    init_app()  # 加载注册中心
    # await init_db()  # 初始化表
    # await init_data()  # 初始化数据
    app.state.redis = await init_redis_pool()  # redis


@app.on_event("shutdown")
async def shutdown():
    await app.state.redis.close()  # 关闭 redis

@app.get("/token")
async def token(token: str = Depends(oauth2_scheme)):
    return {"token": token}

# gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8101
if __name__ == '__main__':
    uvicorn.run(app='main:app', host="127.0.0.1", port=8102, reload=True)
