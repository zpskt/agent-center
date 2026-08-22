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
from app.domain.models import DiagnoseRequest

class DiagnoseService:
    def __init__(self,agent:DiagnoseAgent):
        self.agent = agent
    def diagnose(self,request: DiagnoseRequest):
        return self.agent.excute(request)
