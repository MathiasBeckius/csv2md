#!/usr/bin/env python

import unittest
import sys
sys.path.append('../../../application/python/')

from csv2md import CSVToMarkdown

class TestParse(unittest.TestCase):
    def setUp(self):
        self.converter = CSVToMarkdown(',', None)

    def tearDown(self):
        del self.converter

    def test_parse_SimpleLine1(self):
        tokens = self.converter._parse('1,2,3')
        self.assertEqual(['1', '2', '3'], tokens)

    def test_parse_SimpleLine2(self):
        tokens = self.converter._parse(' 1, "2" ,3 ')
        self.assertEqual([' 1', '"2"', '3 '], tokens)
    """
    def test_parse_SimpleLine3(self):
        tokens = self.converter._parse('"alarm.h')
        self.assertEqual(None, tokens)
        tokens = self.converter._parse('alarm.c",1,0,"test_alarm.c",,74.82%,0,"Test coverage has been improved, but refactoring of Alarm is advised."')
        #tokens = self.converter._parse('alarm.c",1,0,"test_alarm.c",,74.82%,0,"Test coverage has been improved, but refactoring of Alarm is advised."')
    """
    def test_parse_SimpleLineFollowedByNewLine(self):
        tokens = self.converter._parse('1,2,3')
        self.assertEqual(['1', '2', '3'], tokens)
        # Here comes the new line
        tokens = self.converter._parse('4,5,6')
        self.assertEqual(['4', '5', '6'], tokens)

    def test_parse_QuoteOverTwoLines1(self):
        tokens = self.converter._parse('1,2,"3,')
        self.assertEqual(None, tokens)
        tokens = self.converter._parse('4",5')
        self.assertEqual(['1', '2', '"3,<br>4"', '5'], tokens)

    def test_parse_QuoteOverTwoLines2(self):
        tokens = self.converter._parse('1,2,"3')
        self.assertEqual(None, tokens)
        tokens = self.converter._parse('4"')
        self.assertEqual(['1', '2', '"3<br>4"'], tokens)

    def test_parse_QuoteOverTwoLinesFollowedByNewLine(self):
        tokens = self.converter._parse('1,2,"3,')
        self.assertEqual(None, tokens)
        tokens = self.converter._parse('4",5')
        self.assertEqual(['1', '2', '"3,<br>4"', '5'], tokens)
        # Here comes the new line
        tokens = self.converter._parse('4,5,6')
        self.assertEqual(['4', '5', '6'], tokens)

    def test_parse_QuoteOverThreeLines(self):
        tokens = self.converter._parse('1,2,"3,')
        self.assertEqual(None, tokens)
        tokens = self.converter._parse('4')
        self.assertEqual(None, tokens)
        tokens = self.converter._parse(',5,6",7')
        self.assertEqual(['1', '2', '"3,<br>4<br>,5,6"', '7'], tokens)

    def test_parse_QuoteOverThreeLinesFollowedByNewLine(self):
        tokens = self.converter._parse('1,2,"3,')
        self.assertEqual(None, tokens)
        tokens = self.converter._parse('4')
        self.assertEqual(None, tokens)
        tokens = self.converter._parse(',5,6",7')
        self.assertEqual(['1', '2', '"3,<br>4<br>,5,6"', '7'], tokens)
        # Here comes the new line
        tokens = self.converter._parse('1,2,3')
        self.assertEqual(['1', '2', '3'], tokens)

if __name__ == '__main__':
    unittest.main()