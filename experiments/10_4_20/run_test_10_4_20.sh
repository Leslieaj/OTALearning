#!/bin/sh

rm -rf result/
mkdir result
for i in $(seq 1 10)
do
python3 ../../learn_for_test.py 10_4_20-$i.json
done
