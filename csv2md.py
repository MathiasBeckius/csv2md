#!/usr/bin/env python

"""
Converts a CSV (comma-separated values) formatted file into a
MD (markdown) formatted table.

Usage: csv2md.py <source> <destination> <delimiter>

Author : Mathias Beckius
License: MIT
"""

import sys
import re

class FileOperation:
    def __init__(self, filename, mode):
        assert isinstance(filename, str)
        self.file = None
        self.error_msg = None
        try:
            self.file = open(filename, mode)
        except IOError as e:
            self.error_msg = 'Could not open "' + csvfile_path + '"'
            if e.strerror != None:
                self.error_msg += ', due to: ' + str(e.strerror)
        except:
            self.error_msg = 'Unexpected error: ' + str(sys.exc_info()[0])

    def error(self):
        return self.error_msg

    def close(self):
        if self.file != None:
            self.file.close()

class FileRead(FileOperation):
    def __init__(self, filename):
        FileOperation.__init__(self, filename, 'r')

    def lines(self):
        if self.file != None:
            return iter(self.file)
        else:
            return iter([])

    def lines_as_str(self):
        return ''.join(self.file.readlines())

class FileWrite(FileOperation):
    def __init__(self, filename):
        FileOperation.__init__(self, filename, 'w')

    def write(self, data):
        try:
            self.file.write(data)
        except IOError as e:
            self.error_msg = 'Could not write to "' + csvfile_path + '"'
            if e.strerror != None:
                self.error_msg += ', due to: ' + str(e.strerror)
        except:
            self.error_msg = 'Unexpected error: ' + str(sys.exc_info()[0])

def extract_program_info(contents_to_print = ""):
    contents_to_print = contents_to_print.lower()
    this_file = FileRead(sys.argv[0])
    contents = this_file.lines_as_str()
    start_pos = contents.find('"""')
    program_info = contents[start_pos + 3:contents.find('"""', start_pos + 1)]
    if contents_to_print == 'usage':
        start_pos = program_info.find('Usage:')
        end_pos = program_info.find('\n', start_pos)
        return program_info[start_pos:end_pos]
    else:
        return program_info
    this_file.close()

def valid_filename(filename):
    """Checks the validity of a filename.

    These are the rules:
    - the length of a filename must be at least one character (excl. file extension).
    - a file extension must 2 or 3 characters long.
    - the following characters are not valid: ? *
    """
    assert isinstance(filename, str)
    return (re.match('.{1,}[.].{2,3}$', filename) != None) and \
           (re.findall(r'[\?\*]', filename) == [])

def md_table_row(csv_row, is_header_row, delimiter, linebreak):
    """Returns a MD formatted table row, converted from a CSV formatted row.

    A table line will be added after the row in case it is a header row.
    Existing linebreaks will be removed - we want to use the specified linebreak!
    """
    csv_row = csv_row.replace("\n", "").replace("\r", "")
    # Create a line of columns - keep content but replace delimiters
    md_row = "|" + csv_row.replace(delimiter, "|") + "|" + linebreak
    if is_header_row:
        md_row += "|" + "---|" * (csv_row.count(delimiter) + 1) + linebreak
    return md_row

#-------------------------------------------------------------------------------
# MAIN PROGRAM
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    nr_of_arguments = len(sys.argv)
    if nr_of_arguments == 1 or sys.argv[1] == '--help':
        print(extract_program_info())
        sys.exit()
    elif nr_of_arguments != 4:
        print('\nInvalid arguments!\n')
        print(extract_program_info('usage'))
        sys.exit()

    csvfile_path = sys.argv[1]
    mdfile_path = sys.argv[2]
    delimiter = sys.argv[3]

    if (not valid_filename(csvfile_path)) and (csvfile_path.find('.csv') != -1):
        print("Invalid filename: '" + csvfile_path + "'")
        sys.exit()
    if (not valid_filename(mdfile_path)) and (mdfile_path.find('.md') != -1):
        print("Invalid filename: '" + mdfile_path + "'")
        sys.exit()
    if delimiter != ";" and delimiter != ",":
        print("Invalid delimiter! You must use comma or semicolon!")
        sys.exit()

    linebreak = "\n"

    csv_file = FileRead(csvfile_path)
    if csv_file.error() == None:
        is_header_row = True
        md_file = FileWrite(mdfile_path)
        for line in csv_file.lines():
            if md_file.error() != None:
                break
            md_file.write(md_table_row(line, is_header_row, delimiter, linebreak))
            is_header_row = False
        md_file.close()
    csv_file.close()

    if csv_file.error() != None:
        print(csv_file.error())
    if md_file.error() != None:
        print(md_file.error())