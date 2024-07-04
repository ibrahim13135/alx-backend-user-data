#!/usr/bin/env python3
import logging
import re


def filter_datum(
        fields: list,
        redaction: str,
        message: str,
        separator: str) -> str:
    """Return the log message obfuscated."""
    for field in fields:
        message = re.sub(
            f'{field}=[^ {separator}]*',
            f'{field}={redaction}',
            message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: list):
        """ Initialize the formatter with specific fields to redact """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Format the log record to redact specified fields """
        original_message = super().format(record)
        redacted_message = filter_datum(
            self.fields,
            self.REDACTION,
            original_message,
            self.SEPARATOR)
        return redacted_message
