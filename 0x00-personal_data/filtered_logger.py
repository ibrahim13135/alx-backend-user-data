#!/usr/bin/env python3
"""
This module contains the filter_datum function for obfuscating PII fields.
"""

import re
from typing import List
import logging
import mysql.connector
import os
from os import environ



class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Returns filtered values from log records """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ Returns regex obfuscated log messages """
    for field in fields:
        message = re.sub(f'{field}=(.*?){separator}',
                         f'{field}={redaction}{separator}', message)
    return message


# Define the PII_FIELDS constant
PII_FIELDS = ("name", "email", "password", "ssn", "phone")


def get_logger() -> logging.Logger:
    """Creates and returns a logger named 'user_data'"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Create and configure the StreamHandler
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Connection to MySQL environment """
    db_connect = mysql.connector.connect(
        user=environ.get('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=environ.get('PERSONAL_DATA_DB_PASSWORD', ''),
        host=environ.get('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=environ.get('PERSONAL_DATA_DB_NAME')
    )
    return db_connect
