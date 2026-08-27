#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：settings.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/22 21:51 
@Description： 
'''
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    llm_api_key: str
    llm_model: str
    llm_base_url: str
    llm_timeout: int
    database_url: str
    database_echo: bool = False
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings()