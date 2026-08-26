#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：test_agent_run_repository.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/27 00:09 
@Description： 
'''
from datetime import datetime

import pytest
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.infrastructure.agent.agent_run_repository import (
    AgentRunRepository,
)
from app.infrastructure.database.models import (
    AgentRunModel,
    Base,
)


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
async def test_create_agent_run(session):

    repository = AgentRunRepository(session)

    run = await repository.create(
        user_id="user-001",
        conversation_id="conv-001",
        agent_name="diagnose",
    )

    assert run.id is not None
    assert run.user_id == "user-001"
    assert run.conversation_id == "conv-001"
    assert run.agent_name == "diagnose"
    assert run.status == "running"
    assert run.iterations == 0
    assert run.finished_at is None


@pytest.mark.asyncio
async def test_complete_agent_run(session):

    repository = AgentRunRepository(session)

    run = await repository.create(
        user_id="user-001",
        conversation_id="conv-001",
        agent_name="diagnose",
    )

    await repository.complete(
        run=run,
        iterations=2,
    )

    assert run.status == "success"
    assert run.iterations == 2
    assert run.finished_at is not None
    assert isinstance(run.finished_at, datetime)


@pytest.mark.asyncio
async def test_fail_agent_run(session):

    repository = AgentRunRepository(session)

    run = await repository.create(
        user_id="user-001",
        conversation_id="conv-001",
        agent_name="diagnose",
    )

    await repository.fail(
        run=run,
        iterations=3,
    )

    assert run.status == "failed"
    assert run.iterations == 3
    assert run.finished_at is not None