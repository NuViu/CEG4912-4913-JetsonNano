import time
import serial

from voice_prompts import *

from haptic_handler import *

# The purpose of this file is to act as the center of the cane logic. Processing the
# data from the dictionary sent by the Arduino Nano, this file will deligate tasks to
# different modules in our code base.

def keysInDict(dic, keys):
    for key in keys:
        if key not in dic.keys():
            return False
    return True

print('Dictionary Processing')

# Initializing serial port

serial_port = serial.Serial(port='/dev/ttyTHS1', baudrate=115200,
                            bytesize=serial.EIGHTBITS,
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE)

# Wait for serial port initialization

time.sleep(1)

prev_sm_state = 0
prev_nm_state = 0
hapticEnabled = 0

try:

    # wait for input at serial port

    while True:
        finalString = ''
        state = False
        while True:
            if serial_port.inWaiting() > 0:
                data = serial_port.read()

                # print recieved data

                valReceived = data.decode()
                if valReceived == '{':
                    state = True
                if state:
                    finalString = finalString + valReceived
                    if valReceived == '}':
                        break

        if finalString != '':
            print(finalString)
            try:
                finalDict = eval(finalString)

                # Using the dictionairy keys determine states
                # (street mode, navigation mode, left haptic, right haptic, fall detect)
                # Dict Struct:
                # {
                # ....sm: 0,
                # ....nm: 0,
                # ....lh: 1234,
                # ....rh: 4321,
                # ....fd: 0,
                # }


                if keysInDict(finalDict, ['lh', 'rh', 'nm', 'sm']):
                
                    # street mode
                    if(finalDict["sm"] != prev_sm_state):
                        if (finalDict["sm"] == 1):
                            street_mode_e()
                        elif (finalDict["sm"] == 0):
                            street_mode_d()

                    prev_sm_state = finalDict["sm"]

                    # navigation mode
                    if(finalDict["nm"] != prev_nm_state):
                        #if nav mode is disabled then stop both Haptic motors =
                        if(finalDict["nm"] == 0):
                            runLeftHaptic(0)
                            runRightHaptic(0)
                            # play nm disable audio
                            nav_mode_d()
                        else:
                            # play nm disable audio
                            nav_mode_e()

                    prev_nm_state = finalDict["nm"]

                        # Left and Right Haptic Level - 0 off, <1,2,3> on & intesity
                    
                    if(finalDict["nm"]):
                        runLeftHaptic(finalDict['lh'])
                        runRightHaptic(finalDict['rh'])

            except SyntaxError:

                # Fall Detection - 0 no fall detected, 1 fall detected

                print('dropped datagram')
except KeyboardInterrupt:
    print('Exiting Program')
finally:

    serial_port.close()
    p_right.stop()
    p_left.stop()
    GPIO.cleanup()
    pass


