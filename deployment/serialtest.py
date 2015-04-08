import serial
import time


if __name__ == "__main__":

    usb_port = "/dev/ttyACM0"
    baud_rate = 9600
    idle_time = 60

    ser = serial.Serial(usb_port, baud_rate)

    while True:
        time.sleep(idle_time / 10)

        try:
            val = str(ser.readline(), 'ascii')
            val = float(val)
        except:
            print("[ ERROR ] serial reading failed - monitor terminated")
            sys.exit()

        print("[ SENSOR ]               ", val)