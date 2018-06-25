#!/bin/sh
APPLICATION=../csv2md.py

cat test.csv | $APPLICATION ';' > new.md
diff old.md new.md

cat test.csv | sed 's/;/,/g' | $APPLICATION > new.md
diff old.md new.md

cat test.csv | sed 's/;/,/g' | $APPLICATION ',' > new.md
diff old.md new.md

$APPLICATION --help > help_param.txt
diff expected_help_param.txt help_param.txt

$APPLICATION sdf sdf > invalid_arg_list.txt
diff expected_invalid_arg_list.txt invalid_arg_list.txt

$APPLICATION '.' > invalid_delimiter.txt
diff expected_invalid_delimiter.txt invalid_delimiter.txt