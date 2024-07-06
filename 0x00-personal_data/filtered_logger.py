#!/usr/bin/env python3
'''
Write a function called filter_datum that returns the log message obfuscated:

Arguments:
fields: a list of strings representing all fields to obfuscate
redaction: a string representing by what the field will be obfuscated
message: a string representing the log line
separator: a string representing by which character is separating all fields in
the log line (message)
The function should use a regex to replace occurrences of certain field values.
filter_datum should be less than 5 lines long and use re.sub to perform the
substitution with a single regex.
'''
from typing import List
import re
import logging
import mysql.connector

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(
        fields: List[str], redaction: str,
        message: str, separator: str) -> str:
    '''Returns the log message obfuscated.'''
    for field in fields:
        # Create the regex pattern for the current field
        pattern = fr'({field}=)[^{separator}]+({separator})'
        # Create the replacement string
        replacement = fr'\1{redaction}\2'
        # Substitute the pattern in the message
        message = re.sub(pattern, replacement, message)
    return message


def get_logger() -> logging.Logger:
    '''
    Use user_data.csv for this task

    Implement a get_logger function that takes no arguments and returns a
    logging.Logger object.

    The logger should be named "user_data" and only log up to logging.INFO
    level. It should not propagate messages to other loggers. It should have
    a StreamHandler with RedactingFormatter as formatter.

    Create a tuple PII_FIELDS constant at the root of the module containing the
    fields from user_data.csv that are considered PII. PII_FIELDS can contain
    only 5 fields - choose the right list of fields that can are considered as
    “important” PIIs or information that you must hide in your logs. Use it to
    parameterize the formatter.

    Tips:

    What Is PII, non-PII, and personal data?
    Uncovering Password Habits
    '''
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    '''
    Database credentials should NEVER be stored in code or checked into version
    control. One secure option is to store them as environment variable on the
    application server.

    In this task, you will connect to a secure holberton database to read a
    users table. The database is protected by a username and password that are
    set as environment variables on the server named PERSONAL_DATA_DB_USERNAME
    (set the default as “root”), PERSONAL_DATA_DB_PASSWORD (set the default
    as an empty string) and PERSONAL_DATA_DB_HOST (set the
    default as “localhost”).

    The database name is stored in PERSONAL_DATA_DB_NAME.

    Implement a get_db function that returns a connector to the database
    (mysql.connector.connection.MySQLConnection object).

    Use the os module to obtain credentials from the environment
    Use the module mysql-connector-python to connect to the MySQL database
    (pip3 install mysql-connector-python)
    '''
    from dotenv import load_dotenv
    import os

    load_dotenv()
    my_db = mysql.connector.connect(
        hostname=os.getenv('PERSONAL_DATA_DB_HOST', default='localhost'),
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', default='root'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', default=''),
        database=os.getenv('PERSONAL_DATA_DB_NAME')
    )
    return my_db


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        ''' The constructor method for the class'''
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''
        Update the class to accept a list of strings fields constructor
        argument.

        Implement the format method to filter values in incoming log records
        using filter_datum. Values for fields in fields should be filtered.

        DO NOT extrapolate FORMAT manually. The format method should be less
        than 5 lines long.
        '''
        record.msg = filter_datum(
            self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR)
        return super().format(record)
