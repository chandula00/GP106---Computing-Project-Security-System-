### import modules ###
from pyfirmata import OUTPUT, Arduino, util
from time import sleep, time
from VariablesAndOther.VARIABLES import *

###############################################################
'''  class Buzzer  '''


class Buzzer:

    def __init__(self, board, pin):
        self.board = board
        self.pin = pin
        self.ON, self.OFF = False, False
        self.board.digital[self.pin].mode = OUTPUT

    def onBuzzer(self):
        self.ON = True
        self.OFF = False

    def offBuzzer(self):
        self.OFF = True
        self.ON = False


    def RUN(self):
        if self.ON:
            self.board.digital[self.pin].write(1)
        else:
            self.board.digital[self.pin].write(0)


##########################################################################

if __name__ == "__main__":

    board = Arduino("COM3")
    digital_pin = 6
    it = util.Iterator(board)
    it.start()
    Buz = Buzzer(board, digital_pin)
    Buz.onBuzzer()

    while True:
        Buz.RUN()
        sleep(SLEEP)