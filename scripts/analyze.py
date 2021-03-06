#!/usr/bin/python3
"""
For analyzing the data from temp.log
and then logging that.

Using python 3.8
"""
import os
import datetime
import pytz
from dateutil.parser import parse as date_parse
import mysql.connector
from timeit import default_timer as timer
import logging
import sys

log_file = os.path.abspath('../logs/scripts.log')
temperature_file_directory = os.path.abspath('../logs')
logging.basicConfig(filename='../logs/scripts.log', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M%S %p')
logger = logging.getLogger(__name__)
logger.warning("should see this in file")
print(logger.handlers)

def parse_date(t_stamp):
    """
    For parsing date,s eventualy to be put into it's own date module.
    Args:
        dt: datetime string
    Returns:
        dt: datetime object
    """
    dt = date_parse(t_stamp)
#    tz = pytz.timezone(tz)
#    dt = dt.astimezone(tz)
    db_date =  dt.strftime('%Y-%m-%d %H-%M-%S')
#    print(f"db date is {db_date}")
    return db_date

def get_db_connection():
    """
    Included in this script for learnings sake
    Args:
        None, stuff is hard coded for ease of use
    Returns:
        cnx, connection object to local mysql db.
    """
    cnx = mysql.connector.connect(user="ubuntu", password="Normie419",
                                  host="localhost",
                                  database="ubuntu")
    return cnx

def insert_temperature_record(temperature, t_stamp, cursor, cnx):
    """
    For inserting the record into the database.
    Args:
        temperature: float, the temperature in celsius
        t_stamp: datetime.datetime object
        cursor: cnx.cursor() object, for writing to db
        cnx: mysql-connector connection object
    Returns:
        bool: True if successful insert
              False if an error occured
    """
    query = f"INSERT INTO temperature_log (degrees, t_stamp)  VALUES({temperature}, '{t_stamp}')"
 #   print(f"{query}")
    try:
        cursor.execute(query)
        cnx.commit()
        return True
    except Exception as e:
        return False

def analyze_full_file(file_path=temperature_file_directory):
    """
    Scans in the entirety of the temp.log file, figures out the
    unique dates, gets the max, min, and average temperature, and
    then writes that to a file.
    Args:
        file_path: string, path to temp file.
    """
    cnx = get_db_connection()
    recordsInserted = 0
    duplicateAttempted = 0
    logMsg = ''
    start = timer()
    try:
        with open(os.path.join(file_path, 'temp.log'), "r") as temperature_log_file:
            for line in temperature_log_file:
                stripped_line = line.strip()
                temperature, t_stamp = tuple(stripped_line.split(','))
                temperature = temperature.split('C')[0]
                t_stamp = parse_date(t_stamp)
                cursor = cnx.cursor()
                successful_insert = insert_temperature_record(temperature, t_stamp, cursor, cnx)
                if successful_insert:
                    recordsInserted += 1
                else:
                    duplicateAttempted += 1
        logger.info(f"{recordsInserted} records inserted")
        logger.info(f"{duplicateAttempted} records already exist")
    except Exception as e:
        logger.exception("Error with analyze full file")
    finally:
        cnx.close()
    end = timer()
    logger.info("inserted %i records in %s seconds"%(recordsInserted, str(end-start)))

if __name__ == '__main__':
     logger.info("I've been called")
     logger.info("Number of arguments: %i"%(len(sys.argv)))
     logger.info("Arguments: " + str(sys.argv))
     logging.info("Calling one shot analyze full file from the command line")
     analyze_full_file()
     logging.info("Finished")
