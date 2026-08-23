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
from app.domain.context import AgentContext


class AgentRunner:

    def __init__(
        self,
        agent
    ):
        self.agent = agent


    async def run(
        self,
        context: AgentContext
    ):
        return await self.agent.execute(
            context
        )