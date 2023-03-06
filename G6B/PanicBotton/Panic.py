### import modules ###
from VariablesAndOther.Bottons.Bottons import Botton
from VariablesAndOther.VARIABLES import *

#################################################################################
'''  Panic Botton class'''

class PanicBotton:

    def __init__(self,board,pin):
        self.board = board
        self.pin = pin
        self.botton = Botton(self.board,self.pin)
        self.resetBotton()

    def checkEmergency(self):
        self.botton.updateState()
        if not self.EMERGENCY:
            if self.botton.state == PRESS:
                self.EMERGENCY = True
            else:
                self.EMERGENCY = False

    def resetBotton(self):
        self.EMERGENCY = False
##################################################################################
