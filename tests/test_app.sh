#!/bin/sh
APP_NAME="csv2md"
APP_PORT="$1" # perl or python
OPTION="$2"

check_output() {
    ACTUAL_OUTPUT="$1"
    EXPECTED_OUTPUT="$2"
    MESSAGE="$3"
    OPTION="$4"
    if ! cmp -s $ACTUAL_OUTPUT $EXPECTED_OUTPUT; then
        echo -e "\nERROR: $MESSAGE"
        if [ "$OPTION" == "-v" ]; then
            diff $ACTUAL_OUTPUT $EXPECTED_OUTPUT
        fi
    fi
}

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

    ACTUAL_OUTPUT=actual_output/new.md
    EXPECTED_OUTPUT=expected_output/old.md
    cat input/test.csv | $APPLICATION ';' > $ACTUAL_OUTPUT
    check_output $ACTUAL_OUTPUT $EXPECTED_OUTPUT "conversion, semi-colon delimiter" $OPTION

    ACTUAL_OUTPUT=actual_output/new.md
    EXPECTED_OUTPUT=expected_output/old.md
    cat input/test.csv | sed 's/;/,/g' | $APPLICATION > $ACTUAL_OUTPUT
    check_output $ACTUAL_OUTPUT $EXPECTED_OUTPUT "conversion, comma delimiter (standard option)" $OPTION

    ACTUAL_OUTPUT=actual_output/new.md
    EXPECTED_OUTPUT=expected_output/old.md
    cat input/test.csv | sed 's/;/,/g' | $APPLICATION ',' > $ACTUAL_OUTPUT
    check_output $ACTUAL_OUTPUT $EXPECTED_OUTPUT "conversion, comma delimiter" $OPTION

    ACTUAL_OUTPUT=actual_output/help_param.txt
    EXPECTED_OUTPUT="expected_output/$APP_PORT/expected_help_param.txt"
    $APPLICATION --help > $ACTUAL_OUTPUT
    check_output $ACTUAL_OUTPUT $EXPECTED_OUTPUT "request help text" $OPTION

    ACTUAL_OUTPUT=actual_output/invalid_arg_list.txt
    EXPECTED_OUTPUT="expected_output/$APP_PORT/expected_invalid_arg_list.txt"
    $APPLICATION sdf sdf 2> $ACTUAL_OUTPUT
    check_output $ACTUAL_OUTPUT $EXPECTED_OUTPUT "invalid argument list" $OPTION

    ACTUAL_OUTPUT=actual_output/invalid_delimiter.txt
    EXPECTED_OUTPUT=expected_output/expected_invalid_delimiter.txt
    $APPLICATION '.' 2> $ACTUAL_OUTPUT
    check_output $ACTUAL_OUTPUT $EXPECTED_OUTPUT "invalid delimiter" $OPTION

    ACTUAL_OUTPUT=actual_output/nonprintable.txt
    EXPECTED_OUTPUT=expected_output/expected_nonprintable.txt
    cat input/toxic.png | $APPLICATION &> $ACTUAL_OUTPUT
    check_output $ACTUAL_OUTPUT $EXPECTED_OUTPUT "non-printable characters" $OPTION
fi