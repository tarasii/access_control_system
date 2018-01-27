import serial
import time
from datetime import datetime
import os

ser = None
opened = False
i = 0

while 1 :
    if os.path.isfile('stoprfid'):
        if opened:
            ser.close()
            os.remove('stoprfid')
            print datetime.now(), "stopped" 
            quit()

    if not opened:
        try:
            time.sleep(0.2)
            ser = serial.Serial(
                 port='/dev/ttyACM0',
                 baudrate=115200,
                 parity=serial.PARITY_ODD,
                 stopbits=serial.STOPBITS_TWO,
                 bytesize=serial.SEVENBITS
            )
            opened = ser.isOpen()
            if opened:
                print datetime.now(), "connected"
                i = 0
        except:
            i+=1;
            print datetime.now(), "trying to reconect", i 
    else:
        out = ''
        time.sleep(0.1)
        try:
            while ser.inWaiting() > 0:
                tmp = ser.read(1)
                out += tmp
        except:
            ser.close()
            opened = False
            print datetime.now(), "connection lost"

        if out:
            res = "{} {} {}".format(datetime.now(), 0, out)
            print res
            f = open('rfid0', 'w')
            f.write(res)
            f.close()

    