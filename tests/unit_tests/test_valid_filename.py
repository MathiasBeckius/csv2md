#!/usr/bin/env python

import unittest
import sys
sys.path.append('../../')

from csv2md import valid_filename

class TestValidFilename(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_valid_filename_ValidFilename(self):
        self.assertTrue(valid_filename('a.md'))
        self.assertTrue(valid_filename('a.csv'))
        self.assertTrue(valid_filename('table.csv'))
        self.assertTrue(valid_filename('../../table.csv'))
        self.assertTrue(valid_filename('c:\tables\table.csv'))

    def test_valid_filename_InvalidFilename(self):
        self.assertFalse(valid_filename('a.x'))
        self.assertFalse(valid_filename('a.html'))
        self.assertFalse(valid_filename('.csv'))
        self.assertFalse(valid_filename('csv'))
        self.assertFalse(valid_filename('tablecsv'))
        self.assertFalse(valid_filename('tabl?e.csv'))
        self.assertFalse(valid_filename('../../tab*le.csv'))

if __name__ == '__main__':
    unittest.main()