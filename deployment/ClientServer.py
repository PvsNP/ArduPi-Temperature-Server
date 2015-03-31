import time
import http.client
import urllib.parse

class Monitor:
    """
    wrapper class to database inserting operations and sensor monitoring
    """
    def __init__(self, tempDB):
        """
        this is the class constructor
        :param tempDB: TemperatureDatabase
        :return: None
        """
        self.database = tempDB
        self.values_list = []
        self.id_counter = 1

    def insert_data(self, value):
        """
        this function connects to the database and allow the user to insert data,
        it manages the id counter too
        :param: value, the sensor value
        :param: id, integer
        :return: None
        """
        self.values_list.append(value)

        if len(self.values_list) == 10:
            for elem in self.values_list[1:]:
                self.values_list[0] += elem

            final = self.values_list[0] / 10.0
            timestamp = str(int(time.time()))

            final_list = [(self.id_counter, final, timestamp)]
            self.database.insert_values(final_list)

            self.id_counter += 1
            self.values_list = []


class WebClient:
    """
    wrapper class to server connections
    """
    def __init__(self, tempDB, uri, url):
        """
        this is the class constructor
        :param tempDB: TemperatureDatabase
        :param uri: string, the URI of the cloud service
        :param url: string, the URL of the cloud service
        :return: None
        """
        self.database = tempDB
        self.client_uri = uri
        self.client_url = url

    def check_connection(self):
        """
        this is a simple tool to check for a connection
        :return: boolean
        """
        connected = True

        test_client = http.client.HTTPConnection("azure.microsoft.com")
        try:
            test_client.request("HEAD", "/")
        except:
            connected = False

        test_client.close()
        return connected

    def send_data(self, id):
        """
        this function will be used to send data to the remote server
        :param id: integer
        :return: None
        """
        while not self.check_connection():
            time.sleep(10)

        data = self.database.retrieve_values(id)

        params = urllib.parse.urlencode({'temperature': data[1], 'measuretime': data[2]})
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}

        try:
            connection = http.client.HTTPConnection(self.client_uri)
            connection.request('POST', self.client_url, params, headers)
            connection.getresponse()
            connection.close()
        except:
            print("[ ERROR ] connection to remote server failed ")