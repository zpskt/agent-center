#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：conversation_repository.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/23 09:04 
@Description： 
'''
from abc import abstractmethod, ABC

from app.domain.models import ConversationMessage


class ConversationRepository(ABC):
    @abstractmethod
    async def get_history(
        self,
        user_id: str,
        conversation_id: str,
    ) -> list[ConversationMessage]:
        ...

    @abstractmethod
    async def append_message(
        self,
        user_id: str,
        conversation_id: str,
        message: ConversationMessage,
    ) -> None:
        ...
