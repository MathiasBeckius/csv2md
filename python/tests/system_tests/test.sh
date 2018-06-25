#!/bin/sh
cat test.csv | ../../csv2md.py ';' > new.md
diff old.md new.md
