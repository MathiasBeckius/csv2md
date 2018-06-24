#!/bin/sh
../../csv2md.py test.csv new.md ';'
diff old.md new.md
