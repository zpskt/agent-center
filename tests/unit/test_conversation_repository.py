#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：test_conversation_repository.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/23 09:23 
@Description： 
'''
import pytest

from app.domain.context import ConversationMessage
from app.infrastructure.conversation.memory_conversation_repository import MemoryConversationRepository


@pytest.mark.asyncio
async def test_conversation_isolated_by_user():
    repository = MemoryConversationRepository()

    await repository.append_message(
        user_id="user-001",
        conversation_id="conv-001",
        message=ConversationMessage(
            role="user",
            content="用户1的问题",
        )
    )

    await repository.append_message(
        user_id="user-002",
        conversation_id="conv-001",
        message=ConversationMessage(
            role="user",
            content="用户2的问题",
        ),
    )

    history_1 = await repository.get_history(
        user_id="user-001",
        conversation_id="conv-001",
    )

    history_2 = await repository.get_history(
        user_id="user-002",
        conversation_id="conv-001",
    )

    assert history_1 == [
        {
            "role": "user",
            "content": "用户1的问题",
        }
    ]

    assert history_2 == [
        {
            "role": "user",
            "content": "用户2的问题",
        }
    ]
