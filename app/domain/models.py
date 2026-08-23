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
from typing import Literal
from pydantic import BaseModel


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

class AgentAction(BaseModel):

    action: Literal[
        "tool_call",
        "final"
    ]

    tool_name: str | None = None

    arguments: dict = {}