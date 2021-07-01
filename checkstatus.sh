#!/bin/sh

sudo nvme smart-log /dev/nvme0 -H > smartLog.txt

#delete first 8 lines
sed -i '1,8d' smartLog.txt

