__author__ = 'silvianittel'
__copyright__ = "Copyright 2021, SIE557"
__version__ = "1.0"
__date__ = "03/18/2021"

# Connect to the database

import pymysql.cursors
import db_config_file

try:
    con = pymysql.connect(host=db_config_file.DB_SERVER,
                      user=db_config_file.DB_USER,
                      password=db_config_file.DB_PASS,
                      database=db_config_file.DB, port=db_config_file.DB_PORT)

except (Exception) as error:
    print("Error while fetching data from MYSQL", error)
    exit()
finally:
    print("successfully connected to database")
    con.close()


