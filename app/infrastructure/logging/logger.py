#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：agent-center 
@File    ：logger.py
@IDE     ：PyCharm 
@Author  ：张鹏
@Date    ：2026/8/27 23:08 
@Description： 
'''
import logging

from app.config.settings import settings


def setup_logging() -> None:
    logging.basicConfig(
        level=getattr(
            logging,
            settings.log_level.upper(),
            logging.INFO,
        ),
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
    )


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)