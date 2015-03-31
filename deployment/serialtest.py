#!/usr/bin/python3

import serial

usbport = '/dev/ttyACM0'

if __name__ == "__main__":
	ser = serial.Serial(usbport, 9600)
	while True:
		data = str(ser.readline(), 'ascii')
		data = data[0 : len(data) - 1]
		print(data)