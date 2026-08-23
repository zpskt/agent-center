#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：context.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/23 18:13 
@Description： Agent上下文
'''
from abc import ABC
from pydantic import BaseModel,Field
from typing import Literal


class ConversationMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class AgentContext(BaseModel,ABC):
    user_id: str
    conversation_id: str
    message: str
    history: list[ConversationMessage] = Field(
        default_factory=list
    )
    metadata: dict = Field(
        default_factory=dict
    )
    available_tools: list[str] = Field(
        default_factory=list
    )

class DiagnosisContext(AgentContext):
    pass
