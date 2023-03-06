### IMPORTING MODULES ###
from pyfirmata import Arduino, util
from time import sleep
from ENGINE import *
from Door.SecretKnock import DoorLock
from TemperatureSensor.Thermostor import Thermistor
from PanicBotton.Panic import PanicBotton
from VariablesAndOther.Leds.Leds import Led
from VariablesAndOther.Buzzers.Buzzers import Buzzer
from VariablesAndOther.Bottons.Bottons import Botton
from VariablesAndOther.VARIABLES import *


################### Creating a Board ######################
BOARD = Arduino("COM3")
it = util.Iterator(BOARD)
it.start()

################### Creating Door Lock ########################
LOCK = DoorLock(BOARD, DOORLOCK_PIN)
################## Creating Thermistor ######################
THERM = Thermistor(BOARD, THERMISTOR_PIN)
################# Creating Panic Botton ####################
PANIC = PanicBotton(BOARD,PANIC_PIN)

################# Initializing the LEDs #####################
LED_KNOCK = Led(BOARD, LED_KNOCK_PIN)
LED_PANIC = Led(BOARD, LED_PANIC_PIN)
LEDs = [LED_KNOCK, LED_PANIC]
################# Initializing the Buzzer #####################
BUZ_TEMP = Buzzer(BOARD, BUZ_TEMP_PIN)
################# Initializing the UNLOCK Bottons #####################
UNLOCK_BOTTON = Botton(BOARD,UNLOCK_BOTTON_PIN)
UNPANIC_BOTTON = Botton(BOARD,UNPANIC_PIN)


'''' MAIN LOOP '''
while True:
    KnockLogic(LOCK, LED_KNOCK, UNLOCK_BOTTON)
    PanicLogic(PANIC,LED_PANIC, UNPANIC_BOTTON )
    ThermistorLogic(THERM,BUZ_TEMP)

    print(PANIC.EMERGENCY, LOCK.botton.state,THERM.TEMP,LOCK.LOCK,LOCK.COUNT,LOCK.KNOCK_COUNT,LOCK.ARRAY)

    BUZ_TEMP.RUN()
    LedRun(LEDs)
    sleep(SLEEP)