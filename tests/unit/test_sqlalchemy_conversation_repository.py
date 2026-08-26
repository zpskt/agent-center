#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：test_sqlalchemy_conversation_repository.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/26 23:59 
@Description： 
'''
import pytest
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.domain.context import ConversationMessage
from app.infrastructure.conversation.sqlalchemy_conversation_repository import (
    SQLAlchemyConversationRepository,
)
from app.infrastructure.database.models import Base


@pytest.fixture
async def session():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:"
    )

    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all
        )

    session_factory = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with session_factory() as session:
        yield session

    await engine.dispose()


@pytest.mark.asyncio
async def test_append_and_get_history(session):

    repository = SQLAlchemyConversationRepository(
        session
    )

    await repository.append_message(
        user_id="user-001",
        conversation_id="conv-001",
        message=ConversationMessage(
            role="user",
            content="第一个问题",
        ),
    )

    await repository.append_message(
        user_id="user-001",
        conversation_id="conv-001",
        message=ConversationMessage(
            role="assistant",
            content="第一个回答",
        ),
    )

    history = await repository.get_history(
        user_id="user-001",
        conversation_id="conv-001",
    )

    assert len(history) == 2

    assert history[0].role == "user"
    assert history[0].content == "第一个问题"

    assert history[1].role == "assistant"
    assert history[1].content == "第一个回答"