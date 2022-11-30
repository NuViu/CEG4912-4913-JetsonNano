import time
import serial

from voice_prompts import *

from haptic_handler import *

from State_machine import State_machine

from snail import snail

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

orev_rs_state = 0
prev_sm_state = 0
prev_nm_state = 0
prev_fd_state = 0
hapticEnabled = 0
ml_model = State_machine()
ml_model.startup()
fall = snail()

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
                # ....rs> 1,
                # ....lh: 1234,
                # ....rh: 4321,
                # ....fd: 0,
                # }


                if keysInDict(finalDict, ['lh', 'rh', 'nm', 'sm', 'rs', 'fd']):
                

                    # disable rs & sm threads ####################
                        #must be here to avoid starting new thread while old one has camera
                    if(finalDict["rs"] != prev_rs_state):
                        if(finalDict["rs"] == 0):
                            ml_model.stop_text()

                    if(finalDict["sm"] != prev_sm_state):
                        if(finalDict["sm"] == 0):
                            ml_model.stop_object()

                    # read signs #################################
                    if(finalDict["rs"] != prev_rs_state):
                        if (finalDict["rs"] == 1):
                            #street_mode_e()
                            #print("road signs enabled")
                            ml_model.run_text()
                        elif (finalDict["rs"] == 0):
                            #street_mode_d()
                            print("road signs disabled")
                    
                    prev_rs_state = finalDict["rs"]
                    #############################################

                    # street mode ###############################
                    if(finalDict["sm"] != prev_sm_state):
                        if (finalDict["sm"] == 1):
                            street_mode_e()
                            ml_model.run_object()
                        elif (finalDict["sm"] == 0):
                            street_mode_d()

                            
                    prev_sm_state = finalDict["sm"]
                    ##############################################

                    # navigation mode ############################
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

                    ###############################################

                    # fall detection TODO ########################
                    if(finalDict["fd"] != prev_fd_state):
                        if (finalDict["fd"] == 1):
                            fall.run()
                            print("Fall detected, email sent")  
                        elif (finalDict["fd"] == 0):
                            print("Fall handled")
                    
                    prev_fd_state = finalDict["fd"]
                    #############################################1

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


