''' MAIN FUNCTIONS AND LOGICS '''
from VariablesAndOther.VARIABLES import *

########################################################################
########################################################################
''' FOR Secrete Knock'''
Flag = False


def KnockLogic(LOCK, LED, BOTTON):
    global Flag

    if LOCK.LOCK:
        LED.blink()
        BOTTON.updateState()
        print("LOCKED")
        if BOTTON.state == UNPRESS:
            LED.onLed()
            LOCK.liftLock()
    elif LOCK.PASSED:
        print("PASSED")
        LED.blink(BLINK_3)
    elif LOCK.RESET:
        print("RESET")
        LED.blink(BLINK_1)
    elif LOCK.STARTED_CHANCE:
        print("ACTIVE")
        LED.offLed()
    else:
        print("DIACTIVE")
        LED.onLed()

    LOCK.Setup()


##############################################################################
##############################################################################

##############################################################################
##############################################################################
''' FOR Panic Botton  '''


def PanicLogic(PANIC, LED, BOTTON):
    PANIC.checkEmergency()
    if PANIC.EMERGENCY:
        LED.blink()
        BOTTON.updateState()
        if BOTTON.state == UNPRESS:
            pass
            # PANIC.resetBotton()
            # LED.offLed()
    else:
        LED.offLed()


###############################################################################
################################################################################

############################################################################
############################################################################
''' FOR Temperature sensor  '''


def ThermistorLogic(THERM, BUZ):
    THERM.checkTemperature()
    if THERM.GOODTEMP:
        BUZ.offBuzzer()
    else:
        BUZ.onBuzzer()


#############################################################################
##############################################################################


##############################################################################
''' A function to run LEDs'''


def LedRun(arr):
    for i in arr:
        i.RUN()

###############################################################################
