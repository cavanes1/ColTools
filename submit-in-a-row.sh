#!/bin/bash

i=1
 
while [ $i -le 12 ]
do
 cd CALC.c$i.d0.001
 sbatch pscript.sh
 echo submitted positive
 pwd
 sleep 1
 cd ..
 cd CALC.c$i.d-0.001
 sbatch pscript.sh
 echo submitted negative
 pwd
 sleep 1
 cd ..
 ((i++))
done

sleep 1
cd REFPOINT
sbatch pscript.sh
echo submitted reference point
pwd
sleep 1
cd ..

echo work complete
