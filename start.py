import threading
import time
import sys
import serial

from deployment.ClientServer import Monitor, WebClient
from deployment.DBMS import TemperatureDatabase
from deployment.IO.configuration import ServerConfiguration

global id_flag
global server

def monitoring(database, lock, debug=False):
    """
    this function is run by a thread to load data into db from serial
    :return: None
    """
    global server
    ser = serial.Serial(server.arduino.usb_port,
                        server.arduino.baud_rate)
    monitor = Monitor(database)
    counter = 0
    acquired = False

    while True:
        time.sleep(server.arduino.idle_time / 10)
        if not acquired:
            lock.acquire()
            acquired = True

        val = str(ser.readline(), 'ascii')
        val = val[0:len(val) - 2]
        try:
            val = int(val)
        except ValueError:
            continue

        monitor.insert_data(val)
        if debug:
            print("[DEBUG] data inserted...", counter)

        counter += 1
        if counter == 10:
            global id_flag
            id_flag = True
            lock.release()
            acquired = False
            counter = 0



def azure_interface(database, lock):
    """
    this function is run by a thread to load data from the db to the cloud
    :return: None
    """
    global server
    client = WebClient(database,
                       server.client.client_uri,
                       server.client.client_url)
    time.sleep(server.arduino.idle_time)
    id_counter_local = 1
    
    while True:
        lock.acquire()
        global id_flag
        if id_flag:
            client.send_data(id_counter_local)
            print("[ SUCCESS ] connection correctly performed")
            id_counter_local += 1
            id_flag = False
            
        lock.release()
        time.sleep(server.arduino.idle_time)

        
def startup():
    """
    this function can be used to launch the server: it manages the thread creation
    and so on
    :return: None
    """
    print("\n[ OK ] Temperature server is starting up...")
    global server
    server = ServerConfiguration()
    server.config_init("main.cf")

    database = TemperatureDatabase(server.database.database_complete_path,
                                   server.database.database_name,
                                   server.database.table_name)
    global id_flag
    id_flag = False

    lock = threading.Lock()

    try:
        thread_monitor = threading.Thread(target = monitoring, args = (database, lock))
        thread_monitor.start()

        thread_client = threading.Thread(target = azure_interface, args = (database, lock))
        thread_client.start()

    except:
        print("[ERROR] Thread creation")
        sys.stdout.flush()
        sys.exit()


if __name__ == "__main__":
    startup()
