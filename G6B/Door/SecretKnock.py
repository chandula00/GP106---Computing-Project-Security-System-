### Import Modules ###
from time import time, sleep
from pyfirmata import Arduino, INPUT, util
from VariablesAndOther.VARIABLES import *
from VariablesAndOther.Bottons.Bottons import Botton

####################################################################
'''  Door class  '''


class DoorLock:
    ''' class that used for Door '''

    def __init__(self, board, pin):
        # initialize the Attributes
        self.board = board
        self.pin = pin
        self.botton = Botton(self.board, self.pin)
        self.PASSED, self.Press, self.LOCK, self.STARTED_CHANCE, self.BEGIN, self.RESET = False, False, False, False, False, False
        self.TIME, self.TIME_CHANCE, self.TIMEPASS, self.COUNT, self.KNOCK_COUNT, self.TIME_ALL = 0, 0, 0, 0, 0, 0
        self.ARRAY = []

    def changeTimes(self):
        '''A method to change Times in a Object'''
        if not self.Press:
            if self.KNOCK_COUNT == 0:
                self.STARTED_CHANCE = True
                self.TIME_CHANCE = time()
                self.TIME = time()
                if self.COUNT == 0:
                    self.TIME_ALL = time()
                    self.BEGIN = True
            else:
                self.TIMEPASS = time() - self.TIME
                self.TIME = time()
                self.ARRAY.append(self.TIMEPASS)
            self.KNOCK_COUNT += 1
            self.Press = True

    def ifPress(self):
        '''A method that check if the botton pressed and run changeTime()'''
        if self.botton.state == PRESS and self.KNOCK_COUNT < KNOCK_COUNT:
            self.changeTimes()
        else:
            self.Press = False

    def check(self, arr1):
        '''A method the check the Knock is correct'''
        if self.KNOCK_COUNT == KNOCK_COUNT:
            for i in self.ARRAY:
                x, y = arr1[self.ARRAY.index(i)]
                if not x < i <= y:
                    self.COUNT += 1
                    self.KNOCK_COUNT, self.STARTED_CHANCE = 0, False
                    self.ARRAY.clear()
                    return False
            else:
                self.KNOCK_COUNT, self.STARTED_CHANCE = 0, False
                self.ARRAY.clear()
                return True
        else:
            return False

    def LogicDoor(self):
        '''Logic method'''
        if self.COUNT < COUNT:
            if self.check(ARRAY):
                self.PASSED = True
        elif self.COUNT == 3:
            self.COUNT, self.KNOCK_COUNT, self.STARTED_CHANCE, self.BEGIN, self.LOCK = 0, 0, False, False, True

    def checkChanceTime(self):
        '''A method to check the Full time and Chance time'''
        if time() - self.TIME_CHANCE > TIME_CHANCE and self.STARTED_CHANCE and not self.LOCK:
            self.COUNT += 1
            self.KNOCK_COUNT, self.STARTED_CHANCE = 0, False
            self.ARRAY.clear()
        if time() - self.TIME_ALL > TIME_RESET and not self.LOCK and self.BEGIN and not self.STARTED_CHANCE:
            self.COUNT, self.KNOCK_COUNT, self.STARTED_CHANCE, self.BEGIN = 0, 0, False, False
            self.ARRAY.clear()
            self.RESET = True

    def Setup(self):
        '''The Main Method'''
        self.RESET = False
        if self.PASSED:
            self.COUNT, self.PASSED, self.BEGIN = 0, False, False

        self.checkChanceTime()
        if not self.LOCK:
            self.botton.updateState()
            self.ifPress()
            self.LogicDoor()

    def liftLock(self):
        '''A method to Lift the LockDown'''
        self.COUNT, self.LOCK = 0, False


###############################################################################


###############################################################################
if __name__ == "__main__":
    board = Arduino("COM3")
    digital_pin = 8
    it = util.Iterator(board)
    it.start()

    DOORLOCK = DoorLock(board, digital_pin)
    while True:
        DOORLOCK.Setup()
        print(DOORLOCK.LOCK, DOORLOCK.TIME_ALL, DOORLOCK.TIME_CHANCE, DOORLOCK.STARTED_CHANCE, DOORLOCK.COUNT,
              DOORLOCK.KNOCK_COUNT, DOORLOCK.ARRAY)
        sleep(SLEEP)
###################################################################################
