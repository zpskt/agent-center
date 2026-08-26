#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：diagnose_service.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/22 20:53 
@Description： 
'''
from app.agent.agent_runner import AgentRunner
from app.domain.context import DiagnosisContext, ConversationMessage
from app.domain.exceptions import DiagnosisError
from app.domain.models import DiagnoseRequest
from app.domain.repositories.conversation_repository import ConversationRepository
from app.tools.registry import get_all_tools


class DiagnoseService:
    def __init__(self, conversation_repository:ConversationRepository, runner:AgentRunner):
        self.conversation_repository = conversation_repository
        self.runner = runner

    async def diagnose(self, request: DiagnoseRequest):
        history = await self.conversation_repository.get_history(
            user_id=request.user_id,
            conversation_id=request.conversation_id,
        )
        await self.conversation_repository.append_message(
            user_id=request.user_id,
            conversation_id=request.conversation_id,
            message=ConversationMessage(
                role="user",
                content=request.message,
            ),
            )

        tools = [
            tool.get_schema()
            for tool in get_all_tools()
        ]
        context = DiagnosisContext(
            user_id=request.user_id,
            conversation_id=request.conversation_id,
            message=request.message,
            history=history,
            available_tools=tools,
        )

        action = await self.runner.run(context)

        if action.action == "final":
            if action.response is None:
                raise DiagnosisError("Agent 没有返回诊断结果")

            await self.conversation_repository.append_message(
                user_id=request.user_id,
                conversation_id=request.conversation_id,
                message=ConversationMessage(
                    role="assistant",
                    content=action.response.diagnosis,
                ),
            )

            return action.response
        raise DiagnosisError(
            f"Agent 未返回最终诊断结果: {action.action}"
        )