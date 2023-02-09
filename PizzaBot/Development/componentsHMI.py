import wpilib

class FlightStickHMI:
    def __init__(self, stickLeft_ID, stickRight_ID):
        self.leftStick = wpilib.Joystick(stickLeft_ID)
        self.rightStick = wpilib.Joystick(stickRight_ID)
        self.fsR = 0
        self.fsL = 0
        self.changed = True

    def is_changedInput(self):
        fsL = self.leftStick.getY()
        fsR = self.rightStick.getY()

        if fsL != self.fsL or fsR != self.fsR:
            self.fsR = fsR
            self.fsL = fsL
            self.changed = True
            return True

        else:
            self.changed = False
            return False

    def getInput(self):
        return (self.fsL, self.fsR)

class HMIModule:
    hmi_interface: FlightStickHMI

    def __init__(self):
        self.fsR = 0
        self.fsL = 0
        self.changed = False

    def getInput(self): # fsTuple = (fsL, fsR)
        self.changed = False
        return (self.fsL, self.fsR)

    def is_changed(self):
        return self.changed

    def execute(self):
        if self.hmi_interface.is_changedInput():
            (self.fsL, self.fsR) = self.hmi_interface.getInput()
            self.changed = True


