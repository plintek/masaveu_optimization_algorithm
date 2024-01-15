import psycopg2
import os
import psycopg2.extras


def get_database_cursor():

    conn = psycopg2.connect(
        host="localhost",
        database="dotgis_ctc",
        user="postgres",
        password="DOTGIS_2020",
        port="3232",
    )
    conn.set_client_encoding('UTF8')
    return conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
