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

def convert_timezone(dt, tz):
    """
    Found this on stack overflow.  Necessary currently because our pi thinks
    its in UTC.  I'm leaving it in as it's decent real world practice for manipulating
    data that isn't tidy/the format you want.
    Args:
        dt: datetime string
        tz: desired timezone
    Returns:
        dt: datetime object
    """
    dt = date_parse(dt)
    tz = pytz.timezone(tz)
    dt = dt.astimezone(tz)
    return dt

def get_db_connection():
    """
    Included in this script for learnings sake
    Args:
        None, stuff is hard coded for ease of use
    Returns:
        cnx, connection object to local mysql db.
    """
    cnx = mysql.connector.connect(user="app", password="pass",
                                  host="localhost",
                                  database="production")
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
    try:
        cursor.execute(query)
        cnx.commit()
        return True
    except Exception as e:
        print("issue inserting")
        print(str(e))

def analyze_full_file(file_path='//home//projects//temperature_logger'):
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
                t_stamp = convert_timezone(t_stamp, 'EST')
                cursor = cnx.cursor()
                insert_temperature_record(temperature, t_stamp, cursor, cnx)
                recordsInserted += 1
    except Exception as e:
        print("Error with analyze full file")
    finally:
        cnx.close()
    end = timer()
    print("inserted %i records in %s seconds"%(recordsInserted, str(end-start)))

if __name__ == '__main__':
    analyze_full_file()