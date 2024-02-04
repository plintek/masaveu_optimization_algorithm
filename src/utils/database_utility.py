""" This module contains the utility functions for the database. """
import psycopg2
import psycopg2.extras


def get_database_cursor():
    """
    Connects to the PostgreSQL database and returns a cursor object.

    Returns:
        tuple: A tuple containing the connection object and the cursor object.
    """
    conn = psycopg2.connect(
        host="localhost",
        database="dotgis_ctc",
        user="postgres",
        password="DOTGIS_2020",
        port="3232",
    )
    conn.set_client_encoding('UTF8')
    return conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
