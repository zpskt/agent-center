#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：sqlalchemy_conversation_repository.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/26 23:52 
@Description： 
'''
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.context import ConversationMessage
from app.domain.repositories.conversation_repository import ConversationRepository
from app.infrastructure.database.models import (
    ConversationModel,
    ConversationMessageModel,
)


class SQLAlchemyConversationRepository(ConversationRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_history(
        self,
        user_id: str,
        conversation_id: str,
    ) -> list[ConversationMessage]:

        result = await self.session.execute(
            select(ConversationMessageModel)
            .join(
                ConversationModel,
                ConversationMessageModel.conversation_id
                == ConversationModel.conversation_id,
            )
            .where(
                ConversationModel.user_id == user_id,
                ConversationModel.conversation_id == conversation_id,
            )
            .order_by(ConversationMessageModel.created_at)
        )

        rows = result.scalars().all()

        return [
            ConversationMessage(
                role=row.role,
                content=row.content,
            )
            for row in rows
        ]

    async def append_message(
        self,
        user_id: str,
        conversation_id: str,
        message: ConversationMessage,
    ) -> None:

        conversation = await self.session.scalar(
            select(ConversationModel).where(
                ConversationModel.user_id == user_id,
                ConversationModel.conversation_id == conversation_id,
            )
        )

        if conversation is None:
            conversation = ConversationModel(
                user_id=user_id,
                conversation_id=conversation_id,
            )

            self.session.add(conversation)
            await self.session.flush()

        self.session.add(
            ConversationMessageModel(
                conversation_id=conversation_id,
                role=message.role,
                content=message.content,
            )
        )

        await self.session.commit()