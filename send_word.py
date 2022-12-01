import struct
import serial
from serial.tools.list_ports import comports

# send -13 (0xFFFFFFF3) as 32-bit value
# send 13 (0x0000000D) as 32-bit value
my_integer = 13

# set the format to be little endian signed integer (4 bytes signed int) (int16)
int_format = "<i"

# convert to desired bytes size (4 byte signed int) and order
# https://docs.python.org/3/library/struct.html
int_bytes = struct.pack(int_format, my_integer)

# print our results to be sure we're correct
print("Base 10: ", my_integer, "Base 16:", hex(int_bytes[3]), hex(int_bytes[2]), hex(int_bytes[1]), hex(int_bytes[0]))


# set parameters for serial port
portName='/dev/cu.usbmodem101'
#portName = 'COM3'
baudRate = 9600

# attempt to open port
try:
    ser = serial.Serial(portName, baudRate)
    print("Opening port " + ser.name)

# if fail, print a helpful message
except:
    print("Couldn't open port. Try changing portName to one of the options below:")
    ports_list = comports()
    for port_candidate in ports_list:
        print(port_candidate.device)
    exit(-1)

if ser.is_open == True:
    print("Success!")

else:
    print("Unable to open port :(")
    exit(0)

# wait until we have an '!' from the Arduino
bytes = ser.readline()

# decode bytes into string
received = bytes.decode('utf-8')
received = received.replace('\r', '').replace('\n', '')

if '!' in received is False:
    print("Invalid request received. Continue to wait.")
    exit(-1)

# clear the input buffer in case we've been spammed
ser.reset_input_buffer()

# send bytes down to Arduino
ser.write(int_bytes)

for i in range(0,2):
    # wait until a response from the board
    bytes = ser.readline()

    # decode bytes into string
    response = bytes.decode('utf-8')
    response = response.replace('\r', '').replace('\n', '')

    print("Target reported: "+response)