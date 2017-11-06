#!/bin/bash

h=$1
m=$2

now=$(date +%s)
then=$(date -d "$h:$m" +%s)
if [ $then -lt $now ]; then
	then=$(date -d "$h:$m tomorrow" +%s)
fi

exec >/dev/ttyUSB0

echo warming >&2
echo 0
sleep 3
echo up >&2
echo 1
sleep 4
echo --- >&2
echo 0
sleep 2
echo good night >&2
echo 1
sleep 4
echo 0

stepdelay=4

then2=$((then-128*stepdelay*2))  # light up a bit earlier
echo "Sleeping until $(date -d "1970-01-01 $then2 seconds") +-TZ..." >&2

echo "$((then2-now))" >&2
sleep $((then2-now))
date >&2
echo "Good morning!" >&2

for i in `seq 1 10`; do
	echo $i >&2
	echo $i
	sleep $((stepdelay*4))
done
for i in `seq 11 30`; do
	echo $i >&2
	echo $i
	sleep $((stepdelay*3))
done
for i in `seq 31 70`; do
	echo $i >&2
	echo $i
	sleep $((stepdelay*2))
done
for i in `seq 71 192`; do
	echo "$i" >&2
	echo "$i"
	sleep $stepdelay
done

date >&2
echo "There." >&2

sleep 3600

date >&2
echo "Safety shutdown." >&2

echo 0
sleep 5
