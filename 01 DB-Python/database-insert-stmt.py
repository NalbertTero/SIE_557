__author__ = 'silvianittel'
__copyright__ = "Copyright 2021, SIE557"
__version__ = "1.0"
__date__ = "03/18/2021"

import pymysql.cursors
import db_config_file

# Connect to the database
try:
    conn = pymysql.connect(host=db_config_file.DB_SERVER,
                      user=db_config_file.DB_USER,
                      password=db_config_file.DB_PASS,
                      database=db_config_file.DB, port=db_config_file.DB_PORT)

except (Exception) as error:
    print("Error while connecting to MYSQL", error)
    exit()

print("successfully connected to database")
# create insert statement

try:
    with conn.cursor() as cursor:
        # Create a new record as a test example
        sql = "INSERT INTO `final_project`.`students` (`last_name`, `first_name`, `grade`) VALUES (%s, %s, %s)"
        cursor.execute(sql, ('Wheeler', 'Mike', '8'))
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        conn.commit()
        print("Successfully inserted record")

except (Exception) as error:
    print("Error while inserting data to MYSQL", error)
    exit()


finally:
    cursor.close()
    conn.close()


