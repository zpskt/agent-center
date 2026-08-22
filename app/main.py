#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：main.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/22 17:26 
@Description： 
'''
from urllib.request import Request

from fastapi import FastAPI
from starlette.responses import JSONResponse

from app.api.diagnose import router as diagnose_router
from app.api.health import router as health_router
from app.domain.exceptions import DiagnosisError

app = FastAPI()
@app.exception_handler(DiagnosisError)
async def diagnosis_exception_handler(
    request: Request,
    exc: DiagnosisError,
):
    return JSONResponse(
        status_code=500,
        content={
            "code": "DIAGNOSIS_ERROR",
            "message": exc.message,
        },
    )
app.include_router(health_router)
app.include_router(diagnose_router)

@app.get('/')
def root():
    return {"message":"hello"}