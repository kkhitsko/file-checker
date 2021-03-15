#!/bin/bash

file=$1
trunc_lines=$2

cmd=$(tail -n +$trunc_lines $file)
echo "$cmd" > $file
minimumsize=5
actualsize=$(du -b "$file" | cut -f 1)
if [ ! $actualsize -ge $minimumsize ]; then
    rm $file
fi
