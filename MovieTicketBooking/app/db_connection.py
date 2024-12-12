import mysql.connector


def connect_to_db():

    conncection = mysql.connector.connect(
        host="127.0.0.1", user="root", password="", database="movie_booking"
    )

    cursor = conncection.cursor(dictionary=True)
    return conncection, cursor


def close_connection(connection, cursor):
    cursor.close()
    connection.close()
