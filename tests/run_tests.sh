#!/bin/sh
OPTION=$1

echo "Running tests!"
echo "-------------------------------------------------------------------------"
./test_app.sh perl $OPTION
echo "-------------------------------------------------------------------------"
./test_app.sh python $OPTION
echo "-------------------------------------------------------------------------"
echo "DONE!"