#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：exception_handlers.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/23 10:09 
@Description： 
'''
from fastapi import Request
from fastapi.responses import JSONResponse

from app.domain.exceptions import LLMResponseError


async def llm_error_handler(
    request: Request,
    exc: LLMResponseError,
):
    return JSONResponse(
        status_code=502,
        content={
            "message": str(exc)
        },
    )