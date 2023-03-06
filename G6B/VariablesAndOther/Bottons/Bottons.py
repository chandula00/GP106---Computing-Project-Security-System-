###  import modules ###
from pyfirmata import INPUT
from VariablesAndOther.VARIABLES import *

############################################################################
'''  Botton class  '''


class Botton:

    def __init__(self, board, pin):
        self.board = board
        self.pin = pin
        self.state = UNPRESS
        self.board.digital[self.pin].mode = INPUT
        self.updateVAL()

    def updateVAL(self):
        self.VAL = self.board.digital[self.pin].read()

    def updateState(self):
        '''A method read the input and change the State'''
        self.updateVAL()
        if self.VAL == None:
            self.state = UNPRESS
        elif self.VAL:
            self.state = PRESS
        else:
            self.state = UNPRESS

    def readStates(self):
        return self.state
#####################################################################################
