#!/usr/bin/env python

import unittest
import sys
sys.path.append('../../../application/python/')

from csv2md import CSVToMarkdown

class TestTokenizeHelpers(unittest.TestCase):
    def test_line_to_split_EmptyString(self):
        line, remaining_line = CSVToMarkdown._line_to_split('', ',')
        self.assertEqual('', line)
        self.assertEqual('', remaining_line)

    def test_line_to_split_NoQuote(self):
        line = '1,2,3'
        line, remaining_line = CSVToMarkdown._line_to_split(line, ',')
        self.assertEqual('1,2,3', line)
        self.assertEqual('', remaining_line)
    
    def test_line_to_split_WithQuote(self):
        line = '1,2,"3,4", 5'
        line, remaining_line = CSVToMarkdown._line_to_split(line, ',')
        self.assertEqual('1,2', line)
        self.assertEqual('"3,4", 5', remaining_line)

    def test_extract_quote(self):
        line = '"3,4", 5'
        quote, unfinished_quote, remaining_line = CSVToMarkdown._extract_quote(line, False)
        self.assertEqual('"3,4"', quote)
        self.assertFalse(unfinished_quote)
        self.assertEqual(', 5', remaining_line)

if __name__ == '__main__':
    unittest.main()