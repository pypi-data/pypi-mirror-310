# -*- coding: utf-8 -*-
# author: NhanDD3 <hp.duongducnhan@gmail.com>
import logging
import os
import json
import requests
from functools import wraps
from typing import Dict, List
from typing import Callable
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler
from pythonjsonlogger import jsonlogger


def json_translate_obj(obj):
    # for example, serialize a custom object
    # if isinstance(obj, MyClass):
    #     return {"special": obj.special}
    return {'obj': str(obj)}


def setup_time_rotation_logger(
    name, 
    level, 
    log_file_dir=None, 
    format_json=False, 
    json_translator=json_translate_obj
):
    if not log_file_dir:
        log_file_dir = os.path.join(Path.home(), "cmk-tools", "logs")

    if not os.path.isdir(log_file_dir):
        os.makedirs(log_file_dir, exist_ok=True)
    
    log_file_path = os.path.join(log_file_dir, f"{name}.log")
    # print("log files will be saved at:", log_file_path)

    logger = logging.getLogger(f'cmk-tools.{name}')
    logger.setLevel(logging.DEBUG)

    handler = TimedRotatingFileHandler(
        log_file_path, when="midnight", interval=1, backupCount=7
    )

    if format_json:
        formatter = jsonlogger.JsonFormatter(
            json_encoder=json.JSONEncoder,
            json_default=json_translator,
        )
    else:
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    handler.setFormatter(formatter)
    handler.setLevel(level)
    logger.addHandler(handler)
    return logger


def setup_log(name: str, level: int = logging.INFO):
    home_path = Path.home()
    log_dir = os.path.join(home_path, "fmon_active_check_logs")

    active_check_log_dir_name = name
    if active_check_log_dir_name.endswith([".log", ".txt"]):
        active_check_log_dir_name = active_check_log_dir_name.split(".")[0]
    log_dir = os.path.join(log_dir, active_check_log_dir_name)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = setup_time_rotation_logger(name, level, log_file_dir=log_dir, format_json=True)
    logger.debug = restruct_log_method(logger.debug)
    logger.info = restruct_log_method(logger.info)
    logger.warn = restruct_log_method(logger.warn)
    logger.error = restruct_log_method(logger.error)
    logger.critical = restruct_log_method(logger.critical)
    logger.exception = restruct_log_method(logger.exception, True)
    logger.warning = restruct_log_method(logger.warning)
    return logger

def restruct_log_method(func, exc_info: bool = None):
    @wraps(func)
    def structured_method(
        message,
        exc_info: bool = exc_info,
        extra: Dict = None,
        stack_info=False,
        stacklevel=1,
        **kwargs
    ):
        if not extra:
            extra = {}

        for k, v in kwargs.items():
            if k == 'api_resp' and isinstance(v, requests.Response):
                extra.update({
                    'api_request_url': v.request.url,
                    'api_request_method': v.request.method,
                    'api_request_headers': dict(v.request.headers),
                    'api_request_body': v.request.body.decode('utf-8'),
                    'api_status_code': v.status_code,
                    'api_response_text': v.text
                })
        try:
            return func(message, exc_info=exc_info, extra=extra, stack_info=stack_info, stacklevel=stacklevel)
        except Exception as e:
            new_extra = {'exc_extra': str(extra)}
            return func(message, exc_info=exc_info, extra=new_extra, stack_info=stack_info, stacklevel=stacklevel)
    return structured_method
