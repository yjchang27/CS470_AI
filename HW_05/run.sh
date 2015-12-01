#!/bin/bash
hsizes=( 80 85 )
lrates=( 1.14 1.15 )

for i in "${hsizes[@]}"
do
    for j in "${lrates[@]}"
    do
        echo $i, $j
        python mnist.py $i $j
    done
done
