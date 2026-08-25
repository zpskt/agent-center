#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：test_agent_action.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/23 19:14 
@Description： 
'''
from app.domain.models import AgentAction


def test_tool_call_action():

    action = AgentAction(
        action="tool_call",
        tool_name="system_info",
        arguments={}
    )

    assert action.action == "tool_call"

    assert action.tool_name == "system_info"


def test_final_action():

    action = AgentAction(
        action="final",
    tool_name = "system_info",
    arguments = {}
    )

    assert action.action == "final"