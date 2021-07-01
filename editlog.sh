#!/bin/bash

filename="smartLog.txt"

# deleting the first 8 lines
#sed -i '1,8d' "$filename"

#accessing the file line by line
while read -r line;do
	echo "$line"	
done < "$filename"

cat "$filename" | tr -s '[:blank:]:' ',' > log1.txt
#cat log1.txt | tr -s ":" "," > log.csv

