#!/usr/bin/env python3

import re
from typing import List
"""
   A function called filter_datum that returns the log
   message obfuscated
"""

import logging

PII_FIELDS = ("ssn", "password", "ip", "name", "email")
def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    A function that replaces personal info with
    redaction
    """
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message

def get_logger() -> logging.Logger:
    """
      Function that creates a custom logger, and
      sets it format, level and gives it handler.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.propagate = False
    logger.addHandler(stream_handler)

    return logger


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields=None):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.field = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg = filter_datum(self.field, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)
