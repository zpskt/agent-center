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
from app.domain.agent.tool_call_recorder import ToolCallRecorder
from app.domain.context import AgentContext
from app.domain.models import AgentRunResult
from app.infrastructure.logging.logger import get_logger
from app.tools.executor import ToolExecutor

logger = get_logger(__name__)
class AgentRunner:

    def __init__(
        self,
        agent: BaseAgent,
        tool_executor: ToolExecutor,
        tool_call_recorder: ToolCallRecorder,

    ):
        self.agent = agent
        self.tool_executor = tool_executor
        self.tool_call_recorder = tool_call_recorder


    async def run(
            self,
            context: AgentContext,
            run_id: int,
    ) -> AgentRunResult:

        MAX_ITERATIONS = 5
        logger.info(
            "Agent run started | run_id=%s | conversation_id=%s",
            run_id,
            context.conversation_id,
        )
        for iteration in range(1, MAX_ITERATIONS + 1):

            action = await self.agent.execute(context)

            if action.action == "final":
                return AgentRunResult(
                    action=action,
                    iterations=iteration,
                )

            if action.action == "tool_call":
                tool_call_id = await self.tool_call_recorder.start(
                    run_id=run_id,
                    tool_name=action.tool_name,
                    arguments=action.arguments,
                )

                try:
                    result = await self.tool_executor.execute(
                        action.tool_name,
                        **action.arguments,
                    )

                    await self.tool_call_recorder.success(
                        tool_call_id=tool_call_id,
                        result=result,
                    )

                    context.metadata["tool_result"] = result

                except Exception:
                    logger.exception(
                        "Tool call failed | run_id=%s | tool_call_id=%s | tool=%s",
                        run_id,
                        tool_call_id,
                        action.tool_name,
                    )
                    await self.tool_call_recorder.fail(
                        tool_call_id=tool_call_id,
                    )
                    raise
        logger.error(
            "Agent exceeded max iterations | run_id=%s | max_iterations=%s",
            run_id,
            MAX_ITERATIONS,
        )
        raise RuntimeError(
            "Agent exceeded max iterations"
        )