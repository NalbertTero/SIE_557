import pymysql
from tkinter import messagebox
import GM_db_functions
import db_config_file

class DatabaseError(Exception):
    def __init__(self, e):
        super().__init__(e)


def open_database():
    try:
        con = pymysql.connect(host=db_config_file.DB_SERVER,
                              user=db_config_file.DB_USER,
                              password=db_config_file.DB_PASS,
                              database=db_config_file.DB,
                              port=db_config_file.DB_PORT)
        status = 1
        return status, con

    except pymysql.InternalError as e:
        status = 0
        return status, e
    except pymysql.OperationalError as e:
        status = 0
        return status, e
    except pymysql.NotSupportedError as e:
        status = 0
        return status, e


def query_database(con, sql):
    try:
        cursor = con.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        num_of_rows = cursor.rowcount

    except pymysql.InternalError as e:
        print(e)
        raise DatabaseError(e)
    except pymysql.OperationalError as e:
        print(e)
        raise DatabaseError(e)
    except pymysql.ProgrammingError as e:
        print(e)
        raise DatabaseError(e)
    except pymysql.DataError as e:
        print(e)
        raise DatabaseError(e)
    except pymysql.IntegrityError as e:
        print(e)
        raise DatabaseError(e)
    except pymysql.NotSupportedError as e:
        print(e)
        raise DatabaseError(e)
    finally:
        cursor.close()
        #con.close()
        return num_of_rows, rows

def load_database_results(con, sql):
    global rows
    global num_rows

    try:
        num_rows, rows = GM_db_functions.query_database(con, sql)
    except DatabaseError:
        messagebox.showinfo("Error querying the database.")

    return num_rows, rows

def insertIntoDatabase(con, sql):

    try:
        cursor = con.cursor()
        cursor.execute(sql)

    except DatabaseError:
        messagebox.showinfo("Error adding entry to the database.")

