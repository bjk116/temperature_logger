My first project!  Here's what was accomplished and done.

Goal:  Log the temperatue of the raspberry pi every minute

How:
1)  Write a .sh file that gets the temperature and the date and
writes them to a file
    this is the file logscript.sh in this directory
    and add permissions so its executable with
    sudo chmod +x logscript.sh
2)  Create a temp.log file with sudo nano temp.log, save it
and then allow the permissions so that it can be written to using
sudo chmod ugo+w temp.log
3)  Add the cronjob with 
sudo crontab -e (to edit the current crontab list) and add
* * * * * /home/projects/temperature_logger/logscript.sh
* * * * * sleep 30; /home/projects/temperature_logger/logscript.sh
This sets it to run every 30 seconds
