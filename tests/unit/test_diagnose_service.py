#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：test_diagnose_service.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/23 08:35 
@Description： 
'''
import pytest

from app.agent.agent_runner import AgentRunner
from app.application.diagnose_service import DiagnoseService
from app.domain.agent.tool_call_recorder import ToolCallRecorder
from app.domain.models import DiagnoseRequest
from app.infrastructure.agent.tool_call_repository import ToolCallRepository
from app.infrastructure.conversation.memory_conversation_repository import MemoryConversationRepository

from app.agent.diagnose_agent import DiagnoseAgent
from app.tools.executor import ToolExecutor
class FakeToolCallRecorder(ToolCallRecorder):

    async def start(
        self,
        run_id: int,
        tool_name: str,
        arguments: dict,
    ) -> int:
        return 1

    async def success(
        self,
        tool_call_id: int,
        result: dict,
    ) -> None:
        pass

    async def fail(
        self,
        tool_call_id: int,
    ) -> None:
        pass

@pytest.mark.asyncio
async def test_diagnose_service(fake_llm_client):
    from app.application.diagnose_service import DiagnoseService
    from app.domain.models import DiagnoseRequest

    agent = DiagnoseAgent(
        llm_client=fake_llm_client
    )
    tool_executor = ToolExecutor()
    tool_call_recoder = FakeToolCallRecorder()
    runner = AgentRunner(agent,tool_executor,tool_call_recoder)
    conversation_repository = MemoryConversationRepository()

    service = DiagnoseService(runner=runner, conversation_repository=conversation_repository)

    request = DiagnoseRequest(
        user_id="user-001",
        conversation_id="conv-001",
        message="测试问题",
    )

    result = await service.diagnose(request)

    assert result.diagnosis == "测试诊断"
    assert result.confidence == 0.9
    assert result.recommendations == ["测试建议"]

@pytest.mark.asyncio
async def test_diagnose_service_preserves_conversation_history(
    fake_llm_client,
):
    repository = MemoryConversationRepository()

    agent = DiagnoseAgent(
        llm_client=fake_llm_client
    )
    tool_executor = ToolExecutor()
    tool_call_recoder = FakeToolCallRecorder()
    runner = AgentRunner(agent,tool_executor,tool_call_recoder)
    service = DiagnoseService(
        runner=runner,
        conversation_repository=repository,
    )

    request = DiagnoseRequest(
        user_id="user-001",
        conversation_id="conv-001",
        message="第一个问题",
    )

    await service.diagnose(request)

    history = await repository.get_history(
        user_id="user-001",
        conversation_id="conv-001",
    )

    assert len(history) == 2

    assert history[0] == {
        "role": "user",
        "content": "第一个问题",
    }

    assert history[1] == {
        "role": "assistant",
        "content": "测试诊断",
    }
@pytest.mark.asyncio
async def test_diagnose_service_loads_previous_history(
    fake_llm_client,
):
    repository = MemoryConversationRepository()

    agent = DiagnoseAgent(
        llm_client=fake_llm_client
    )
    tool_executor = ToolExecutor()
    tool_call_recorder = FakeToolCallRecorder()
    runner = AgentRunner(agent,tool_executor,tool_call_recorder)

    service = DiagnoseService(
        runner=runner,
        conversation_repository=repository,
    )

    first_request = DiagnoseRequest(
        user_id="user-001",
        conversation_id="conv-001",
        message="我的电脑运行很慢",
    )

    await service.diagnose(first_request)

    second_request = DiagnoseRequest(
        user_id="user-001",
        conversation_id="conv-001",
        message="尤其是打开程序很慢",
    )

    await service.diagnose(second_request)

    prompt = fake_llm_client.last_prompt

    assert "我的电脑运行很慢" in prompt
    assert "测试诊断" in prompt
    assert "尤其是打开程序很慢" in prompt