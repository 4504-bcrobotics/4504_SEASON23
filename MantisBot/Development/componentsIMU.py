import wpilib
import ctre

class IMUModule:

    imuSensor: ctre.Pigeon2

    def __init__(self):
        self.YPR = (0, 0, 0)
        self.errorCode = None

    def getYPR(self):
        return self.YPR

    def getErrorCode(self):
        return self.errrorCode

    def execute(self):
        (self.errorCode, self.YPR) = self.imuSensor.getYawPitchRoll()
        pass 
