#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：diagnose.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/22 17:41 
@Description： 
'''
from fastapi import APIRouter
from fastapi.params import Depends

from app.agent.diagnose_agent import DiagnoseAgent
from app.application.diagnose_service import DiagnoseService
from app.domain.models import DiagnoseRequest, DiagnoseResponse
from app.infrastructure.llm.llm_client import LLMClient

# ====================
# 添加依赖
# ====================

def get_llm_client() -> LLMClient:
    return LLMClient()
def get_diagnose_agent(llm_client: LLMClient = Depends(get_llm_client)) -> DiagnoseAgent:
    return DiagnoseAgent(llm_client=llm_client)
def get_diagnose_service(agent: DiagnoseAgent = Depends(get_diagnose_agent)) -> DiagnoseService:
    return DiagnoseService(agent=agent)

router = APIRouter(prefix='/diagnose')


@router.post('/',response_model=DiagnoseResponse)
def diagnose(request: DiagnoseRequest, service: DiagnoseService = Depends(get_diagnose_service)):
    return service.diagnose(request)