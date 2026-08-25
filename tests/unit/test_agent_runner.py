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
from app.domain.models import AgentAction, DiagnoseResponse


class FakeAgent(BaseAgent):

    def __init__(self, llm_client=None):
        super().__init__(llm_client)
        self.count = 0

    def build_prompt(self, context):
        return ""

    def parse_action(self, result: str):
        pass

    def parse_response(self, result: str):
        pass

    async def execute(self, context):

        self.count += 1

        # 第一次调用 Agent，需要工具
        if self.count == 1:
            return AgentAction(
                action="tool_call",
                tool_name="system_info",
                arguments={},
            )

        # 第二次调用 Agent，根据工具结果生成最终答案
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

    def __init__(self):
        self.called = False

    async def execute(
        self,
        tool_name: str,
        **kwargs
    ):
        self.called = True

        assert tool_name == "system_info"

        return {
            "cpu": "20%",
            "memory": "50%",
            "disk": "60%",
        }


@pytest.mark.asyncio
async def test_agent_runner_tool_call_flow():

    agent = FakeAgent()

    tool_executor = FakeToolExecutor()

    runner = AgentRunner(
        agent=agent,
        tool_executor=tool_executor,
    )

    context = DiagnosisContext(
        user_id="user-001",
        conversation_id="conv-001",
        message="帮我看看电脑状态",
        history=[],
    )

    result = await runner.run(context)

    # 最终必须返回 final
    assert result.action == "final"

    # final 必须带 response
    assert result.response is not None

    assert result.response.diagnosis == "电脑状态正常"

    assert result.response.confidence == 0.9

    assert result.response.recommendations == [
        "保持系统更新"
    ]

    # Agent 被调用两次
    # 第一次：决定调用工具
    # 第二次：根据工具结果生成答案
    assert agent.count == 2

    # ToolExecutor 被调用
    assert tool_executor.called is True

    # Tool结果写入上下文
    assert context.metadata["tool_result"]["cpu"] == "20%"

    assert context.metadata["tool_result"]["memory"] == "50%"