#!/bin/sh
APP_NAME="csv2md"
APP_PORT=$1 # perl or python

if [ "$APP_PORT" == "perl" ]; then
    FILE_EXTENSION="pl"
elif [ "$APP_PORT" == "python" ]; then
    FILE_EXTENSION="py"
else
    echo "Invalid parameter: $APP_PORT"
    exit
fi

APPLICATION="../$APP_PORT/$APP_NAME.$FILE_EXTENSION"

if [ -f "$APPLICATION" ]; then
    echo "Testing $APPLICATION..."
    cat test.csv | $APPLICATION ';' > new.md
    diff old.md new.md
    cat test.csv | sed 's/;/,/g' | $APPLICATION > new.md
    diff old.md new.md
    cat test.csv | sed 's/;/,/g' | $APPLICATION ',' > new.md
    diff old.md new.md
    $APPLICATION --help > help_param.txt
    diff "$APP_PORT/expected_help_param.txt" help_param.txt
    $APPLICATION sdf sdf 2> invalid_arg_list.txt
    diff "$APP_PORT/expected_invalid_arg_list.txt" invalid_arg_list.txt
    $APPLICATION '.' 2> invalid_delimiter.txt
    diff expected_invalid_delimiter.txt invalid_delimiter.txt
fi