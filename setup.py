"""
This setup script will let the user go through the database initialization and
useful resources allocation, eg files for log etc
"""

import sqlite3
import os
import sys
from deployment.IO.configuration import ServerConfiguration

global server

def create_database():
    """
    this function is used to create the database
    :return: None
    """
    global server
    # create the directory
    os.makedirs(server.database.resources_path,
                exist_ok=True)
    # create the database
    connection = sqlite3.connect(server.database.database_name)
    cursor = connection.cursor()
    cursor.execute(server.database.creation_query)
    connection.commit()
    # closing db connection
    connection.close()

    return


# starting the setup script here
if __name__ == "__main__":
    global server
    server = ServerConfiguration()

    # proceedings authorization is required
    authorized = input("This is an installation wizard of a Python simple server for IoT purposes. Proceed? (y/n)\n")
    authorized = authorized.lower()

    if authorized != "y":
        sys.stdout.flush()
        exit()
    else:
        # initializations
        create_database()
        print("[ OK ] setup completed.")
        exit()
