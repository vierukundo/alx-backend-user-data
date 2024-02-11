#!/usr/bin/env python3
"""obfuscate log message"""
from typing import List
import re
import logging


def filter_datum(
        fields: List[str], redaction: str,
        message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    for field in fields:
        message = re.sub(
                r'(?<={}=)[^{}]+'.format(
                    field, separator), redaction, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self._fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter values in incoming log records using filter_datum"""
        message = record.getMessage()
        record.msg = filter_datum(
                self._fields, RedactingFormatter.REDACTION,
                message, RedactingFormatter.SEPARATOR)
        return super().format(record)


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """Configure and return a logger named 'user_data'"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)

    formatter = RedactingFormatter(fields=PII_FIELDS)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.propagate = False

    return logger
