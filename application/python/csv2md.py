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
import re

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
        self.buffered_tokens = None
        self.unfinished_quote = False
        # The first row is assumed to be the header row.
        self.is_header_row = True

    @staticmethod
    def _tokenize(line, delimiter, unfinished_quote=False):
        """Divide line into tokens.

        The string is separated into tokens where delimiter is found, except
        where the delimiter is found within quotation marks.
        """
        assert isinstance(line, str)
        assert (isinstance(delimiter, str)) and (len(delimiter) == 1)
        tokens = []
        found_quote = False
        while line != '':
            if found_quote or unfinished_quote:
                quote, unfinished_quote, line = CSVToMarkdown._extract_quote(line, unfinished_quote)
                if quote != None:
                    tokens.append(quote)
                line = CSVToMarkdown._after_delimiter(line, delimiter)
            line, remaining_line = CSVToMarkdown._line_to_split(line, delimiter)
            if line != '':
                tokens += line.split(delimiter)
            line = remaining_line
            found_quote = (line != '')
        return tokens, unfinished_quote

    @staticmethod
    def _extract_quote(line, unfinished_quote):
        if unfinished_quote:
            end_quote_pos = line.find('"')
        else:
            quote_pos = line.find('"')
            if quote_pos == -1:
                quote = None
                remaining_line = line
                end_quote_pos = -1
            else:
                end_quote_pos = line.find('"', quote_pos + 1)
        if end_quote_pos == -1:
            unfinished_quote = True
            quote = line
            remaining_line = ''
        else:
            unfinished_quote = False
            quote = line[:end_quote_pos + 1]
            remaining_line = line[end_quote_pos + 1:]
        return quote, unfinished_quote, remaining_line
    
    @staticmethod
    def _after_delimiter(line, delimiter):
        delimiter_pos = line.find(delimiter)
        if delimiter_pos == -1:
            return ''
        return line[delimiter_pos + 1:]

    @staticmethod
    def _until_quote(line, delimiter):
        quote_pos = line.find('"')
        assert quote_pos != -1
        delimiter_pos = line[:quote_pos].rfind(delimiter)
        if delimiter_pos == -1:
            remaining_line = line
            line = ''
        else:
            remaining_line = line[quote_pos:]
            line = line[:delimiter_pos]
        return line, remaining_line

    @staticmethod
    def _line_to_split(line, delimiter):
        if line.count('"') == 0:
            return line, ''
        return CSVToMarkdown._until_quote(line, delimiter)

    @staticmethod
    def _sanitize(tokens):
        """Strip tokens from surrounding whitespace and quotation marks.
        """
        assert isinstance(tokens, list)
        sanitized_tokens = []
        for token in tokens:
            sanitized_token = token.strip()
            sanitized_token = re.sub(r'^"(.*)', r'\1', sanitized_token)
            sanitized_token = re.sub(r'(.*)"$', r'\1', sanitized_token)
            sanitized_tokens.append(sanitized_token)
        return sanitized_tokens
        
    def _parse(self, line):
        """Parse lines.
        
        When a line (or several lines) are parsed, then these will be returned
        as a list of tokens. If parsing has not finished, then None will be 
        returned instead.
        """
        parsed_tokens = None
        tokens, self.unfinished_quote = self._tokenize(line, self.delimiter_char, self.unfinished_quote)
        if self.buffered_tokens == None:
            if self.unfinished_quote:
                self.buffered_tokens = tokens
            else:
                parsed_tokens = tokens
        else:
            last_buffered_token = self.buffered_tokens.pop()
            tokens[0] = last_buffered_token + '<br>' + tokens[0]
            self.buffered_tokens += tokens
            if not self.unfinished_quote:
                parsed_tokens = self.buffered_tokens
                self.buffered_tokens = None
        return parsed_tokens

    def _md_row(self, tokens):
        """Create a MD-formatted table row from tokens.
        """
        assert isinstance(tokens, list)
        assert len(tokens) > 0
        md_row = '|' + '|'.join(tokens) + '|'
        if self.is_header_row:
            md_row += '\n|' + '---|' * len(tokens)
            self.is_header_row = False
        return md_row

    def convert(self, line):
        """Convert a line, from CSV to MD.

        None will be returned for an empty line or when a table row is divided
        into multiple lines.
        """
        converted_line = None
        line = line.replace('\r', '').replace('\n', '')
        if not line.isprintable():
            self.error.report('Non-printable characters!')
        elif line != '':
            parsed_tokens = self._parse(line)
            if parsed_tokens != None:
                sanitized_tokens = self._sanitize(parsed_tokens)
                converted_line = self._md_row(sanitized_tokens)
        return converted_line

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
        if converted_line != None:
            print(converted_line, flush=True)