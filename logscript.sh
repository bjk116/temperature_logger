#!/bin/bash
now="$(date)"
temp=$(cat /sys/class/thermal/thermal_zone0/temp)
temp_f=$(printf '%s\n' "$temp/1000" | bc -l)
echo temp_f $temp_f
printf '%.3fC,%s\n' "$temp_f" "$now" >> /home/projects/temperature_logger/temp.log
Tue Sep 22 13:54:31 UTC 2020
Tue Sep 22 13:55:31 UTC 2020
