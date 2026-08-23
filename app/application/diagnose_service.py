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
from app.agent.diagnose_agent import DiagnoseAgent
from app.domain.context import DiagnosisContext, ConversationMessage
from app.domain.models import DiagnoseRequest
from app.domain.repositories.conversation_repository import ConversationRepository


class DiagnoseService:
    def __init__(self, agent:DiagnoseAgent, conversation_repository:ConversationRepository):
        self.agent = agent
        self.conversation_repository = conversation_repository

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

        context = DiagnosisContext(
            user_id=request.user_id,
            conversation_id=request.conversation_id,
            message=request.message,
            history=history,
        )

        result = await self.agent.execute(context)

        await self.conversation_repository.append_message(
            user_id=request.user_id,
            conversation_id=request.conversation_id,
            message=ConversationMessage(
                role="assistant",
                content=result.diagnosis,
            )
        )

        return result
