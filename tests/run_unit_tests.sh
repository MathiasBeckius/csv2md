#!/bin/sh
OPTION=$1

echo "Running unit tests!"
echo "-------------------------------------------------------------------------"
#./test_app.sh perl $OPTION
#echo "-------------------------------------------------------------------------"
cd unit_tests/python
./run_unit_tests.sh $OPTION
echo "-------------------------------------------------------------------------"
echo "DONE!"