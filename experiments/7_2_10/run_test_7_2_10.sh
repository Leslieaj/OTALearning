#!/bin/sh

rm -rf result/
mkdir result
for i in $(seq 1 10)
do
python3 ../../learn_for_test.py 7_2_10-$i.json
done
