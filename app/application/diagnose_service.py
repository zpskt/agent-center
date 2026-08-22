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
from app.domain.models import DiagnoseRequest, DiagnosisContext


class DiagnoseService:
    def __init__(self,agent:DiagnoseAgent):
        self.agent = agent
    async def diagnose(self,request: DiagnoseRequest):
        context = DiagnosisContext(
            user_id=request.user_id,
            message=request.message,
        )
        return await self.agent.execute(context)
