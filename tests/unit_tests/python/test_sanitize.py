#!/usr/bin/env python

import unittest
import sys
sys.path.append('../../../application/python/')

from csv2md import CSVToMarkdown

class TestSanitize(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sanitize_RemoveWhitespace(self):
        expected_output = ['1', '2', '3']
        output = CSVToMarkdown._sanitize([' 1', ' 2 ', '3 '])
        self.assertEqual(expected_output, output)

    def test_sanitize_RemoveQuotationMarks(self):
        expected_output = ['1', '2', '3']
        output = CSVToMarkdown._sanitize(['"1', '"2"', '3"'])
        self.assertEqual(expected_output, output)

    def test_sanitize_RemoveWhitespaceAndQuotationMarks1(self):
        expected_output = ['1', '2', '3']
        output = CSVToMarkdown._sanitize([' "1 ', ' "2" ', ' 3" '])
        self.assertEqual(expected_output, output)

    def test_sanitize_RemoveWhitespaceAndQuotationMarks2(self):
        expected_output = ['1', '2', '3']
        output = CSVToMarkdown._sanitize([' "1 ', ' "2" ', ' 3" '])
        self.assertEqual(expected_output, output)

    def test_sanitize_DoNotRemoveWhitespaceWithinQuotationMarks(self):
        expected_output = [' 1', ' 2 ', '3 ']
        output = CSVToMarkdown._sanitize([' " 1" ', ' " 2 " ', ' "3 " '])
        self.assertEqual(expected_output, output)

if __name__ == '__main__':
    unittest.main()