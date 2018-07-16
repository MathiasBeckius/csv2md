#!/bin/sh

OPTION="$1"

if [ "$OPTION" != "-v" ]; then
    OPTION="-q"
fi

find ./test_*.py -type f | sed "s#.*\/##g" | while read FILE; do
    echo "Testing $FILE"
    python $FILE $OPTION
    echo ""
done