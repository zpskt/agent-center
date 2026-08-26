#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：database.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/26 23:38 
@Description： 
'''
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config.settings import settings
from app.infrastructure.database.models import Base


engine = create_async_engine(
    settings.database_url,
    echo=settings.database_echo,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db():
    print(">>> init_db called")
    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all
        )

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session