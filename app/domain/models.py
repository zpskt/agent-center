#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：models.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/22 17:42 
@Description： 
'''
from pydantic import BaseModel,Field
from typing import Literal

class ConversationMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class DiagnoseRequest(BaseModel):
    """
    请求体
    """
    message: str
    conversation_id: str
    user_id: str


class DiagnoseResponse(BaseModel):
    diagnosis: str
    confidence: float
    recommendations: list[str]

class DiagnosisContext(BaseModel):
    user_id: str
    conversation_id: str
    message: str
    history: list[ConversationMessage] = Field(default_factory=list)