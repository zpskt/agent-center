#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：agent_run_repository.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/27 00:06 
@Description： 
'''
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models import AgentRunModel


class AgentRunRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        user_id: str,
        conversation_id: str,
        agent_name: str,
    ) -> AgentRunModel:

        run = AgentRunModel(
            user_id=user_id,
            conversation_id=conversation_id,
            agent_name=agent_name,
            status="running",
            iterations=0,
        )

        self.session.add(run)

        await self.session.flush()

        return run

    async def complete(
        self,
        run: AgentRunModel,
        iterations: int,
    ):

        run.status = "success"
        run.iterations = iterations
        run.finished_at = datetime.utcnow()

        await self.session.commit()

    async def fail(
        self,
        run: AgentRunModel,
        iterations: int,
    ):

        run.status = "failed"
        run.iterations = iterations
        run.finished_at = datetime.utcnow()

        await self.session.commit()
