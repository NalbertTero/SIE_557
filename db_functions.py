# === some database commands ======

import pymysql
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
        return con

    except pymysql.InternalError as e:
        print(e)
        raise DatabaseError(e)
    except pymysql.OperationalError as e:
        print(e)
        raise DatabaseError(e)
    except pymysql.NotSupportedError as e:
        print(e)
        raise DatabaseError(e)


def query_database(con, sql, values):
    try:
        cursor = con.cursor()
        cursor.execute(sql, values)
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
        con.close()
        return num_of_rows, rows