#!/usr/bin/env python

import unittest
import sys
sys.path.append('../../../application/python/')

from csv2md import CSVToMarkdown

class TestConvert(unittest.TestCase):
    def setUp(self):
        self.converter = CSVToMarkdown(',', None)

    def tearDown(self):
        del self.converter

    def test_convert_BlankLine(self):
        converted_line = self.converter.convert('')
        self.assertEqual(None, converted_line)

    def test_convert_HeaderRow(self):
        line = 'Column 1,Column 2,Column 3'
        expected_line = '|Column 1|Column 2|Column 3|\n' + \
                        '|---|---|---|'
        converted_line = self.converter.convert(line)
        self.assertEqual(expected_line, converted_line)

    def test_convert_SimpleLine1(self):
        converted_line = self.converter.convert('Column 1,Column 2,Column 3')
        # After header row, insert line
        line = '1,2,3'
        converted_line = self.converter.convert(line)
        self.assertEqual('|1|2|3|', converted_line)

    def test_convert_SimpleLine2(self):
        converted_line = self.converter.convert('Column 1,Column 2,Column 3')
        # After header row, insert line
        line = '1,"2",3'
        converted_line = self.converter.convert(line)
        self.assertEqual('|1|2|3|', converted_line)

    def test_convert_SimpleLineButSanitizedLine(self):
        converted_line = self.converter.convert('Column 1,Column 2,Column 3')
        # After header row, insert line
        line = ' 1, "2" ,3 '
        converted_line = self.converter.convert(line)
        self.assertEqual('|1|2|3|', converted_line)

    def test_convert_QuoteOverTwoLines(self):
        converted_line = self.converter.convert('Column 1,Column 2,Column 3')
        # After header row, insert line
        line = '"1'
        converted_line = self.converter.convert(line)
        self.assertEqual(None, converted_line)
        line = '2"'
        converted_line = self.converter.convert(line)
        self.assertEqual('|1<br>2|', converted_line)
    """
    def test_convert_QuoteOverTwoLines2(self):
        tokens = self.converter._parse('1,2,"3')
        self.assertEqual(None, tokens)
        tokens = self.converter._parse('4"')
        self.assertEqual(['1', '2', '"34"'], tokens)

    def test_convert_QuoteOverTwoLinesFollowedByNewLine(self):
        tokens = self.converter._parse('1,2,"3,')
        self.assertEqual(None, tokens)
        tokens = self.converter._parse('4",5')
        self.assertEqual(['1', '2', '"3,4"', '5'], tokens)
        # Here comes the new line
        tokens = self.converter._parse('4,5,6')
        self.assertEqual(['4', '5', '6'], tokens)

    def test_convert_QuoteOverThreeLines(self):
        tokens = self.converter._parse('1,2,"3,')
        self.assertEqual(None, tokens)
        tokens = self.converter._parse('4')
        self.assertEqual(None, tokens)
        tokens = self.converter._parse(',5,6",7')
        self.assertEqual(['1', '2', '"3,4,5,6"', '7'], tokens)

    def test_convert_QuoteOverThreeLinesFollowedByNewLine(self):
        tokens = self.converter._parse('1,2,"3,')
        self.assertEqual(None, tokens)
        tokens = self.converter._parse('4')
        self.assertEqual(None, tokens)
        tokens = self.converter._parse(',5,6",7')
        self.assertEqual(['1', '2', '"3,4,5,6"', '7'], tokens)
        # Here comes the new line
        tokens = self.converter._parse('1,2,3')
        self.assertEqual(['1', '2', '3'], tokens)
    """
if __name__ == '__main__':
    unittest.main()