#!/bin/sh

mkdir result
for i in $(seq 1 20)
do
python3 ../../learn_for_test.py 7_4_20-$i.json
done
