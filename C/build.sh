#!/bin/bash

CFLAGS="-std=c99 -march=native -O3 -pipe"
FILES=*.c

for FILE in $FILES
do
	BINARYNAME="${FILE%.*}"
	gcc $CFLAGS -o $BINARYNAME $FILE core/*.c
done
