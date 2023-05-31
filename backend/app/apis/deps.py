# -*- coding: utf-8 -*-
# @author: xiaobai


import typing
from fastapi import Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from config import config
from app.db.redis import MyRedis
from app.db.session import async_session



async def get_db() -> typing.AsyncGenerator[AsyncSession, None]:
    """ sql连接会话 """
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_redis(request: Request) -> MyRedis:
    """ redis连接对象 """
    return await request.app.state.redis
