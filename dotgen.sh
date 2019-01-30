#!/usr/bin/env bash
python3 dotgen.py
find . -iname '*.dot' | while read dot
do
	svg=$(echo $dot | sed 's/\.dot$/.svg/')
	dot $dot -Tsvg -o $svg
done