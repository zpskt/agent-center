#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：registry.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/23 18:27 
@Description： 
'''
from app.prompts.diagnose import build_prompt


PROMPTS = {
    "diagnose": build_prompt
}


def get_prompt(name: str):
    return PROMPTS[name]