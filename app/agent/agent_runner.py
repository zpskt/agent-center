#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：agent_runner.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/23 19:34 
@Description： 负责调度、循环、工具调用
'''
from app.agent.base_agent import BaseAgent
from app.domain.context import AgentContext
from app.tools.executor import ToolExecutor


class AgentRunner:

    def __init__(
        self,
        agent: BaseAgent,
        tool_executor: ToolExecutor
    ):
        self.agent = agent
        self.tool_executor = tool_executor


    async def run(
        self,
        context: AgentContext
    ):
        MAX_ITERATIONS = 5
        for _ in range(MAX_ITERATIONS):

            action = await self.agent.execute(context)

            if action.action == "final":
                return action

            if action.action == "tool_call":
                result = await self.tool_executor.execute(
                    action.tool_name,
                    **action.arguments
                )
                # 把当前工具执行结果保存下来
                context.metadata["tool_result"] = result

        raise RuntimeError(
            "Agent exceeded max iterations"
        )