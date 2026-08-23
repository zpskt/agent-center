#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：memory_conversation_repository.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/23 09:05 
@Description： 
'''
from app.domain.repositories.conversation_repository import ConversationRepository


class MemoryConversationRepository(ConversationRepository):

    def __init__(self):
        self._conversations: dict[
            tuple[str, str],
            list[dict[str, str]]
        ] = {}

    async def get_history(
        self,
        user_id: str,
        conversation_id: str,
    ) -> list[dict[str, str]]:
        key = (user_id, conversation_id)

        return self._conversations.get(key, []).copy()

    async def append_message(
        self,
        user_id: str,
        conversation_id: str,
        role: str,
        content: str,
    ) -> None:
        key = (user_id, conversation_id)

        if key not in self._conversations:
            self._conversations[key] = []

        self._conversations[key].append({
            "role": role,
            "content": content,
        })