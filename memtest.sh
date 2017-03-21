#!/bin/bash

for i in {100..3000..100}
do
    number=$i
    echo "i is now $i of 3000"
    sed -i "s/validation[[:digit:]][[:digit:]]*/validation$number/g" test_backup.py
    sed -i "s/samples = [[:digit:]][[:digit:]]*/samples = $number/g" test_backup.py
    mprof run test_backup.py
done 

