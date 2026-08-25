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

from app.agent.agent_runner import AgentRunner
from app.agent.base_agent import BaseAgent
from app.agent.diagnose_agent import DiagnoseAgent
from app.application.diagnose_service import DiagnoseService
from app.domain.models import DiagnoseRequest, DiagnoseResponse
from app.domain.repositories.conversation_repository import ConversationRepository
from app.infrastructure.conversation.memory_conversation_repository import MemoryConversationRepository
from app.infrastructure.llm.deepseek_client import DeepSeekClient
from app.infrastructure.llm.fake_llm_client import FakeLLMClient
from app.infrastructure.llm.llm_client import LLMClient
from app.tools.executor import ToolExecutor


# ====================
# 添加依赖
# ====================
def get_conversation_repository() -> ConversationRepository:
    return MemoryConversationRepository()

def get_llm_client() -> LLMClient:
    return DeepSeekClient()

def get_tool_executor() -> ToolExecutor:
    return ToolExecutor()

def get_diagnose_agent(llm_client: LLMClient = Depends(get_llm_client)) -> DiagnoseAgent:
    return DiagnoseAgent(llm_client=llm_client)

def get_agent_runner(agent: DiagnoseAgent = Depends(get_diagnose_agent),tool_executor: ToolExecutor = Depends(get_tool_executor)) -> AgentRunner:
    return AgentRunner(agent=agent,tool_executor=tool_executor)

def get_diagnose_service(runner: AgentRunner = Depends(get_agent_runner),
                         conversation_repository: ConversationRepository = Depends(get_conversation_repository)) -> DiagnoseService:
    return DiagnoseService(runner=runner, conversation_repository=conversation_repository)

router = APIRouter(prefix='/diagnose')

@router.post('/',response_model=DiagnoseResponse)
async def diagnose(request: DiagnoseRequest, service: DiagnoseService = Depends(get_diagnose_service)):
    return await service.diagnose(request)