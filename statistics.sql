USE production;
SELECT DISTINCT t_stamp, MIN(degrees)
FROM temperature_log;
