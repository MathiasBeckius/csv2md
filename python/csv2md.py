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
    nr_of_arguments = len(sys.argv)
    if nr_of_arguments == 1: # No arguments?
        # Normal case
        delimiter = ','
    elif nr_of_arguments == 2: # Single argument?
        argument = sys.argv[1]
        if argument.lower() == '--help':
            print(program_info())
            sys.exit()
        else:
            # Assume it is delimiter
            delimiter = argument
            if delimiter != ';' and delimiter != ',':
                print('Invalid delimiter! You must use comma or semicolon!')
                sys.exit()
    else: #  More than one argument...
        print('Invalid arguments list!\n')
        print(program_info())
        sys.exit()
    
    is_header_row = True
    for line in sys.stdin:
        line = line.replace('\r', '').replace('\n', '')
        print('|' + line.replace(delimiter, '|') + '|')
        if is_header_row:
            print('|' + '---|' * (line.count(delimiter) + 1))
        is_header_row = False