#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：diagnose_agent.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/22 21:03 
@Description： 
'''
from app.domain.models import DiagnoseRequest
from app.infrastructure.llm.llm_client import LLMClient


class DiagnoseAgent:
    def __init__(self,llm_client: LLMClient):
        self.llm_client = llm_client;
    def excute(self,request:DiagnoseRequest):
        return self.llm_client.invoke(request.message)
