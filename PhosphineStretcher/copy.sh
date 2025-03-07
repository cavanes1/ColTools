#!/bin/bash

i=1
 
while [ $i -le 12 ]
do
 cd CALC.c$i.d0.001
 cp ../cisrtin .
 echo copied positive
 pwd
 sleep 2
 cd ..
 cd CALC.c$i.d-0.001
 cp ../cisrtin .
 echo copied negative
 pwd
 sleep 2
 cd ..
 ((i++))
done

sleep 1
cd REFPOINT
cp ../cisrtin .
echo copied reference point
pwd
sleep 1
cd ..

echo work complete
