#!/bin/sh
APP_NAME="csv2md"
APP_PORT=$1 # perl or python
OPTION=$2

if [ "$APP_PORT" == "perl" ]; then
    FILE_EXTENSION="pl"
elif [ "$APP_PORT" == "python" ]; then
    FILE_EXTENSION="py"
else
    echo "Invalid parameter: $APP_PORT"
    exit
fi

FILENAME="$APP_NAME.$FILE_EXTENSION"
APPLICATION="../$APP_PORT/$FILENAME"

if [ -f "$APPLICATION" ]; then
    echo "Testing $FILENAME..."

    cat test.csv | $APPLICATION ';' > new.md
    if ! cmp -s old.md new.md; then
        echo -e "\nUnexpected difference in output, error when converting CSV -> MD (semi-colon delimiter)"
        if [ "$OPTION" == "-v" ]; then
            diff old.md new.md
        fi
    fi

    cat test.csv | sed 's/;/,/g' | $APPLICATION > new.md
    if ! cmp -s old.md new.md; then
        echo -e "\nUnexpected difference in output, error when converting CSV -> MD (comma delimiter, standard option)"
        if [ "$OPTION" == "-v" ]; then
            diff old.md new.md
        fi
    fi

    cat test.csv | sed 's/;/,/g' | $APPLICATION ',' > new.md
    if ! cmp -s old.md new.md; then
        echo -e "\nUnexpected difference in output, error when converting CSV -> MD (comma delimiter)"
        if [ "$OPTION" == "-v" ]; then
            diff old.md new.md
        fi
    fi

    $APPLICATION --help > help_param.txt
    if ! cmp -s "$APP_PORT/expected_help_param.txt" help_param.txt; then
        echo -e "\nUnexpected difference in output, error when reading help text"
        if [ "$OPTION" == "-v" ]; then
            diff "$APP_PORT/expected_help_param.txt" help_param.txt
        fi
    fi

    $APPLICATION sdf sdf 2> invalid_arg_list.txt
    if ! cmp -s "$APP_PORT/expected_invalid_arg_list.txt" invalid_arg_list.txt; then
        echo -e "\nUnexpected difference in output, error when using invalid argument list"
        if [ "$OPTION" == "-v" ]; then
            diff "$APP_PORT/expected_invalid_arg_list.txt" invalid_arg_list.txt
        fi
    fi

    $APPLICATION '.' 2> invalid_delimiter.txt
    if ! cmp -s expected_invalid_delimiter.txt invalid_delimiter.txt; then
        echo -e "\nUnexpected difference in output, error when specifying invalid delimiter"
        if [ "$OPTION" == "-v" ]; then
            diff expected_invalid_delimiter.txt invalid_delimiter.txt
        fi
    fi
fi