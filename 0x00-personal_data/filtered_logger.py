#!/usr/bin/env python3
"""
This module contains the filter_datum function for obfuscating PII fields.
"""

import re
from typing import List


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
