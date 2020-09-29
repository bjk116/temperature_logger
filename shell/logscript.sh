#!/bin/bash
now="$(date)"
# cat /sys/../temp is how you get the current temp of the raspberry pi
# on ubuntu
temp=$(cat /sys/class/thermal/thermal_zone0/temp)
temp_f=$(printf '%s\n' "$temp/1000" | bc -l)
printf '%.3fC,%s\n' "$temp_f" "$now" >> /home/ubuntu/temperature_logger/logs/temp.log
