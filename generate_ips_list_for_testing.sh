#!/bin/sh

for j in `seq 0 40`
do
    for i in `seq 1 255` ; do echo "127.0.$j.$i" >> ips.txt ; done
done
