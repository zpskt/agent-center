#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：test_agent_runner.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/26 00:00 
@Description： 
'''
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest

from app.agent.agent_runner import AgentRunner
from app.agent.base_agent import BaseAgent
from app.domain.context import DiagnosisContext
from app.domain.models import (
    AgentAction,
    AgentRunResult,
    DiagnoseResponse,
)


class FakeAgent(BaseAgent):

    def __init__(self):
        self.count = 0

    def build_prompt(self, context):
        return ""

    def parse_action(self, result):
        return result

    def parse_response(self, result):
        return result

    async def execute(self, context):

        self.count += 1

        if self.count == 1:
            return AgentAction(
                action="tool_call",
                tool_name="system_info",
                arguments={},
            )

        return AgentAction(
            action="final",
            response=DiagnoseResponse(
                diagnosis="电脑状态正常",
                confidence=0.9,
                recommendations=[
                    "保持系统更新"
                ],
            ),
        )


class FakeToolExecutor:

    async def execute(
        self,
        tool_name: str,
        **kwargs,
    ):

        assert tool_name == "system_info"

        return {
            "cpu": "20%",
            "memory": "50%",
            "disk": "60%",
        }


class FakeToolCallRecorder:

    def __init__(self):
        self.calls = []
        self.next_id = 1

    async def start(
        self,
        run_id: int,
        tool_name: str,
        arguments: dict,
    ) -> int:

        tool_call_id = self.next_id
        self.next_id += 1

        self.calls.append({
            "id": tool_call_id,
            "run_id": run_id,
            "tool_name": tool_name,
            "arguments": arguments,
            "status": "running",
        })

        return tool_call_id

    async def success(
        self,
        tool_call_id: int,
        result: dict,
    ) -> None:

        for call in self.calls:
            if call["id"] == tool_call_id:
                call["status"] = "success"
                call["result"] = result
                return

        raise AssertionError(
            f"Tool call not found: {tool_call_id}"
        )

    async def fail(
        self,
        tool_call_id: int,
    ) -> None:

        for call in self.calls:
            if call["id"] == tool_call_id:
                call["status"] = "failed"
                return

        raise AssertionError(
            f"Tool call not found: {tool_call_id}"
        )


@pytest.mark.asyncio
async def test_agent_runner_tool_call_flow():

    agent = FakeAgent()
    tool_executor = FakeToolExecutor()
    tool_call_recorder = FakeToolCallRecorder()

    runner = AgentRunner(
        agent=agent,
        tool_executor=tool_executor,
        tool_call_recorder=tool_call_recorder,
    )

    context = DiagnosisContext(
        user_id="user-001",
        conversation_id="conv-001",
        message="帮我看看电脑状态",
        history=[],
    )

    result = await runner.run(
        context,
        run_id=100,
    )

    assert isinstance(result, AgentRunResult)

    assert result.action.action == "final"

    assert result.action.response is not None

    assert result.action.response.diagnosis == "电脑状态正常"

    assert result.iterations == 2

    assert agent.count == 2

    assert context.metadata["tool_result"]["cpu"] == "20%"

    assert len(tool_call_recorder.calls) == 1

    tool_call = tool_call_recorder.calls[0]

    assert tool_call["run_id"] == 100
    assert tool_call["tool_name"] == "system_info"
    assert tool_call["arguments"] == {}
    assert tool_call["status"] == "success"

    assert tool_call["result"] == {
        "cpu": "20%",
        "memory": "50%",
        "disk": "60%",
    }