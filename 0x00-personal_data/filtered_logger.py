#!/usr/bin/env python3

import re
from typing import List
"""
   A function called filter_datum that returns the log
   message obfuscated
"""


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
      A function that replaces personal info with
      redaction
    """

    for field in fields:
        pattern = f'{field}=.*?{separator}'
        repl = f'{field}={redaction}{separator}'
        input_str = message
        message = re.sub(pattern, repl, input_str)
    return message
