#!/usr/bin/env python

"""Converts a CSV (comma-separated values) formatted table into a
MD (markdown) formatted equivalent.

The CSV-formatted lines is expected to come from STDIN. The MD-formatted output
is sent to STDOUT.

If comma is used as a delimiter, both command lines are valid:
    cat input.csv | ./csv2md.py > output.md
    cat input.csv | ./csv2md.py ',' > output.md

If semi-colon is used, then this should be specified instead:
    cat input.csv | ./csv2md.py ';' > output.md
"""

import sys

class ErrorHandler:
    def report(self, error_message):
        print(error_message, file=sys.stderr)
        sys.exit(1)

class ProcessArguments:
    def __init__(self, error_handler):
        self.error = error_handler
        self.help_text = None
        self.delimiter_char = None

    def _set_delimiter_char(self, delimiter_char):
        if delimiter_char in [';', ',']:
            self.delimiter_char = delimiter_char
        else:
            self.error.report('Invalid delimiter! You must use comma or semicolon!')

    def process(self, arguments):
        assert isinstance(arguments, list)
        del arguments[0]
        nr_of_arguments = len(sys.argv)
        if nr_of_arguments == 0:
            self._set_delimiter_char(',')
        elif nr_of_arguments == 1:
            argument = arguments[0].lower()
            if argument == '--help':
                self.help_text = program_info()
            else:
                self._set_delimiter_char(argument)
        else:
            self.error.report('Invalid arguments list!\n\n' + program_info())

    def help(self):
        return self.help_text

    def delimiter(self):
        return self.delimiter_char

class CSVToMarkdown:
    def __init__(self, delimiter_char, error_handler):
        self.error = error_handler
        assert delimiter_char in [';', ',']
        self.delimiter_char = delimiter_char
        # The first row is assumed to be the header row.
        self.is_header_row = True

    def convert(self, line):
        line = line.replace('\r', '').replace('\n', '')
        if not line.isprintable():
            self.error.report('Non-printable characters!')
            return None
        output = '|' + line.replace(self.delimiter_char, '|') + '|'
        if self.is_header_row:
            output += '\n|' + '---|' * (line.count(self.delimiter_char) + 1)
            self.is_header_row = False
        return output

def program_info():
    info =  'Converts a CSV (comma-separated values) formatted table into a ' +     \
            'MD (markdown) formatted equivalent.\n\n' +                             \
            'The CSV-formatted lines is expected to come from STDIN. The ' +        \
            'MD-formatted output is sent to STDOUT.\n\n' +                          \
            'If comma is used as a delimiter, both command lines are valid:\n' +    \
            '\tcat input.csv | ./csv2md.py > output.md\n' +                         \
            '\tcat input.csv | ./csv2md.py \',\' > output.md\n\n' +                 \
            'If semi-colon is used, then this should be specified instead:\n' +     \
            '\tcat input.csv | ./csv2md.py \';\' > output.md'
    return info

if __name__ == '__main__':
    error_handler = ErrorHandler()
    arguments = ProcessArguments(error_handler)
    arguments.process(sys.argv)
    if arguments.help() != None:
        print(arguments.help())
        sys.exit()
    converter = CSVToMarkdown(arguments.delimiter(), error_handler)
    for line in sys.stdin:
        converted_line = converter.convert(line)
        print(converted_line, flush=True)