
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

try:

    with conn.cursor() as cursor:
        # Read a single record
        sql = "Select * from `final_project`.`students`"
        cursor.execute(sql)
        num_of_rows = cursor.rowcount

        for row in cursor:
            print(row)


    with conn.cursor() as cursor:
        # iterate through a all records
        sql = "Select last_name, first_name from `final_project`.`students` where `first_name`=%s"
        cursor.execute(sql, ('Dustin'))
        rows = cursor.fetchall()
        for row in rows:
            print(row)

finally:
    conn.close()