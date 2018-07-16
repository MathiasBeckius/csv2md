#!/usr/bin/env python

import unittest
import sys
sys.path.append('../../../application/python/')

from csv2md import CSVToMarkdown

class TestTokenize(unittest.TestCase):
    def test_tokenize_EmptyString(self):
        tokens, unfinished_quote = CSVToMarkdown._tokenize('', ',')
        self.assertEqual([], tokens)
        self.assertFalse(unfinished_quote)

    def test_tokenize_SimpleString1(self):
        tokens, unfinished_quote = CSVToMarkdown._tokenize('1', ',')
        expected_tokens = ['1']
        self.assertEqual(tokens, expected_tokens)
        self.assertFalse(unfinished_quote)

    def test_tokenize_SimpleString2(self):
        tokens, unfinished_quote = CSVToMarkdown._tokenize('1,2,3', ',')
        expected_tokens = ['1', '2', '3']
        self.assertEqual(tokens, expected_tokens)
        self.assertFalse(unfinished_quote)

    def test_tokenize_SimpleString3(self):
        tokens, unfinished_quote = CSVToMarkdown._tokenize(' 1,"2",3 ', ',')
        expected_tokens = [' 1', '"2"', '3 ']
        self.assertEqual(tokens, expected_tokens)
        self.assertFalse(unfinished_quote)

    def test_tokenize_SimpleString4(self):
        tokens, unfinished_quote = CSVToMarkdown._tokenize('1,2,3,', ',')
        expected_tokens = ['1', '2', '3', '']
        self.assertEqual(tokens, expected_tokens)
        self.assertFalse(unfinished_quote)

    def test_tokenize_StringWithQuote(self):
        tokens, unfinished_quote = CSVToMarkdown._tokenize('1,2,3,""', ',')
        expected_tokens = ['1', '2', '3', '""']
        self.assertEqual(tokens, expected_tokens)
        self.assertFalse(unfinished_quote)
        
    def test_tokenize_StringWithUnfinishedQuote1(self):
        tokens, unfinished_quote = CSVToMarkdown._tokenize('"1,2,3', ',')
        expected_tokens = ['"1,2,3']
        self.assertEqual(tokens, expected_tokens)
        self.assertTrue(unfinished_quote)

    def test_tokenize_StringWithUnfinishedQuote2(self):
        tokens, unfinished_quote = CSVToMarkdown._tokenize('1,2,"3', ',')
        expected_tokens = ['1', '2', '"3']
        self.assertEqual(tokens, expected_tokens)
        self.assertTrue(unfinished_quote)

    def test_tokenize_StringWithUnfinishedQuote3(self):
        tokens, unfinished_quote = CSVToMarkdown._tokenize('"1', ',')
        expected_tokens = ['"1']
        self.assertEqual(tokens, expected_tokens)
        self.assertTrue(unfinished_quote)

    def test_tokenize_StringWithQuoteSpreadOverLines1(self):
        tokens, unfinished_quote = CSVToMarkdown._tokenize('"1', ',')
        expected_tokens1 = ['"1']
        self.assertEqual(tokens, expected_tokens1)
        self.assertTrue(unfinished_quote)

        tokens, unfinished_quote = CSVToMarkdown._tokenize('2",3', ',', unfinished_quote=unfinished_quote)
        expected_tokens2 = ['2"', '3']
        self.assertEqual(tokens, expected_tokens2)
        self.assertFalse(unfinished_quote)

    def test_tokenize_StringWithQuoteSpreadOverLines2(self):
        tokens, unfinished_quote = CSVToMarkdown._tokenize('"1', ',')
        expected_tokens1 = ['"1']
        self.assertEqual(tokens, expected_tokens1)
        self.assertTrue(unfinished_quote)
        
        tokens, unfinished_quote = CSVToMarkdown._tokenize('2', ',', unfinished_quote=unfinished_quote)
        expected_tokens2 = ['2']
        self.assertEqual(tokens, expected_tokens2)
        self.assertTrue(unfinished_quote)
        
        tokens, unfinished_quote = CSVToMarkdown._tokenize('3"', ',', unfinished_quote=unfinished_quote)
        expected_tokens3 = ['3"']
        self.assertEqual(tokens, expected_tokens3)
        self.assertFalse(unfinished_quote)

    def test_tokenize_StringWithQuoteSpreadOverLines3(self):
        tokens, unfinished_quote = CSVToMarkdown._tokenize('0,"1', ',')
        expected_tokens1 = ['0','"1']
        self.assertEqual(tokens, expected_tokens1)
        self.assertTrue(unfinished_quote)
        
        tokens, unfinished_quote = CSVToMarkdown._tokenize('2,3,4', ',', unfinished_quote=unfinished_quote)
        expected_tokens2 = ['2,3,4']
        self.assertEqual(tokens, expected_tokens2)
        self.assertTrue(unfinished_quote)
        
        tokens, unfinished_quote = CSVToMarkdown._tokenize('5"', ',', unfinished_quote=unfinished_quote)
        expected_tokens3 = ['5"']
        self.assertEqual(tokens, expected_tokens3)
        self.assertFalse(unfinished_quote)

    def test_tokenize_StringWithQuoteSpreadOverLines4(self):
        unfinished_quote = False
        expected_tokens = ['"foobar.h']
        tokens, unfinished_quote = CSVToMarkdown._tokenize('"foobar.h', ',', unfinished_quote=unfinished_quote)
        self.assertEqual(tokens, expected_tokens)
        self.assertTrue(unfinished_quote)

        expected_tokens = ['foobar.c"','1','0','"test_foobar.c"','85.00%','0','"Test coverage can be improved, but is good enough for now!"']
        tokens, unfinished_quote = CSVToMarkdown._tokenize('foobar.c",1,0,"test_foobar.c",85.00%,0,"Test coverage can be improved, but is good enough for now!"', ',', unfinished_quote)
        self.assertEqual(tokens, expected_tokens)
        self.assertFalse(unfinished_quote)

    def test_tokenize_StringWithQuoteContainingDelimiter(self):
        tokens, unfinished_quote = CSVToMarkdown._tokenize('1,2,"3,4",5', ',')
        expected_tokens = ['1', '2', '"3,4"', '5']
        self.assertEqual(tokens, expected_tokens)
        self.assertFalse(unfinished_quote)
    
if __name__ == '__main__':
    unittest.main()