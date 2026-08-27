#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：tool_call_repository.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/27 22:15 
@Description： 
'''
from datetime import datetime

from app.domain.agent.tool_call_recorder import ToolCallRecorder
from app.infrastructure.database.models import ToolCallModel
from sqlalchemy.ext.asyncio import AsyncSession


class ToolCallRepository(ToolCallRecorder):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def start(
        self,
        run_id: int,
        tool_name: str,
        arguments: dict,
    ) -> int:

        tool_call = ToolCallModel(
            run_id=run_id,
            tool_name=tool_name,
            arguments=arguments,
            status="running",
        )

        self.session.add(tool_call)

        await self.session.flush()

        return tool_call.id

    async def create(
        self,
        run_id: int,
        tool_name: str,
        arguments: dict,
    ) -> ToolCallModel:

        tool_call = ToolCallModel(
            run_id=run_id,
            tool_name=tool_name,
            arguments=arguments,
            status="running",
        )

        self.session.add(tool_call)

        await self.session.flush()

        return tool_call

    async def success(
            self,
            tool_call_id: int,
            result: dict,
    ) -> None:
        tool_call = await self.session.get(
            ToolCallModel,
            tool_call_id,
        )

        if tool_call is None:
            raise ValueError(
                f"ToolCall not found: {tool_call_id}"
            )

        tool_call.result = result
        tool_call.status = "success"
        tool_call.finished_at = datetime.utcnow()

        await self.session.flush()

    async def fail(
        self,
        tool_call: ToolCallModel,
    ):

        tool_call.status = "failed"
        tool_call.finished_at = datetime.utcnow()

        await self.session.flush()