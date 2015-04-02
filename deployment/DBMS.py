import sqlite3

class TemperatureDatabase():
    """
    wrapper class to sqlite operations in order to store and retrieve temperature
    data from the sensor connected to the Raspberry Pi
    """

    def __init__(self, db_path, temp_table):
        """
        this is the class constructor
        :param db_path: string, the path which identifies the resources of the db
        :param temp_table: string, the table name used to store temperatures data
        :return: None
        """
        self.database = db_path
        self.table = temp_table


    def insert_values(self, values):
        """
        this is the function the user can use to perform an insertion query
        :param values: list of tuples, the list of the values to be inserted
        :return: None
        """
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()

        query = "INSERT INTO " + self.table + " (id, temperature, measuretime) VALUES (?,?,?)"
        cursor.executemany(query, values)

        cursor.close()
        connection.commit()
        connection.close()


    def retrieve_values(self, id):
        """
        this function will be used to retrieve the specified values at the row's id
        :param id:integer, the id currently used by the main server function to access the db
        :return: list of tuple (string, long), the fetched result
        """
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()

        query = "SELECT * FROM " + self.table + " WHERE id=?"
        cursor.execute(query, (id,))

        t = cursor.fetchone()

        cursor.close()
        connection.commit()
        connection.close()

        return t