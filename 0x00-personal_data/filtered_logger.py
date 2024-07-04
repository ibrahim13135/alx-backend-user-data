#!/usr/bin/env python3
"""
This module contains the filter_datum function for obfuscating PII fields.
"""

import re
from typing import List
import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: list):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        real_messeges = super().format(record)
        filter_messeges = filter_datum(
            self.fields,
            self.REDACTION,
            real_messeges,
            self.SEPARATOR)
        return filter_messeges


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    """
    Returns the log message obfuscated by replacing specified fields
    with a redaction string.

    Args:
        fields (List[str]): A list of strings representing
        all fields to obfuscate.
        redaction (str): A string representing by
          what the field will be obfuscated.
        message (str): A string representing the log line.
        separator (str): A string representing the
          character separating all fields in the log line.

    Returns:
        str: The obfuscated log message.
    """
    pattern = f"({'|'.join(fields)})=.*?{separator}"
    return re.sub(
        pattern,
        lambda m: f"{m.group(1)}={redaction}{separator}",
        message)
