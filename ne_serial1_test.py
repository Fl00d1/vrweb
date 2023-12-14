import serial
import time
ser = serial.Serial('COM14',115200)
ser.reset_input_buffer()
ser.timeout=0.001
ser.write_timeout=0.001

while True:
    try:
        time.sleep(0.01)
        motorspeed=input().encode()
        ser.write(motorspeed)
    except:
        print("Keyboard Interrupt")
        ser.close()
        break
