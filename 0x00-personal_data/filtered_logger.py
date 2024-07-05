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
