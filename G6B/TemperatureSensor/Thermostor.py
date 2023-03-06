### import Moduels ###
from pyfirmata import Arduino, INPUT, util
from numpy import log
from VariablesAndOther.VARIABLES import *
from time import sleep

########################################################################
'''  class for thermistor  '''

class Thermistor:

    def __init__(self, board, pin):
        self.board = board
        self.pin = pin
        self.TEMP = 0
        self.GOODTEMP = True
        self.board.analog[self.pin].mode = INPUT
        self.board.analog[self.pin].enable_reporting()

        self.getVAL()
        self.getTemperature()

    def getVAL(self):
        self.VAL = self.board.analog[self.pin].read()
        if self.VAL == None or self.VAL == 0:
            self.VAL = 0.0001
        elif self.VAL == 1:
            self.VAL = 0.9999

    def getTemperature(self):
        self.getVAL()
        VRT = 5.0 * self.VAL
        VR = VCC - VRT
        RT = VRT / (VR / R)
        ln = log(RT / RT0)
        TX = (1 / ((ln / B) + (1 / T0)))
        self.TEMP = TX - 273.15
        return self.TEMP

    def checkTemperature(self):
        self.getTemperature()
        if TEMP_LIMITS[0] <= self.TEMP < TEMP_LIMITS[1]:
            self.GOODTEMP = True
        else:
            self.GOODTEMP = False
###########################################################################

##########################################################################
if __name__ == "__main__":
    board = Arduino("COM3")
    pin = 0
    it = util.Iterator(board)
    it.start()

    Term = Thermistor(board, pin)

    while True:
        print(Term.getTemperature(), Term.VAL, Term.GOODTEMP)

        sleep(SLEEP)
##########################################################################