# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from logging import FileHandler

from colorlog import ColoredFormatter
from pythonjsonlogger import jsonlogger

__license__ = "Apache License, Version 2.0"
__author__ = "Carmen Tawalika"
__copyright__ = "Copyright 2019-2021, mundialis"
__maintainer__ = "Carmen Tawalika"


# TODO make configurable
class LogConfig(object):
    def __init__(self):
        self.logfile = "/openeo-grassgis-driver.log"
        self.level = "INFO"
        self.type = "json"


LOGCONFIG = LogConfig()

log = logging.getLogger('openeo-grass-gis-driver')
werkzeugLog = logging.getLogger('werkzeug')
gunicornLog = logging.getLogger('gunicorn')


def setLogFormat(veto=None):
    # "veto" is used for fileformat, so "type=json" is only applied to stdout
    logformat = ""
    if LOGCONFIG.type == 'json' and not veto:
        logformat = CustomJsonFormatter('%(time) %(level) %(component)'
                                        '%(module) %(message) %(pathname)'
                                        '%(lineno) %(processName)'
                                        '%(threadName)')
    else:
        logformat = ColoredFormatter(
            '%(log_color)s[%(asctime)s] %(levelname)-10s: %(name)s.%(module)-'
            '10s -%(message)s [in %(pathname)s:%(lineno)d]%(reset)s'
        )
    return logformat


def setLogHandler(logger, type, format):
    if type == 'stdout':
        handler = logging.StreamHandler()
    elif type == 'file':
        # For readability, json is never written to file
        handler = FileHandler(LOGCONFIG.logfile)
    handler.setFormatter(format)
    logger.addHandler(handler)


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(
            log_record, record, message_dict)

        # (Pdb) dir(record)
        # ... 'args', 'created', 'exc_info', 'exc_text', 'filename', 'funcName'
        # ,'getMessage', 'levelname', 'levelno', 'lineno', 'message', 'module',
        # 'msecs', 'msg', 'name', 'pathname', 'process', 'processName',
        # 'relativeCreated', 'stack_info', 'thread', 'threadName']

        now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        log_record['time'] = now
        log_record['level'] = record.levelname
        log_record['component'] = record.name


def createLogger():
    # create logger, set level and define format
    log.setLevel(getattr(logging, LOGCONFIG.level))
    fileformat = setLogFormat('veto')
    stdoutformat = setLogFormat()
    setLogHandler(log, 'file', fileformat)
    setLogHandler(log, 'stdout', stdoutformat)


def createWerkzeugLogger():
    werkzeugLog.setLevel(getattr(logging, LOGCONFIG.level))
    fileformat = setLogFormat('veto')
    stdoutformat = setLogFormat()
    setLogHandler(werkzeugLog, 'file', fileformat)
    setLogHandler(werkzeugLog, 'stdout', stdoutformat)


def createGunicornLogger():
    gunicornLog.setLevel(getattr(logging, LOGCONFIG.level))
    fileformat = setLogFormat('veto')
    stdoutformat = setLogFormat()
    setLogHandler(gunicornLog, 'file', fileformat)
    setLogHandler(gunicornLog, 'stdout', stdoutformat)
    # gunicorn already has a lot of children logger, e.g gunicorn.http,
    # gunicorn.access. These lines deactivate their default handlers.
    for name in logging.root.manager.loggerDict:
        if "gunicorn." in name:
            logging.getLogger(name).propagate = True
            logging.getLogger(name).handlers = []


createLogger()
createWerkzeugLogger()
createGunicornLogger()
