
class DatabaseConfiguration:
    def __init__(self):
        """
        this class is used to set the database configuration
        """
        self.resources_path = None
        self.database_name = None
        self.database_complete_path = None
        self.table_name = None
        self.creation_query = None
        self.configuration = {
            "database_resources_path": None,
            "database_name":           None,
            "database_table_name":     None,
            "database_creation_query": None
        }

    def finalize_configuration(self):
        """
        this method can be used to finalize the configuration
        :return: bool, success or not
        """
        proceed = True
        for conf in self.configuration:
            if self.configuration[conf] is None:
                proceed = False

        if proceed:
            self.resources_path = self.configuration["database_resources_path"]
            self.database_name  = self.configuration["database_name"]
            self.database_complete_path = self.resources_path + "/" + self.database_name
            self.table_name     = self.configuration["database_table_name"]
            self.creation_query = self.configuration["database_creation_query"]
            print("[ OK ] Database configured successfully")

        return proceed


class ClientConfiguration:
    def __init__(self):
        """
        this class is used to set the client configuration
        """
        self.client_uri = None
        self.client_url = None
        self.configuration = {
            "client_uri": None,
            "client_url": None
        }

    def finalize_configuration(self):
        """
        this method can be used to finalize the configuration
        :return: bool, success or not
        """
        proceed = True
        for conf in self.configuration:
            if self.configuration[conf] is None:
                proceed = False

        if proceed:
            self.client_uri = self.configuration["client_uri"]
            self.client_url = self.configuration["client_url"]
            print("[ OK ] Client configured successfully")
        return proceed


class ArduinoConfiguration:
    def __init__(self):
        """
        this class is used to set the Arduino configuration
        """
        self.usb_port = None
        self.baud_rate = None
        self.idle_time = None
        self.configuration = {
            "arduino_usb_port":  None,
            "arduino_baud_rate": None,
            "arduino_idle_time": None,
        }

    def finalize_configuration(self):
        """
        this method can be used to finalize the configuration
        :return: bool, success or not
        """
        proceed = True
        for conf in self.configuration:
            if self.configuration[conf] is None:
                proceed = False

        if proceed:
            self.usb_port =  self.configuration["arduino_usb_port"]
            self.baud_rate = int(self.configuration["arduino_baud_rate"])
            self.idle_time = int(self.configuration["arduino_idle_time"])
            print("[ OK ] Arduino parameters configured successfully")

        return proceed


class ServerConfiguration:
    def __init__(self):
        """
        this class is used to set the complete server configuration
        """
        self.database = DatabaseConfiguration()
        self.client = ClientConfiguration()
        self.arduino = ArduinoConfiguration()

    def config_init(self, config_file):
        """
        this method can be used to start the configuration reading the config file
        :param: string, the configuration file path
        """
        print("[ OK ] starting server configuration... ")

        conf = open(config_file, 'r')
        for line in conf:
            if line[0] != "#":
                config = line.split(" = ")
                if "database" in config[0]:
                    self.database.configuration[config[0]] = config[1][:len(config[1]) - 1]
                elif "client" in config[0]:
                    self.client.configuration[config[0]] = config[1][:len(config[1]) - 1]
                elif "arduino" in config[0]:
                    self.arduino.configuration[config[0]] = config[1][:len(config[1]) - 1]

        d = self.database.finalize_configuration()
        c = self.client.finalize_configuration()
        a = self.arduino.finalize_configuration()

        if d and c and a:
            print("\n------------------------------------------------------------------")
            print("TEMPERATURE SERVER CONFIGURATION v. 0.0.1 \n")

            print("DATABASE: ")
            print("          - database name:", self.database.database_name)
            print("          - database table name:", self.database.table_name)

            print("CLIENT: ")
            print("          - hostname:", self.client.client_uri)
            print("          - resource:", self.client.client_url)

            print("ARDUINO: ")
            print("          - usb port:", self.arduino.usb_port)
            print("          - baud rate:", self.arduino.baud_rate)
            print("          - idle time:", self.arduino.idle_time)

            print("------------------------------------------------------------------")

        if not (d and c and a):
            print("[ ERROR ] configuration failed, please check 'main.cf' configuration file!")
